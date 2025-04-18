from enum import Enum


class CheckoutErrorCode(Enum):
    BILLING_ADDRESS_NOT_SET = "billing_address_not_set"
    CHECKOUT_NOT_FULLY_PAID = "checkout_not_fully_paid"
    GRAPHQL_ERROR = "graphql_error"
    PRODUCT_NOT_PUBLISHED = "product_not_published"
    PRODUCT_UNAVAILABLE_FOR_PURCHASE = "product_unavailable_for_purchase"
    INSUFFICIENT_STOCK = "insufficient_stock"
    INVALID = "invalid"
    INVALID_SHIPPING_METHOD = "invalid_shipping_method"
    NOT_FOUND = "not_found"
    PAYMENT_ERROR = "payment_error"
    QUANTITY_GREATER_THAN_LIMIT = "quantity_greater_than_limit"
    REQUIRED = "required"
    SHIPPING_ADDRESS_NOT_SET = "shipping_address_not_set"
    SHIPPING_METHOD_NOT_APPLICABLE = "shipping_method_not_applicable"
    DELIVERY_METHOD_NOT_APPLICABLE = "delivery_method_not_applicable"
    SHIPPING_METHOD_NOT_SET = "shipping_method_not_set"
    SHIPPING_NOT_REQUIRED = "shipping_not_required"
    TAX_ERROR = "tax_error"
    UNIQUE = "unique"
    VOUCHER_NOT_APPLICABLE = "voucher_not_applicable"
    GIFT_CARD_NOT_APPLICABLE = "gift_card_not_applicable"
    ZERO_QUANTITY = "zero_quantity"
    MISSING_CHANNEL_SLUG = "missing_channel_slug"
    CHANNEL_INACTIVE = "channel_inactive"
    UNAVAILABLE_VARIANT_IN_CHANNEL = "unavailable_variant_in_channel"
    EMAIL_NOT_SET = "email_not_set"
    NO_LINES = "no_lines"
    INACTIVE_PAYMENT = "inactive_payment"
    NON_EDITABLE_GIFT_LINE = "non_editable_gift_line"
    NON_REMOVABLE_GIFT_LINE = "non_removable_gift_line"
    SHIPPING_CHANGE_FORBIDDEN = "shipping_change_forbidden"


class OrderCreateFromCheckoutErrorCode(Enum):
    GRAPHQL_ERROR = "graphql_error"
    CHECKOUT_NOT_FOUND = "checkout_not_found"
    CHANNEL_INACTIVE = "channel_inactive"
    INSUFFICIENT_STOCK = "insufficient_stock"
    VOUCHER_NOT_APPLICABLE = "voucher_not_applicable"
    GIFT_CARD_NOT_APPLICABLE = "gift_card_not_applicable"
    TAX_ERROR = "tax_error"
    SHIPPING_METHOD_NOT_SET = "shipping_method_not_set"
    BILLING_ADDRESS_NOT_SET = "billing_address_not_set"
    SHIPPING_ADDRESS_NOT_SET = "shipping_address_not_set"
    INVALID_SHIPPING_METHOD = "invalid_shipping_method"
    NO_LINES = "no_lines"
    EMAIL_NOT_SET = "email_not_set"
    UNAVAILABLE_VARIANT_IN_CHANNEL = "unavailable_variant_in_channel"


class CheckoutCreateFromOrderErrorCode(Enum):
    GRAPHQL_ERROR = "graphql_error"
    INVALID = "invalid"
    ORDER_NOT_FOUND = "order_not_found"
    CHANNEL_INACTIVE = "channel_inactive"
    TAX_ERROR = "tax_error"


class CheckoutCreateFromOrderUnavailableVariantErrorCode(Enum):
    NOT_FOUND = "not_found"
    PRODUCT_UNAVAILABLE_FOR_PURCHASE = "product_unavailable_for_purchase"
    UNAVAILABLE_VARIANT_IN_CHANNEL = "unavailable_variant_in_channel"
    PRODUCT_NOT_PUBLISHED = "product_not_published"
    QUANTITY_GREATER_THAN_LIMIT = "quantity_greater_than_limit"
    INSUFFICIENT_STOCK = "insufficient_stock"
