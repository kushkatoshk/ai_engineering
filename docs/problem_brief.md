# Problem brief: Apparel Support Copilot

**Version:** 0.1 (week 1). Numbers are assumptions until checked; see below.

## Problem

An apparel brand's support team handles about 50,000 tickets a month at roughly 6 minutes each: about 5,000 agent hours, or $125,000 a month at $25 an hour. Around a third of tickets are routine questions (order status, shipping times, return policy) with predictable answers. Counting confirmable actions too (returns, exchanges, cancellations), roughly half of all tickets could be handled without a person.

## What we'll build

A system that reads each incoming ticket, classifies its intent, and takes one of three paths based on the intent and the model's confidence. Low confidence on any intent sends the ticket to a human.

| Path | What happens | Intents |
| --- | --- | --- |
| **Auto resolve** (15) | The bot answers or acts with no human involved | track_order, track_refund, delivery_period, delivery_options, check_refund_policy, check_payment_methods, check_cancellation_fee, check_invoice, get_invoice, contact_customer_service, recover_password, newsletter_subscription, create_account, sizing_question, stock_availability |
| **Resolve after confirmation** (11) | The bot proposes the action and acts only after the customer confirms | cancel_order, change_order, place_order, change_shipping_address, set_up_shipping_address, edit_account, switch_account, registration_problems, review, start_return, start_exchange |
| **Human** (7) | Always routed to an agent | get_refund, payment_issue, delete_account, complaint, contact_human_agent, product_issue, other |

**How the groups were decided:** informational intents (the bot replies with facts) are cheap to get wrong, so they're automated. Actions that can be reversed if caught get a confirmation step. Anything involving money, legal obligations (account deletion is a CCPA request), irreversible changes, or an upset customer goes to a human.

**Special cases:**
- `sizing_question` answers only from the brand's size guide and says so when a product has no size data. A wrong answer causes a return (about $15), which costs more than a human ticket.
- `edit_account` requires identity verification before changing an email address (account takeover risk).

**Overrides (apply regardless of predicted intent):**
- Escalation keywords (lawyer, attorney, lawsuit, chargeback, BBB, fraud) go straight to a senior agent.
- Messages saying self service already failed ("never came", "didn't work", "already tried") go to a human.

## Success metrics

- **Primary:** at least 33% of tickets resolved with no human involved (auto resolved plus confirmed).
- **Guardrails:**
  - Error rate on automated tickets under 3%.
  - Zero automated actions on refunds, payment issues, account deletions, product issues, or complaints.
  - Customer satisfaction on automated tickets no lower than on human handled ones.

## Out of scope (for now)

Issuing refunds automatically, non-English tickets, voice and phone support.

## Assumptions to verify

| Assumption | Value used | How we'll check | When |
| --- | --- | --- | --- |
| Monthly ticket volume | 50,000 | Industry benchmarks, or real data if available | Week 5 |
| Average handle time | 6 minutes | Industry benchmarks | Week 5 |
| Fully loaded agent cost | $25/hour | Industry benchmarks | Week 5 |
| Share of tickets that are routine or confirmable | ~50% | Intent distribution on real or realistic tickets | Week 2 |
| Cost of one automated mistake | ~$20 | Error cost table by intent | Week 5 |

## Decision log

| Date | Decision | Why |
| --- | --- | --- |
| 2026-10-27 | One primary intent per ticket, not multi label | Routing needs one label; the reply generator reads the full message and can answer secondary questions |
| 2026-10-27 | Added start_return, start_exchange, sizing_question, stock_availability, product_issue, other | Bitext is generic e-commerce and has no returns, exchanges, fit, stock, or defect intents |
| 2026-10-27 | Returns and exchanges in scope, with confirmation | High volume in apparel and reversible if wrong; needed to reach the 33% target |
| 2026-10-27 | sizing_question automated only from the size guide | Informational, but a wrong answer causes a costly return |
