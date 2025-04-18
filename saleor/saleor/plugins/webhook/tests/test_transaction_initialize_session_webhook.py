import json
import uuid
from decimal import Decimal
from unittest import mock

import graphene
from freezegun import freeze_time

from ....channel import TransactionFlowStrategy
from ....core import EventDeliveryStatus
from ....core.models import EventDelivery, EventPayload
from ....payment.interface import (
    PaymentGatewayData,
    TransactionProcessActionData,
    TransactionSessionData,
    TransactionSessionResult,
)
from ....webhook.event_types import WebhookEventSyncType
from ....webhook.models import Webhook

TRANSACTION_INITIALIZE_SESSION = """
subscription {
  event{
    ...on TransactionInitializeSession{
      merchantReference
      action{
        amount
        currency
        actionType
      }
      data
      idempotencyKey
      sourceObject{
        __typename
        ... on Checkout{
          id
        }
        ... on Order{
          id
        }
      }
      issuingPrincipal {
        ... on Node {
          id
        }
      }
    }
  }
}
"""


def _assert_with_subscription(
    source_object,
    transaction,
    request_data,
    amount,
    action_type,
    webhook,
    expected_response,
    response,
    mock_request,
    idempotency_key,
    requestor=None,
    requestor_type=None,
):
    object_id = graphene.Node.to_global_id(
        source_object.__class__.__name__, source_object.pk
    )
    payload = {
        "data": request_data,
        "merchantReference": graphene.Node.to_global_id(
            "TransactionItem", transaction.token
        ),
        "action": {
            "amount": amount,
            "actionType": action_type.upper(),
            "currency": transaction.currency,
        },
        "idempotencyKey": idempotency_key,
        "sourceObject": {
            "__typename": source_object.__class__.__name__,
            "id": object_id,
        },
        "issuingPrincipal": (
            {"id": graphene.Node.to_global_id(requestor_type, requestor.pk)}
            if requestor
            else None
        ),
    }
    _assert_fields(payload, webhook, expected_response, response, mock_request)


def _assert_with_static_payload(
    source_object,
    transaction,
    request_data,
    amount,
    action_type,
    webhook,
    expected_response,
    response,
    mock_request,
):
    source_object_id = graphene.Node.to_global_id(
        source_object.__class__.__name__, source_object.pk
    )
    payload = {
        "id": source_object_id,
        "data": request_data,
        "amount": str(amount),
        "currency": "USD",
        "action_type": action_type.upper(),
        "transaction_id": graphene.Node.to_global_id(
            "TransactionItem", transaction.token
        ),
    }
    _assert_fields(payload, webhook, expected_response, response, mock_request)


def _assert_fields(payload, webhook, expected_response, response, mock_request):
    webhook_app = webhook.app
    mock_request.assert_called_once()
    assert not EventDelivery.objects.exists()
    delivery = mock_request.mock_calls[0].args[0]
    assert json.loads(delivery.payload.get_payload()) == payload
    assert delivery.status == EventDeliveryStatus.PENDING
    assert delivery.event_type == WebhookEventSyncType.TRANSACTION_INITIALIZE_SESSION
    assert delivery.webhook == webhook
    assert response == TransactionSessionResult(
        app_identifier=webhook_app.identifier, response=expected_response, error=None
    )


@freeze_time()
@mock.patch("saleor.webhook.transport.synchronous.transport.send_webhook_request_sync")
def test_transaction_initialize_checkout_without_request_data_and_static_payload(
    mock_request,
    webhook_plugin,
    webhook_app,
    checkout,
    permission_manage_payments,
    transaction_session_response,
    transaction_item_generator,
):
    # given
    expected_response_data = transaction_session_response
    mock_request.return_value = expected_response_data
    plugin = webhook_plugin()

    webhook_app.identifier = "app.identifier"
    webhook_app.save()
    webhook_app.permissions.add(permission_manage_payments)
    webhook = Webhook.objects.create(
        name="Webhook",
        app=webhook_app,
    )
    event_type = WebhookEventSyncType.TRANSACTION_INITIALIZE_SESSION
    webhook.events.create(event_type=event_type)
    amount = Decimal("10.00")

    transaction = transaction_item_generator(
        checkout_id=checkout.pk,
        app=webhook_app,
        psp_reference=None,
        name=None,
        message=None,
    )
    action_type = TransactionFlowStrategy.CHARGE

    # when
    response = plugin.transaction_initialize_session(
        transaction_session_data=TransactionSessionData(
            transaction=transaction,
            source_object=checkout,
            action=TransactionProcessActionData(
                amount=amount,
                currency=transaction.currency,
                action_type=action_type,
            ),
            customer_ip_address="127.0.0.1",
            payment_gateway_data=PaymentGatewayData(
                app_identifier=webhook_app.identifier, data=None, error=None
            ),
        ),
        previous_value=None,
    )

    # then
    _assert_with_static_payload(
        checkout,
        transaction,
        None,
        amount,
        action_type,
        webhook,
        expected_response_data,
        response,
        mock_request,
    )


@freeze_time()
@mock.patch("saleor.webhook.transport.synchronous.transport.send_webhook_request_sync")
def test_transaction_initialize_checkout_with_request_data_and_static_payload(
    mock_request,
    webhook_plugin,
    webhook_app,
    checkout,
    permission_manage_payments,
    transaction_session_response,
    transaction_item_generator,
):
    # given
    data = {"some": "request-data"}
    expected_response_data = transaction_session_response
    mock_request.return_value = expected_response_data
    plugin = webhook_plugin()

    webhook_app.identifier = "app.identifier"
    webhook_app.save()
    webhook_app.permissions.add(permission_manage_payments)
    webhook = Webhook.objects.create(
        name="Webhook",
        app=webhook_app,
    )
    event_type = WebhookEventSyncType.TRANSACTION_INITIALIZE_SESSION
    webhook.events.create(event_type=event_type)
    amount = Decimal("10.00")

    transaction = transaction_item_generator(
        checkout_id=checkout.pk,
        app=webhook_app,
        psp_reference=None,
        name=None,
        message=None,
    )
    action_type = TransactionFlowStrategy.CHARGE

    # when
    response = plugin.transaction_initialize_session(
        transaction_session_data=TransactionSessionData(
            transaction=transaction,
            source_object=checkout,
            action=TransactionProcessActionData(
                amount=amount,
                currency=transaction.currency,
                action_type=action_type,
            ),
            customer_ip_address="127.0.0.1",
            payment_gateway_data=PaymentGatewayData(
                app_identifier=webhook_app.identifier, data=data, error=None
            ),
        ),
        previous_value=None,
    )

    # then
    _assert_with_static_payload(
        checkout,
        transaction,
        data,
        amount,
        action_type,
        webhook,
        expected_response_data,
        response,
        mock_request,
    )


@freeze_time()
@mock.patch("saleor.webhook.transport.synchronous.transport.send_webhook_request_sync")
def test_transaction_initialize_checkout_without_request_data(
    mock_request,
    webhook_plugin,
    webhook_app,
    checkout,
    staff_user,
    permission_manage_payments,
    transaction_session_response,
    transaction_item_generator,
):
    # given

    expected_response_data = transaction_session_response
    mock_request.return_value = expected_response_data
    plugin = webhook_plugin()
    plugin.requestor = staff_user

    webhook_app.identifier = "app.identifier"
    webhook_app.save()
    webhook_app.permissions.add(permission_manage_payments)
    webhook = Webhook.objects.create(
        name="Webhook",
        app=webhook_app,
        subscription_query=TRANSACTION_INITIALIZE_SESSION,
    )
    event_type = WebhookEventSyncType.TRANSACTION_INITIALIZE_SESSION
    webhook.events.create(event_type=event_type)
    amount = Decimal("10.00")

    transaction = transaction_item_generator(
        checkout_id=checkout.pk,
        app=webhook_app,
        psp_reference=None,
        name=None,
        message=None,
    )
    action_type = TransactionFlowStrategy.CHARGE
    idempotency_key = str(uuid.uuid4())

    # when
    response = plugin.transaction_initialize_session(
        transaction_session_data=TransactionSessionData(
            transaction=transaction,
            source_object=checkout,
            action=TransactionProcessActionData(
                amount=amount,
                currency=transaction.currency,
                action_type=action_type,
            ),
            customer_ip_address="127.0.0.1",
            payment_gateway_data=PaymentGatewayData(
                app_identifier=webhook_app.identifier, data=None, error=None
            ),
            idempotency_key=idempotency_key,
        ),
        previous_value=None,
    )

    # then
    _assert_with_subscription(
        checkout,
        transaction,
        None,
        amount,
        action_type,
        webhook,
        expected_response_data,
        response,
        mock_request,
        idempotency_key,
        requestor=staff_user,
        requestor_type="User",
    )


@freeze_time()
@mock.patch("saleor.webhook.transport.synchronous.transport.send_webhook_request_sync")
def test_transaction_initialize_checkout_without_request_data_app_requestor(
    mock_request,
    webhook_plugin,
    webhook_app,
    checkout,
    permission_manage_payments,
    transaction_session_response,
    transaction_item_generator,
):
    # given

    expected_response_data = transaction_session_response
    mock_request.return_value = expected_response_data
    plugin = webhook_plugin()
    plugin.requestor = webhook_app

    webhook_app.identifier = "app.identifier"
    webhook_app.save()
    webhook_app.permissions.add(permission_manage_payments)
    webhook = Webhook.objects.create(
        name="Webhook",
        app=webhook_app,
        subscription_query=TRANSACTION_INITIALIZE_SESSION,
    )
    event_type = WebhookEventSyncType.TRANSACTION_INITIALIZE_SESSION
    webhook.events.create(event_type=event_type)
    amount = Decimal("10.00")

    transaction = transaction_item_generator(
        checkout_id=checkout.pk,
        app=webhook_app,
        psp_reference=None,
        name=None,
        message=None,
    )
    action_type = TransactionFlowStrategy.CHARGE
    idempotency_key = str(uuid.uuid4())

    # when
    response = plugin.transaction_initialize_session(
        transaction_session_data=TransactionSessionData(
            transaction=transaction,
            source_object=checkout,
            action=TransactionProcessActionData(
                amount=amount,
                currency=transaction.currency,
                action_type=action_type,
            ),
            customer_ip_address="127.0.0.1",
            payment_gateway_data=PaymentGatewayData(
                app_identifier=webhook_app.identifier, data=None, error=None
            ),
            idempotency_key=idempotency_key,
        ),
        previous_value=None,
    )

    # then
    _assert_with_subscription(
        checkout,
        transaction,
        None,
        amount,
        action_type,
        webhook,
        expected_response_data,
        response,
        mock_request,
        idempotency_key,
        requestor=webhook_app,
        requestor_type="App",
    )


@freeze_time()
@mock.patch("saleor.webhook.transport.synchronous.transport.send_webhook_request_sync")
def test_transaction_initialize_checkout_with_request_data(
    mock_request,
    webhook_plugin,
    webhook_app,
    checkout,
    permission_manage_payments,
    transaction_session_response,
    transaction_item_generator,
):
    # given
    data = {"some": "request-data"}
    expected_response_data = transaction_session_response
    mock_request.return_value = expected_response_data
    plugin = webhook_plugin()

    webhook_app.identifier = "app.identifier"
    webhook_app.save()
    webhook_app.permissions.add(permission_manage_payments)
    webhook = Webhook.objects.create(
        name="Webhook",
        app=webhook_app,
        subscription_query=TRANSACTION_INITIALIZE_SESSION,
    )
    event_type = WebhookEventSyncType.TRANSACTION_INITIALIZE_SESSION
    webhook.events.create(event_type=event_type)
    amount = Decimal("10.00")

    transaction = transaction_item_generator(
        checkout_id=checkout.pk,
        app=webhook_app,
        psp_reference=None,
        name=None,
        message=None,
    )
    action_type = TransactionFlowStrategy.CHARGE
    idempotency_key = str(uuid.uuid4())

    # when
    response = plugin.transaction_initialize_session(
        transaction_session_data=TransactionSessionData(
            transaction=transaction,
            source_object=checkout,
            action=TransactionProcessActionData(
                amount=amount,
                currency=transaction.currency,
                action_type=action_type,
            ),
            customer_ip_address="127.0.0.1",
            payment_gateway_data=PaymentGatewayData(
                app_identifier=webhook_app.identifier, data=data, error=None
            ),
            idempotency_key=idempotency_key,
        ),
        previous_value=None,
    )

    # then
    _assert_with_subscription(
        checkout,
        transaction,
        data,
        amount,
        action_type,
        webhook,
        expected_response_data,
        response,
        mock_request,
        idempotency_key,
    )


@freeze_time()
@mock.patch("saleor.webhook.transport.synchronous.transport.send_webhook_request_sync")
def test_transaction_initialize_session_skips_app_without_identifier(
    mock_request,
    webhook_plugin,
    webhook_app,
    checkout,
    permission_manage_payments,
    transaction_item_generator,
    transaction_session_response,
):
    # given
    data = {"some": "request-data"}
    expected_response_data = transaction_session_response.copy()
    mock_request.return_value = expected_response_data
    plugin = webhook_plugin()

    webhook_app.identifier = ""
    webhook_app.save()
    webhook_app.permissions.add(permission_manage_payments)
    webhook = Webhook.objects.create(
        name="Webhook",
        app=webhook_app,
        subscription_query=TRANSACTION_INITIALIZE_SESSION,
    )
    event_type = WebhookEventSyncType.TRANSACTION_INITIALIZE_SESSION
    webhook.events.create(event_type=event_type)
    amount = Decimal("10.00")

    transaction = transaction_item_generator(
        checkout_id=checkout.pk,
        app=webhook_app,
        psp_reference=None,
        name=None,
        message=None,
    )
    action_type = TransactionFlowStrategy.CHARGE

    # when
    response = plugin.transaction_initialize_session(
        transaction_session_data=TransactionSessionData(
            transaction=transaction,
            source_object=checkout,
            action=TransactionProcessActionData(
                amount=amount,
                currency=transaction.currency,
                action_type=action_type,
            ),
            customer_ip_address="127.0.0.1",
            payment_gateway_data=PaymentGatewayData(
                app_identifier=webhook_app.identifier, data=data, error=None
            ),
        ),
        previous_value=None,
    )

    # then
    assert not EventPayload.objects.first()
    assert not EventDelivery.objects.first()
    assert not mock_request.called
    assert response == TransactionSessionResult(
        app_identifier="", response=None, error="Missing app identifier"
    )


@freeze_time()
@mock.patch("saleor.webhook.transport.synchronous.transport.send_webhook_request_sync")
def test_transaction_initialize_order_without_request_data_and_static_payload(
    mock_request,
    webhook_plugin,
    webhook_app,
    order,
    permission_manage_payments,
    transaction_session_response,
    transaction_item_generator,
):
    # given
    expected_response_data = transaction_session_response
    mock_request.return_value = expected_response_data
    plugin = webhook_plugin()

    webhook_app.identifier = "app.identifier"
    webhook_app.save()
    webhook_app.permissions.add(permission_manage_payments)
    webhook = Webhook.objects.create(
        name="Webhook",
        app=webhook_app,
    )
    event_type = WebhookEventSyncType.TRANSACTION_INITIALIZE_SESSION
    webhook.events.create(event_type=event_type)
    amount = Decimal("10.00")

    transaction = transaction_item_generator(
        order_id=order.pk,
        app=webhook_app,
        psp_reference=None,
        name=None,
        message=None,
    )
    action_type = TransactionFlowStrategy.CHARGE

    # when
    response = plugin.transaction_initialize_session(
        transaction_session_data=TransactionSessionData(
            transaction=transaction,
            source_object=order,
            action=TransactionProcessActionData(
                amount=amount,
                currency=transaction.currency,
                action_type=action_type,
            ),
            customer_ip_address="127.0.0.1",
            payment_gateway_data=PaymentGatewayData(
                app_identifier=webhook_app.identifier, data=None, error=None
            ),
        ),
        previous_value=None,
    )

    # then
    _assert_with_static_payload(
        order,
        transaction,
        None,
        amount,
        action_type,
        webhook,
        expected_response_data,
        response,
        mock_request,
    )


@freeze_time()
@mock.patch("saleor.webhook.transport.synchronous.transport.send_webhook_request_sync")
def test_transaction_initialize_order_with_request_data_and_static_payload(
    mock_request,
    webhook_plugin,
    webhook_app,
    order,
    permission_manage_payments,
    transaction_session_response,
    transaction_item_generator,
):
    # given
    data = {"some": "request-data"}
    expected_response_data = transaction_session_response
    mock_request.return_value = expected_response_data
    plugin = webhook_plugin()

    webhook_app.identifier = "app.identifier"
    webhook_app.save()
    webhook_app.permissions.add(permission_manage_payments)
    webhook = Webhook.objects.create(
        name="Webhook",
        app=webhook_app,
    )
    event_type = WebhookEventSyncType.TRANSACTION_INITIALIZE_SESSION
    webhook.events.create(event_type=event_type)
    amount = Decimal("10.00")

    transaction = transaction_item_generator(
        order_id=order.pk,
        app=webhook_app,
        psp_reference=None,
        name=None,
        message=None,
    )
    action_type = TransactionFlowStrategy.CHARGE

    # when
    response = plugin.transaction_initialize_session(
        transaction_session_data=TransactionSessionData(
            transaction=transaction,
            source_object=order,
            action=TransactionProcessActionData(
                amount=amount,
                currency=transaction.currency,
                action_type=action_type,
            ),
            customer_ip_address="127.0.0.1",
            payment_gateway_data=PaymentGatewayData(
                app_identifier=webhook_app.identifier, data=data, error=None
            ),
        ),
        previous_value=None,
    )

    # then
    _assert_with_static_payload(
        order,
        transaction,
        data,
        amount,
        action_type,
        webhook,
        expected_response_data,
        response,
        mock_request,
    )


@freeze_time()
@mock.patch("saleor.webhook.transport.synchronous.transport.send_webhook_request_sync")
def test_transaction_initialize_order_without_request_data(
    mock_request,
    webhook_plugin,
    webhook_app,
    order,
    permission_manage_payments,
    transaction_session_response,
    transaction_item_generator,
):
    # given
    expected_response_data = transaction_session_response
    mock_request.return_value = expected_response_data
    plugin = webhook_plugin()

    webhook_app.identifier = "app.identifier"
    webhook_app.save()
    webhook_app.permissions.add(permission_manage_payments)
    webhook = Webhook.objects.create(
        name="Webhook",
        app=webhook_app,
        subscription_query=TRANSACTION_INITIALIZE_SESSION,
    )
    event_type = WebhookEventSyncType.TRANSACTION_INITIALIZE_SESSION
    webhook.events.create(event_type=event_type)
    amount = Decimal("10.00")

    transaction = transaction_item_generator(
        order_id=order.pk,
        app=webhook_app,
        psp_reference=None,
        name=None,
        message=None,
    )
    action_type = TransactionFlowStrategy.CHARGE
    idempotency_key = str(uuid.uuid4())

    # when
    response = plugin.transaction_initialize_session(
        transaction_session_data=TransactionSessionData(
            transaction=transaction,
            source_object=order,
            action=TransactionProcessActionData(
                amount=amount,
                currency=transaction.currency,
                action_type=action_type,
            ),
            customer_ip_address="127.0.0.1",
            payment_gateway_data=PaymentGatewayData(
                app_identifier=webhook_app.identifier, data=None, error=None
            ),
            idempotency_key=idempotency_key,
        ),
        previous_value=None,
    )

    # then
    _assert_with_subscription(
        order,
        transaction,
        None,
        amount,
        action_type,
        webhook,
        expected_response_data,
        response,
        mock_request,
        idempotency_key,
    )


@freeze_time()
@mock.patch("saleor.webhook.transport.synchronous.transport.send_webhook_request_sync")
def test_transaction_initialize_order_with_request_data(
    mock_request,
    webhook_plugin,
    webhook_app,
    order,
    permission_manage_payments,
    transaction_session_response,
    transaction_item_generator,
):
    # given
    data = {"some": "request-data"}
    expected_response_data = transaction_session_response
    mock_request.return_value = expected_response_data
    plugin = webhook_plugin()

    webhook_app.identifier = "app.identifier"
    webhook_app.save()
    webhook_app.permissions.add(permission_manage_payments)
    webhook = Webhook.objects.create(
        name="Webhook",
        app=webhook_app,
        subscription_query=TRANSACTION_INITIALIZE_SESSION,
    )
    event_type = WebhookEventSyncType.TRANSACTION_INITIALIZE_SESSION
    webhook.events.create(event_type=event_type)
    amount = Decimal("10.00")

    transaction = transaction_item_generator(
        order_id=order.pk,
        app=webhook_app,
        psp_reference=None,
        name=None,
        message=None,
    )
    action_type = TransactionFlowStrategy.CHARGE
    idempotency_key = str(uuid.uuid4())

    # when
    response = plugin.transaction_initialize_session(
        transaction_session_data=TransactionSessionData(
            transaction=transaction,
            source_object=order,
            action=TransactionProcessActionData(
                amount=amount,
                currency=transaction.currency,
                action_type=action_type,
            ),
            customer_ip_address="127.0.0.1",
            payment_gateway_data=PaymentGatewayData(
                app_identifier=webhook_app.identifier, data=data, error=None
            ),
            idempotency_key=idempotency_key,
        ),
        previous_value=None,
    )

    # then
    _assert_with_subscription(
        order,
        transaction,
        data,
        amount,
        action_type,
        webhook,
        expected_response_data,
        response,
        mock_request,
        idempotency_key,
    )
