import opentracing
import opentracing.tags
import stripe

from .... import TransactionKind
from ....interface import (
    CustomerSource,
    GatewayConfig,
    GatewayResponse,
    PaymentData,
    PaymentMethodInfo,
)
from .utils import (
    get_amount_for_stripe,
    get_amount_from_stripe,
    get_currency_for_stripe,
    get_currency_from_stripe,
    shipping_to_stripe_dict,
)


def get_client_token(**_):
    """Not implemented for stripe gateway currently.

    The client token can be generated by stripe.js automatically.
    """
    return


def authorize(
    payment_information: PaymentData, config: GatewayConfig
) -> GatewayResponse:
    kind = TransactionKind.CAPTURE if config.auto_capture else TransactionKind.AUTH
    client = _get_client(**config.connection_params)
    capture_method = "automatic" if config.auto_capture else "manual"
    currency = get_currency_for_stripe(payment_information.currency)
    stripe_amount = get_amount_for_stripe(payment_information.amount, currency)
    future_use = "off_session" if config.store_customer else "on_session"
    customer_id = PaymentData.customer_id if payment_information.reuse_source else None
    shipping = (
        shipping_to_stripe_dict(payment_information.shipping)
        if payment_information.shipping
        else None
    )

    try:
        with opentracing.global_tracer().start_active_span(
            "stripe.PaymentIntent.create"
        ) as scope:
            span = scope.span
            span.set_tag(opentracing.tags.COMPONENT, "payment")
            span.set_tag("service.name", "stripe")
            intent = client.PaymentIntent.create(
                payment_method=payment_information.token,
                amount=stripe_amount,
                currency=currency,
                confirmation_method="manual",
                confirm=True,
                capture_method=capture_method,
                setup_future_usage=future_use,
                customer=customer_id,
                shipping=shipping,
            )
        if config.store_customer and not customer_id:
            with opentracing.global_tracer().start_active_span(
                "stripe.Customer.create"
            ) as scope:
                span = scope.span
                span.set_tag(opentracing.tags.COMPONENT, "payment")
                span.set_tag("service.name", "stripe")
                customer = client.Customer.create(payment_method=intent.payment_method)
            customer_id = customer.id

    except stripe.error.StripeError as exc:
        response = _error_response(kind=kind, exc=exc, payment_info=payment_information)
    else:
        success = intent.status in ("succeeded", "requires_capture", "requires_action")
        response = _success_response(
            intent=intent, kind=kind, success=success, customer_id=customer_id
        )
        response = fill_card_details(intent, response)
    return response


def capture(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    client = _get_client(**config.connection_params)
    intent = None
    try:
        with opentracing.global_tracer().start_active_span(
            "stripe.PaymentIntent.retrieve"
        ) as scope:
            span = scope.span
            span.set_tag(opentracing.tags.COMPONENT, "payment")
            span.set_tag("service.name", "stripe")
            intent = client.PaymentIntent.retrieve(id=payment_information.token)
        capture = intent.capture()
    except stripe.error.StripeError as exc:
        action_required = intent.status == "requires_action" if intent else False
        response = _error_response(
            kind=TransactionKind.CAPTURE,
            exc=exc,
            payment_info=payment_information,
            action_required=action_required,
        )
    else:
        response = _success_response(
            intent=intent,
            kind=TransactionKind.CAPTURE,
            success=capture.status in ("succeeded", "requires_action"),
        )
        response = fill_card_details(intent, response)
    return response


def confirm(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    client = _get_client(**config.connection_params)
    try:
        intent = client.PaymentIntent(id=payment_information.token)
        with opentracing.global_tracer().start_active_span(
            "stripe.PaymentIntent.confirm"
        ) as scope:
            span = scope.span
            span.set_tag(opentracing.tags.COMPONENT, "payment")
            span.set_tag("service.name", "stripe")
            intent.confirm()
    except stripe.error.StripeError as exc:
        response = _error_response(
            kind=TransactionKind.CONFIRM, exc=exc, payment_info=payment_information
        )
    else:
        response = _success_response(
            intent=intent,
            kind=TransactionKind.CONFIRM,
            success=intent.status == "succeeded",
        )
        response = fill_card_details(intent, response)
    return response


def refund(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    client = _get_client(**config.connection_params)
    currency = get_currency_for_stripe(payment_information.currency)
    stripe_amount = get_amount_for_stripe(payment_information.amount, currency)
    try:
        with opentracing.global_tracer().start_active_span(
            "stripe.PaymentIntent.retrieve"
        ) as scope:
            span = scope.span
            span.set_tag(opentracing.tags.COMPONENT, "payment")
            span.set_tag("service.name", "stripe")
            intent = client.PaymentIntent.retrieve(id=payment_information.token)
        refund = intent["charges"]["data"][0].refund(amount=stripe_amount)
    except stripe.error.StripeError as exc:
        response = _error_response(
            kind=TransactionKind.REFUND, exc=exc, payment_info=payment_information
        )
    else:
        response = _success_response(
            intent=intent,
            kind=TransactionKind.REFUND,
            success=refund.status == "succeeded",
            amount=payment_information.amount,
            currency=get_currency_from_stripe(refund.currency),
        )
    return response


def void(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    client = _get_client(**config.connection_params)
    try:
        with opentracing.global_tracer().start_active_span(
            "stripe.PaymentIntent.retrieve"
        ) as scope:
            span = scope.span
            span.set_tag(opentracing.tags.COMPONENT, "payment")
            span.set_tag("service.name", "stripe")
            intent = client.PaymentIntent.retrieve(id=payment_information.token)
        refund = intent["charges"]["data"][0].refund()
    except stripe.error.StripeError as exc:
        response = _error_response(
            kind=TransactionKind.VOID, exc=exc, payment_info=payment_information
        )
    else:
        response = _success_response(
            intent=intent,
            kind=TransactionKind.VOID,
            currency=get_currency_from_stripe(refund.currency),
            raw_response=refund,
        )
    return response


def list_client_sources(
    config: GatewayConfig, customer_id: str
) -> list[CustomerSource]:
    client = _get_client(**config.connection_params)
    with opentracing.global_tracer().start_active_span(
        "stripe.PaymentMethod.list"
    ) as scope:
        span = scope.span
        span.set_tag(opentracing.tags.COMPONENT, "payment")
        span.set_tag("service.name", "stripe")
        cards = client.PaymentMethod.list(customer=customer_id, type="card")["data"]
    return [
        CustomerSource(
            id=c.id,
            gateway="stripe",
            credit_card_info=PaymentMethodInfo(
                exp_year=c.card.exp_year,
                exp_month=c.card.exp_month,
                last_4=c.card.last4,
                name=None,
            ),
        )
        for c in cards
    ]


def process_payment(
    payment_information: PaymentData, config: GatewayConfig
) -> GatewayResponse:
    return authorize(payment_information, config)


def _get_client(**connection_params):
    stripe.api_key = connection_params.get("private_key")
    return stripe


def _error_response(
    kind: str,  # use TransactionKind class
    exc: stripe.error.StripeError,
    payment_info: PaymentData,
    action_required: bool = False,
) -> GatewayResponse:
    return GatewayResponse(
        is_success=False,
        action_required=action_required,
        transaction_id=payment_info.token or "",
        amount=payment_info.amount,
        currency=payment_info.currency,
        error=exc.user_message,
        kind=kind,
        raw_response=exc.json_body or {},
        customer_id=payment_info.customer_id,
    )


def _success_response(
    intent: stripe.PaymentIntent,
    kind: str,  # use TransactionKind class
    success: bool = True,
    amount=None,
    currency=None,
    customer_id=None,
    raw_response=None,
):
    currency = currency or get_currency_from_stripe(intent.currency)
    return GatewayResponse(
        is_success=success,
        action_required=intent.status == "requires_action",
        transaction_id=intent.id,
        amount=amount or get_amount_from_stripe(intent.amount, currency),
        currency=currency,
        error=None,
        kind=kind,
        raw_response=raw_response or intent,
        customer_id=customer_id,
    )


def fill_card_details(intent: stripe.PaymentIntent, response: GatewayResponse):
    charges = intent.charges["data"]
    if charges:
        card = intent.charges["data"][-1]["payment_method_details"]["card"]
        brand = card["brand"] or ""

        response.payment_method_info = PaymentMethodInfo(
            last_4=card["last4"],
            exp_year=card["exp_year"],
            exp_month=card["exp_month"],
            brand=brand.lower(),
            type="card",
        )
    return response
