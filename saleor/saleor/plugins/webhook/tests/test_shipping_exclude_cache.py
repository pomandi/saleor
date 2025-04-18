import json
from unittest import mock

import graphene

from ....webhook.const import CACHE_EXCLUDED_SHIPPING_TIME
from ....webhook.event_types import WebhookEventSyncType
from ....webhook.transport.utils import generate_cache_key_for_webhook
from ...base_plugin import ExcludedShippingMethod


@mock.patch("saleor.webhook.transport.synchronous.transport.cache.get")
@mock.patch("saleor.webhook.transport.synchronous.transport.cache.set")
@mock.patch("saleor.webhook.transport.synchronous.transport.send_webhook_request_sync")
@mock.patch(
    "saleor.plugins.webhook.plugin.generate_excluded_shipping_methods_for_order_payload"
)
def test_excluded_shipping_methods_for_order_use_cache(
    mocked_payload,
    mocked_webhook,
    mocked_cache_set,
    mocked_cache_get,
    webhook_plugin,
    order_with_lines,
    available_shipping_methods_factory,
    shipping_app_factory,
):
    # given
    shipping_app_factory()
    webhook_reason = "Order contains dangerous products."
    other_reason = "Shipping is not applicable for this order."

    mocked_webhook.return_value = {
        "excluded_methods": [
            {
                "id": graphene.Node.to_global_id("ShippingMethod", "1"),
                "reason": webhook_reason,
            }
        ]
    }
    payload = json.dumps({"order": {"id": 1, "some_field": "12"}})
    mocked_payload.return_value = payload

    mocked_cache_get.return_value = (payload, [{"id": "1", "reason": webhook_reason}])

    plugin = webhook_plugin()
    available_shipping_methods = available_shipping_methods_factory(num_methods=2)
    previous_value = [
        ExcludedShippingMethod(id="1", reason=other_reason),
        ExcludedShippingMethod(id="2", reason=other_reason),
    ]

    # when
    plugin.excluded_shipping_methods_for_order(
        order=order_with_lines,
        available_shipping_methods=available_shipping_methods,
        previous_value=previous_value,
    )
    # then
    assert not mocked_webhook.called

    assert not mocked_cache_set.called


@mock.patch("saleor.webhook.transport.synchronous.transport.cache.get")
@mock.patch("saleor.webhook.transport.synchronous.transport.cache.set")
@mock.patch("saleor.webhook.transport.synchronous.transport.send_webhook_request_sync")
@mock.patch(
    "saleor.plugins.webhook.plugin.generate_excluded_shipping_methods_for_order_payload"
)
def test_excluded_shipping_methods_for_order_stores_in_cache_when_empty(
    mocked_payload,
    mocked_webhook,
    mocked_cache_set,
    mocked_cache_get,
    webhook_plugin,
    order_with_lines,
    available_shipping_methods_factory,
    shipping_app_factory,
):
    # given
    shipping_app = shipping_app_factory()
    shipping_webhook = shipping_app.webhooks.get()
    webhook_reason = "Order contains dangerous products."
    other_reason = "Shipping is not applicable for this order."

    webhook_response = {
        "excluded_methods": [
            {
                "id": graphene.Node.to_global_id("ShippingMethod", "1"),
                "reason": webhook_reason,
            }
        ]
    }

    mocked_webhook.return_value = webhook_response

    payload_dict = {"order": {"id": 1, "some_field": "12"}}
    payload = json.dumps(payload_dict)
    mocked_payload.return_value = payload

    mocked_cache_get.return_value = None

    plugin = webhook_plugin()
    available_shipping_methods = available_shipping_methods_factory(num_methods=2)
    previous_value = [
        ExcludedShippingMethod(id="1", reason=other_reason),
        ExcludedShippingMethod(id="2", reason=other_reason),
    ]

    # when
    plugin.excluded_shipping_methods_for_order(
        order=order_with_lines,
        available_shipping_methods=available_shipping_methods,
        previous_value=previous_value,
    )
    # then
    assert mocked_webhook.called

    expected_cache_key = generate_cache_key_for_webhook(
        payload_dict,
        shipping_webhook.target_url,
        WebhookEventSyncType.ORDER_FILTER_SHIPPING_METHODS,
        shipping_app.id,
    )

    mocked_cache_set.assert_called_once_with(
        expected_cache_key,
        webhook_response,
        timeout=CACHE_EXCLUDED_SHIPPING_TIME,
    )


@mock.patch("saleor.webhook.transport.synchronous.transport.cache.get")
@mock.patch("saleor.webhook.transport.synchronous.transport.cache.set")
@mock.patch("saleor.webhook.transport.synchronous.transport.send_webhook_request_sync")
@mock.patch(
    "saleor.plugins.webhook.plugin.generate_excluded_shipping_methods_for_order_payload"
)
def test_excluded_shipping_methods_for_order_stores_in_cache_when_payload_is_different(
    mocked_payload,
    mocked_webhook,
    mocked_cache_set,
    mocked_cache_get,
    webhook_plugin,
    order_with_lines,
    available_shipping_methods_factory,
    shipping_app_factory,
):
    # given
    shipping_app = shipping_app_factory()
    shipping_webhook = shipping_app.webhooks.get()
    webhook_reason = "Order contains dangerous products."
    other_reason = "Shipping is not applicable for this order."
    webhook_response = {
        "excluded_methods": [
            {
                "id": graphene.Node.to_global_id("ShippingMethod", "1"),
                "reason": webhook_reason,
            }
        ]
    }
    mocked_webhook.return_value = webhook_response

    payload_dict = {"order": {"id": 1, "some_field": "12"}}
    payload = json.dumps(payload_dict)
    mocked_payload.return_value = payload

    mocked_cache_get.return_value = None

    plugin = webhook_plugin()
    available_shipping_methods = available_shipping_methods_factory(num_methods=2)
    previous_value = [
        ExcludedShippingMethod(id="1", reason=other_reason),
        ExcludedShippingMethod(id="2", reason=other_reason),
    ]

    # when
    plugin.excluded_shipping_methods_for_order(
        order=order_with_lines,
        available_shipping_methods=available_shipping_methods,
        previous_value=previous_value,
    )
    # then
    assert mocked_webhook.called

    expected_cache_key = generate_cache_key_for_webhook(
        payload_dict,
        shipping_webhook.target_url,
        WebhookEventSyncType.ORDER_FILTER_SHIPPING_METHODS,
        shipping_app.id,
    )

    mocked_cache_get.assert_called_once_with(expected_cache_key)
    mocked_cache_set.assert_called_once_with(
        expected_cache_key,
        webhook_response,
        timeout=CACHE_EXCLUDED_SHIPPING_TIME,
    )


@mock.patch("saleor.webhook.transport.synchronous.transport.cache.get")
@mock.patch("saleor.webhook.transport.synchronous.transport.cache.set")
@mock.patch("saleor.webhook.transport.synchronous.transport.send_webhook_request_sync")
@mock.patch(
    "saleor.plugins.webhook.plugin."
    "generate_excluded_shipping_methods_for_checkout_payload"
)
def test_excluded_shipping_methods_for_checkout_use_cache(
    mocked_payload,
    mocked_webhook,
    mocked_cache_set,
    mocked_cache_get,
    webhook_plugin,
    checkout_with_items,
    available_shipping_methods_factory,
    shipping_app_factory,
):
    # given
    shipping_app_factory()
    webhook_reason = "Order contains dangerous products."
    other_reason = "Shipping is not applicable for this order."

    mocked_webhook.return_value = {
        "excluded_methods": [
            {
                "id": graphene.Node.to_global_id("ShippingMethod", "1"),
                "reason": webhook_reason,
            }
        ]
    }

    payload = json.dumps({"checkout": {"id": 1, "some_field": "12"}})
    mocked_payload.return_value = payload

    mocked_cache_get.return_value = (payload, [{"id": "1", "reason": webhook_reason}])

    plugin = webhook_plugin()
    available_shipping_methods = available_shipping_methods_factory(num_methods=2)
    previous_value = [
        ExcludedShippingMethod(id="1", reason=other_reason),
        ExcludedShippingMethod(id="2", reason=other_reason),
    ]

    # when
    plugin.excluded_shipping_methods_for_checkout(
        checkout_with_items,
        available_shipping_methods=available_shipping_methods,
        previous_value=previous_value,
    )

    # then
    assert not mocked_webhook.called

    assert not mocked_cache_set.called


@mock.patch("saleor.webhook.transport.synchronous.transport.cache.get")
@mock.patch("saleor.webhook.transport.synchronous.transport.cache.set")
@mock.patch("saleor.webhook.transport.synchronous.transport.send_webhook_request_sync")
@mock.patch(
    "saleor.plugins.webhook.plugin."
    "generate_excluded_shipping_methods_for_checkout_payload"
)
def test_excluded_shipping_methods_for_checkout_stores_in_cache_when_empty(
    mocked_payload,
    mocked_webhook,
    mocked_cache_set,
    mocked_cache_get,
    webhook_plugin,
    checkout_with_items,
    available_shipping_methods_factory,
    shipping_app_factory,
):
    # given
    shipping_app = shipping_app_factory()
    shipping_webhook = shipping_app.webhooks.get()

    webhook_reason = "Order contains dangerous products."
    other_reason = "Shipping is not applicable for this order."

    webhook_response = {
        "excluded_methods": [
            {
                "id": graphene.Node.to_global_id("ShippingMethod", "1"),
                "reason": webhook_reason,
            }
        ]
    }
    mocked_webhook.return_value = webhook_response

    payload_dict = {"checkout": {"id": 1, "some_field": "12"}}
    payload = json.dumps(payload_dict)
    mocked_payload.return_value = payload

    mocked_cache_get.return_value = None

    plugin = webhook_plugin()
    available_shipping_methods = available_shipping_methods_factory(num_methods=2)
    previous_value = [
        ExcludedShippingMethod(id="1", reason=other_reason),
        ExcludedShippingMethod(id="2", reason=other_reason),
    ]

    # when
    plugin.excluded_shipping_methods_for_checkout(
        checkout_with_items,
        available_shipping_methods=available_shipping_methods,
        previous_value=previous_value,
    )

    # then
    assert mocked_webhook.called

    expected_cache_key = generate_cache_key_for_webhook(
        payload_dict,
        shipping_webhook.target_url,
        WebhookEventSyncType.CHECKOUT_FILTER_SHIPPING_METHODS,
        shipping_app.id,
    )

    mocked_cache_set.assert_called_once_with(
        expected_cache_key,
        webhook_response,
        timeout=CACHE_EXCLUDED_SHIPPING_TIME,
    )


@mock.patch("saleor.webhook.transport.synchronous.transport.cache.get")
@mock.patch("saleor.webhook.transport.synchronous.transport.cache.set")
@mock.patch("saleor.webhook.transport.synchronous.transport.send_webhook_request_sync")
@mock.patch(
    "saleor.plugins.webhook.plugin."
    "generate_excluded_shipping_methods_for_checkout_payload"
)
def test_excluded_shipping_methods_for_checkout_stores_in_cache_when_payload_different(
    mocked_payload,
    mocked_webhook,
    mocked_cache_set,
    mocked_cache_get,
    webhook_plugin,
    checkout_with_items,
    available_shipping_methods_factory,
    shipping_app_factory,
):
    # given
    shipping_app = shipping_app_factory()
    shipping_webhook = shipping_app.webhooks.get()

    webhook_reason = "Order contains dangerous products."
    other_reason = "Shipping is not applicable for this order."

    webhook_response = {
        "excluded_methods": [
            {
                "id": graphene.Node.to_global_id("ShippingMethod", "1"),
                "reason": webhook_reason,
            }
        ]
    }

    mocked_webhook.return_value = webhook_response

    payload_dict = {"checkout": {"id": 1, "some_field": "12"}}
    payload = json.dumps(payload_dict)
    mocked_payload.return_value = payload

    mocked_cache_get.return_value = None

    plugin = webhook_plugin()
    available_shipping_methods = available_shipping_methods_factory(num_methods=2)
    previous_value = [
        ExcludedShippingMethod(id="1", reason=other_reason),
        ExcludedShippingMethod(id="2", reason=other_reason),
    ]
    # when
    plugin.excluded_shipping_methods_for_checkout(
        checkout_with_items,
        available_shipping_methods=available_shipping_methods,
        previous_value=previous_value,
    )
    # then
    assert mocked_webhook.called

    expected_cache_key = generate_cache_key_for_webhook(
        payload_dict,
        shipping_webhook.target_url,
        WebhookEventSyncType.CHECKOUT_FILTER_SHIPPING_METHODS,
        shipping_app.id,
    )
    mocked_cache_get.assert_called_once_with(expected_cache_key)

    mocked_cache_set.assert_called_once_with(
        expected_cache_key,
        webhook_response,
        timeout=CACHE_EXCLUDED_SHIPPING_TIME,
    )
