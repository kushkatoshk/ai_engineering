"""The intent taxonomy: the single list of allowed intents.

Must match docs/labeling_guidelines.md. When you change this list, bump
GUIDELINE_VERSION and add a line to the guidelines changelog.
"""

GUIDELINE_VERSION = "1.0"

INTENTS: tuple[str, ...] = (
    # Orders
    "place_order",
    "cancel_order",
    "change_order",
    "track_order",
    # Shipping
    "delivery_period",
    "delivery_options",
    "set_up_shipping_address",
    "change_shipping_address",
    # Refunds
    "get_refund",
    "track_refund",
    "check_refund_policy",
    # Returns, fit and stock (apparel additions, not in Bitext)
    "start_return",
    "start_exchange",
    "sizing_question",
    "stock_availability",
    "product_issue",
    # Payment and invoices
    "check_payment_methods",
    "payment_issue",
    "check_cancellation_fee",
    "check_invoice",
    "get_invoice",
    # Account
    "create_account",
    "delete_account",
    "edit_account",
    "switch_account",
    "recover_password",
    "registration_problems",
    # Contact and feedback
    "contact_customer_service",
    "contact_human_agent",
    "complaint",
    "review",
    "newsletter_subscription",
    # Fallback
    "other",
)
