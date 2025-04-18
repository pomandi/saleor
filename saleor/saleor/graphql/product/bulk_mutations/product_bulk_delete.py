from collections import defaultdict

import graphene
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models.expressions import Exists, OuterRef

from ....attribute import AttributeInputType
from ....attribute import models as attribute_models
from ....core.tracing import traced_atomic_transaction
from ....order import events as order_events
from ....order import models as order_models
from ....order.tasks import recalculate_orders_task
from ....permission.enums import ProductPermissions
from ....product import models
from ....webhook.event_types import WebhookEventAsyncType
from ....webhook.utils import get_webhooks_for_event
from ...app.dataloaders import get_app_promise
from ...core import ResolveInfo
from ...core.mutations import ModelBulkDeleteMutation
from ...core.types import NonNullList, ProductError
from ...plugins.dataloaders import get_plugin_manager_promise
from ..types import Product
from ..utils import get_draft_order_lines_data_for_variants


class ProductBulkDelete(ModelBulkDeleteMutation):
    class Arguments:
        ids = NonNullList(
            graphene.ID, required=True, description="List of product IDs to delete."
        )

    class Meta:
        description = "Deletes products."
        model = models.Product
        object_type = Product
        permissions = (ProductPermissions.MANAGE_PRODUCTS,)
        error_type_class = ProductError
        error_type_field = "product_errors"

    @classmethod
    @traced_atomic_transaction()
    def perform_mutation(  # type: ignore[override]
        cls, _root, info: ResolveInfo, /, *, ids
    ):
        try:
            pks = cls.get_global_ids_or_error(ids, Product)
        except ValidationError as error:
            return 0, error
        product_to_variant = list(
            models.ProductVariant.objects.filter(product__pk__in=pks).values_list(
                "product_id", "id"
            )
        )
        variants_ids = [variant_id for _, variant_id in product_to_variant]

        cls.delete_assigned_attribute_values(pks)

        draft_order_lines_data = get_draft_order_lines_data_for_variants(variants_ids)

        response = super().perform_mutation(
            _root, info, ids=ids, product_to_variant=product_to_variant
        )

        # delete order lines for deleted variants
        order_models.OrderLine.objects.filter(
            pk__in=draft_order_lines_data.line_pks
        ).delete()

        app = get_app_promise(info.context).get()
        # run order event for deleted lines
        for order, order_lines in draft_order_lines_data.order_to_lines_mapping.items():
            order_events.order_line_product_removed_event(
                order, info.context.user, app, order_lines
            )

        order_pks = draft_order_lines_data.order_pks
        if order_pks:
            recalculate_orders_task.delay(list(order_pks))

        return response

    @staticmethod
    def delete_assigned_attribute_values(instance_pks):
        assigned_values = attribute_models.AssignedProductAttributeValue.objects.filter(
            product_id__in=instance_pks
        )
        attributes = attribute_models.Attribute.objects.filter(
            input_type__in=AttributeInputType.TYPES_WITH_UNIQUE_VALUES
        )

        attribute_models.AttributeValue.objects.filter(
            Exists(assigned_values.filter(value_id=OuterRef("id"))),
            Exists(attributes.filter(id=OuterRef("attribute_id"))),
        ).delete()

    @classmethod
    def bulk_action(  # type: ignore[override]
        cls, info: ResolveInfo, queryset, /, *, product_to_variant
    ):
        product_variant_map = defaultdict(list)
        for product, variant in product_to_variant:
            product_variant_map[product].append(variant)

        products = list(queryset)
        with transaction.atomic():
            variants_ids = tuple(
                models.ProductVariant.objects.order_by("pk")
                .select_for_update(of=("self",))
                .filter(product__in=products)
                .values_list("pk", flat=True)
            )
            models.ProductVariant.objects.filter(pk__in=variants_ids).delete()
            ids = tuple(
                models.Product.objects.order_by("pk")
                .select_for_update(of=("self",))
                .filter(pk__in=[product.pk for product in products])
                .values_list("pk", flat=True)
            )
            models.Product.objects.filter(pk__in=ids).delete()

        webhooks = get_webhooks_for_event(WebhookEventAsyncType.PRODUCT_DELETED)
        manager = get_plugin_manager_promise(info.context).get()
        for product in products:
            variants = product_variant_map.get(product.id, [])
            cls.call_event(
                manager.product_deleted, product, variants, webhooks=webhooks
            )
