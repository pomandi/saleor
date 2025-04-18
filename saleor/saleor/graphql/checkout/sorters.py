from django.db.models import CharField, ExpressionWrapper, OuterRef, QuerySet, Subquery

from ...payment.models import Payment
from ..core.doc_category import DOC_CATEGORY_CHECKOUT
from ..core.types import BaseEnum, SortInputObjectType


class CheckoutSortField(BaseEnum):
    CREATION_DATE = ["created_at", "pk"]
    CUSTOMER = ["billing_address__last_name", "billing_address__first_name", "pk"]
    PAYMENT = ["last_charge_status", "pk"]

    class Meta:
        doc_category = DOC_CATEGORY_CHECKOUT

    @property
    def description(self):
        if self.name in CheckoutSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort checkouts by {sort_name}."
        raise ValueError(f"Unsupported enum value: {self.value}")

    @staticmethod
    def qs_with_payment(queryset: QuerySet, **_kwargs) -> QuerySet:
        subquery = Subquery(
            Payment.objects.filter(checkout_id=OuterRef("pk"))
            .order_by("-pk")
            .values_list("charge_status")[:1]
        )
        return queryset.annotate(
            last_charge_status=ExpressionWrapper(subquery, output_field=CharField())
        )


class CheckoutSortingInput(SortInputObjectType):
    class Meta:
        doc_category = DOC_CATEGORY_CHECKOUT
        sort_enum = CheckoutSortField
        type_name = "checkouts"
