# Labeling guidelines

**Version:** 1.0 (2026-10-27)

Changing a definition can make existing labels wrong. Every change bumps the version and gets a changelog line, and every labeled row records the guideline version it was labeled under.

## General rules

1. **Label what the customer needs, not the words they use.** "I don't want a refund, I want a different size" is not get_refund.
2. **One label per message.** If a message has several intents, the action the customer needs taken beats a question. "Cancel my order, and what's your refund policy?" is cancel_order.
3. **Specific and existing means tracking; general means policy.** "Where's my refund?" is track_refund. "How long do refunds take?" is check_refund_policy.
4. **Whether the customer has the item decides the fit and stock cluster.** Before purchase: sizing_question or stock_availability. After receiving it: start_return, start_exchange, or product_issue.
5. **If nothing fits, use `other`.** Never force the closest intent; forcing teaches the model false patterns.
6. **Label the need even when self service already failed.** "My reset email never came" is still recover_password. Escalation is handled by separate rules, not by the label.

## Taxonomy (33 intents)

| Intent | The customer wants to... |
| --- | --- |
| **Orders** | |
| place_order | Buy something, or get help completing a purchase |
| cancel_order | Cancel an order that hasn't been delivered |
| change_order | Change an order before it ships (item, size, color, quantity) |
| track_order | Know where a specific existing order is |
| **Shipping** | |
| delivery_period | Know how long shipping generally takes |
| delivery_options | Know which shipping methods, speeds, or costs exist |
| set_up_shipping_address | Add a new address to their account |
| change_shipping_address | Change the address on their account or on an existing order |
| **Refunds** | |
| get_refund | Get money back without returning an item (never arrived, wrong charge, refund owed) |
| track_refund | Know the status of a refund already in progress |
| check_refund_policy | Know the general rules for refunds or returns |
| **Returns, fit and stock** | |
| start_return | Send back an item they received |
| start_exchange | Swap an item they received for a different size or color |
| sizing_question | Know whether an item will fit them, before buying |
| stock_availability | Know whether an item, color, or size is in stock or coming back |
| product_issue | Report a defect or damage in an item they received |
| **Payment and invoices** | |
| check_payment_methods | Know which payment methods are accepted |
| payment_issue | Fix a payment that failed, or a wrong or double charge |
| check_cancellation_fee | Know whether cancelling costs anything |
| check_invoice | See or ask about details of an existing invoice |
| get_invoice | Get a copy of an invoice |
| **Account** | |
| create_account | Open a new account |
| delete_account | Close their account and remove their data |
| edit_account | Change account details (name, email, phone) |
| switch_account | Move between accounts or change account type |
| recover_password | Regain access to their account |
| registration_problems | Fix a problem signing up |
| **Contact and feedback** | |
| contact_customer_service | Know how to reach support (hours, channels) |
| contact_human_agent | Talk to a person now |
| complaint | Have a problem with the service, a policy, or the company addressed |
| review | Share an opinion with no action needed |
| newsletter_subscription | Subscribe to or unsubscribe from marketing emails |
| **Other** | |
| other | None of the above |

## Confusable clusters

### Refunds and returns

Return policy questions go to check_refund_policy; there is no separate return policy intent.

| Message | Label | Why |
| --- | --- | --- |
| "I want to return these shorts and get my money back." | start_return | The item has to come back first; the refund follows |
| "My package never arrived, I want a refund." | get_refund | Money back with nothing to return |
| "I sent it back two weeks ago, where's my refund?" | track_refund | A specific refund already in progress |
| "What's your return policy on sale items?" | check_refund_policy | A general policy question |
| "Can I get a return label?" | start_return | Starting a return |

### Fit and stock

| Message | Label | Why |
| --- | --- | --- |
| "Doesn't fit." (nothing else) | start_return | Unclear whether they want a replacement, so default to return; the confirmation step can offer an exchange |
| "I bought an M and it's tight, can I get an L?" | start_exchange | Has the item and wants a different size |
| "I'm usually an M, should I get an L in this?" | sizing_question | Hasn't bought yet |
| "Can I swap for a medium? Is it in stock?" | start_exchange | The action beats the question (rule 2) |
| "When will the black XS be back?" | stock_availability | Asking about stock, no existing order involved |
| "Change my order to a medium, it hasn't shipped." | change_order | Before shipping is change_order; after receiving is start_exchange |
| "The seams came apart after one wash." | product_issue | A defect, not a fit problem |

### Orders and delivery

| Message | Label | Why |
| --- | --- | --- |
| "How long does shipping to Texas take?" | delivery_period | General question |
| "I ordered on the 3rd, where is it?" | track_order | A specific existing order |
| "How much longer, it's been a week." | track_order | Implies an existing order, even with no order number |
| "Do you have express shipping?" | delivery_options | Asking which methods exist |

### Feedback

| Message | Label | Why |
| --- | --- | --- |
| "Your customer service is useless, nobody replies." | complaint | Dissatisfied with the service, wants it addressed |
| "The zipper broke on my jacket." | product_issue | A specific defective item |
| "Love these leggings, great quality." | review | An opinion, no action needed |
| "These run small, wish I'd known." | review | Feedback with no request; if they ask to send it back, start_return |

### Contact

| Message | Label | Why |
| --- | --- | --- |
| "What are your support hours?" | contact_customer_service | Asking how to reach support |
| "Let me talk to a real person." | contact_human_agent | Wants a human now |

## Changelog

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-27 | First version: Bitext's 27 intents plus start_return, start_exchange, sizing_question, stock_availability, product_issue, and other; get_refund narrowed to refunds without a return |
