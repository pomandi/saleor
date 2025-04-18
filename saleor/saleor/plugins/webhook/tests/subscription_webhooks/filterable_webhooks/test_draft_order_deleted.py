import json
from unittest.mock import patch

import graphene
from django.test import override_settings

from ......core.models import EventDelivery
from ......graphql.webhook.subscription_query import SubscriptionQuery
from ......webhook.event_types import WebhookEventAsyncType
from .....manager import get_plugins_manager

DRAFT_ORDER_DELETED_SUBSCRIPTION = """
subscription {
  draftOrderDeleted(channels: ["%s"]) {
    order {
      id
    }
  }
}
"""


@patch(
    "saleor.webhook.transport.asynchronous.transport.send_webhook_request_async.apply_async"
)
@override_settings(PLUGINS=["saleor.plugins.webhook.plugin.WebhookPlugin"])
def test_draft_order_deleted(mocked_async, order_line, subscription_webhook, settings):
    # given
    manager = get_plugins_manager(False)

    order = order_line.order
    channel = order.channel
    assert channel.slug == settings.DEFAULT_CHANNEL_SLUG

    event_type = WebhookEventAsyncType.DRAFT_ORDER_DELETED

    query = DRAFT_ORDER_DELETED_SUBSCRIPTION % settings.DEFAULT_CHANNEL_SLUG
    webhook = subscription_webhook(query, event_type)
    subscription_query = SubscriptionQuery(query)
    webhook.filterable_channel_slugs = subscription_query.get_filterable_channel_slugs()
    webhook.save()

    order_id = graphene.Node.to_global_id("Order", order.id)

    # when
    manager.draft_order_deleted(order)

    # then
    expected_payload = json.dumps(
        {
            "data": {
                "draftOrderDeleted": {
                    "order": {
                        "id": order_id,
                    }
                }
            }
        }
    )

    deliveries = EventDelivery.objects.all()
    assert len(deliveries) == 1
    assert deliveries[0].payload.get_payload() == expected_payload
    assert deliveries[0].webhook == webhook
    assert mocked_async.called


@patch(
    "saleor.webhook.transport.asynchronous.transport.send_webhook_request_async.apply_async"
)
@override_settings(PLUGINS=["saleor.plugins.webhook.plugin.WebhookPlugin"])
def test_draft_order_deleted_without_channels_input(
    mocked_async, order_line, subscription_webhook
):
    # given
    manager = get_plugins_manager(False)

    order = order_line.order

    event_type = WebhookEventAsyncType.DRAFT_ORDER_DELETED

    query = """subscription {
      draftOrderDeleted {
        order {
          id
        }
      }
    }"""
    webhook = subscription_webhook(query, event_type)
    subscription_query = SubscriptionQuery(query)
    webhook.filterable_channel_slugs = subscription_query.get_filterable_channel_slugs()
    webhook.save()

    order_id = graphene.Node.to_global_id("Order", order.id)

    # when
    manager.draft_order_deleted(order)

    # then
    expected_payload = json.dumps(
        {
            "data": {
                "draftOrderDeleted": {
                    "order": {
                        "id": order_id,
                    }
                }
            }
        }
    )

    deliveries = EventDelivery.objects.all()
    assert len(deliveries) == 1
    assert deliveries[0].payload.get_payload() == expected_payload
    assert deliveries[0].webhook == webhook
    assert mocked_async.called


@patch(
    "saleor.webhook.transport.asynchronous.transport.create_event_delivery_list_for_webhooks"
)
@patch(
    "saleor.webhook.transport.asynchronous.transport.send_webhook_request_async.apply_async"
)
@override_settings(PLUGINS=["saleor.plugins.webhook.plugin.WebhookPlugin"])
def test_draft_order_updated_with_different_channel(
    mocked_async,
    mocked_create_event_delivery_list_for_webhooks,
    order_with_lines_channel_PLN,
    subscription_webhook,
    settings,
):
    # given
    manager = get_plugins_manager(False)

    order = order_with_lines_channel_PLN
    channel = order.channel
    assert channel.slug != settings.DEFAULT_CHANNEL_SLUG

    event_type = WebhookEventAsyncType.DRAFT_ORDER_DELETED

    query = DRAFT_ORDER_DELETED_SUBSCRIPTION % settings.DEFAULT_CHANNEL_SLUG
    webhook = subscription_webhook(query, event_type)
    subscription_query = SubscriptionQuery(query)
    webhook.filterable_channel_slugs = subscription_query.get_filterable_channel_slugs()
    webhook.save()

    # when
    manager.draft_order_deleted(order)

    # then
    assert not mocked_async.called
    assert not mocked_create_event_delivery_list_for_webhooks.called
    deliveries = EventDelivery.objects.all()
    assert len(deliveries) == 0


@patch(
    "saleor.webhook.transport.asynchronous.transport.create_event_delivery_list_for_webhooks"
)
@patch(
    "saleor.webhook.transport.asynchronous.transport.send_webhook_request_async.apply_async"
)
@override_settings(PLUGINS=["saleor.plugins.webhook.plugin.WebhookPlugin"])
def test_different_event_doesnt_trigger_webhook(
    mocked_async,
    mocked_create_event_delivery_list_for_webhooks,
    order_line,
    subscription_webhook,
    settings,
):
    # given
    manager = get_plugins_manager(False)

    order = order_line.order
    channel = order.channel
    assert channel.slug == settings.DEFAULT_CHANNEL_SLUG

    event_type = WebhookEventAsyncType.ORDER_UPDATED

    query = DRAFT_ORDER_DELETED_SUBSCRIPTION % settings.DEFAULT_CHANNEL_SLUG
    webhook = subscription_webhook(query, event_type)
    subscription_query = SubscriptionQuery(query)
    webhook.filterable_channel_slugs = subscription_query.get_filterable_channel_slugs()
    webhook.save()

    # when
    manager.draft_order_deleted(order)

    # then
    assert not mocked_async.called
    assert not mocked_create_event_delivery_list_for_webhooks.called
    deliveries = EventDelivery.objects.all()
    assert len(deliveries) == 0
