# GoHighLevel reconstruction: feasibility and gap-closing plan

Prepared 2026-11-06 from selected official public documentation. No authenticated GoHighLevel account, private code, complete endpoint/feature inventory, workflow replay, migration or load test was examined. This is a discovery and engineering plan, not a completed GoHighLevel audit or clone.

## What can and cannot be promised

A substantial independent product with measured GoHighLevel-like functionality can be engineered. “Every feature and every hidden behavior, perfectly identical” cannot be substantiated from public pages, APIs and screenshots alone. No REA/Ghidra plugin removes that information boundary. Native tools can inspect available client artifacts; they do not expose remote SaaS internals automatically.

There are three different goals: reproduce a visible interface; build compatible selected workflows/contracts; independently recreate the complete service portfolio. They require different evidence, resources and acceptance criteria. Decide which dimensions must match before implementation.

## Official-source facts that affect discovery

HighLevel describes snapshots as reusable configuration templates, with exclusions for live data and connections. A snapshot is therefore an input to discovery, not an export of the whole product or service implementation. Inspect the current asset/exclusion list for the actual snapshot used. [Official snapshot overview](https://help.gohighlevel.com/support/solutions/articles/48000982511-snapshots-overview).

The public API is access-controlled and rate-limited. Current documented default OAuth limits are 100 requests per 10 seconds and 200,000 per 24 hours per app/resource, with overrides and authoritative response headers. This constrains collection and sync; it does not describe a complete internal implementation. [Official rate limits](https://marketplace.gohighlevel.com/docs/other/rate-limits/index.html), [developer access setup](https://help.gohighlevel.com/support/solutions/articles/155000000136-how-to-get-started-with-the-developer-s-marketplace).

SaaS rebilling/wallets and account enablement are separate service behaviors that need their own accounting, authorization and reconciliation tests. They cannot be reduced to a pricing page or subscription button. [Official rebilling/wallet guide](https://help.gohighlevel.com/support/solutions/articles/155000002095), [SaaS API](https://marketplace.gohighlevel.com/docs/ghl/saas-api/saa-s/index.html).

## Candidate discovery inventory

These are areas to investigate and test, not claims of a complete current HighLevel feature catalog. Every row starts UNVERIFIED until the authorized reference account and current docs establish its applicability, versions and plan availability.

| Domain | Questions/requirements to resolve | Necessary proof |
|---|---|---|
| Agency/sub-account tenancy | Ownership, provisioning, membership, impersonation/support access | Cross-tenant negative cases and lifecycle tests |
| Users/roles/authentication | Sessions, invitations, revocation, MFA/SSO if applicable | Role-by-action contract and denied-access evidence |
| CRM records | Contacts, custom fields/objects, tags, relationships, deduplication | Data invariants, import/export and merge corpus |
| Opportunities/pipelines | Stages, automation effects, assignment and reporting | State-transition and concurrency replay |
| Conversations | Channels, threads, assignment, unread state and search | Message ordering and side-effect comparison |
| Voice/SMS | Provisioning, routing, recording, status callbacks and consent states | Provider sandbox/device evidence and reconciliation |
| Email | Sending identities, domain configuration, bounce/suppression and tracking | Actual test messages/events; delivery limits stated |
| WhatsApp/social messaging | Account connections, approved capabilities and event handling | Separate provider integration tests |
| Calendars/appointments | Availability, timezones/DST, staff/resources, conflict handling | Concurrent booking and reschedule/cancel corpus |
| Workflow builder/runtime | Trigger/action catalog, branches, waits, re-entry, versions, retries | Event histories and timer/failure/replay tests |
| Campaigns/broadcasts | Audience definition, scheduling, deduplication, opt-outs | Safe sandbox send and recipient accounting |
| Website/funnel builders | Components, responsive behavior, publishing, forms and domains | Editor/runtime parity and published journey evidence |
| Forms/surveys/quizzes | Validation, conditional logic, embedding and attribution | Malformed/partial submission corpus |
| Payments/commerce | Checkout, subscriptions, invoices, refunds, documents and taxes if applicable | Provider sandbox ledger and webhook reconciliation |
| SaaS/white label | Plans, entitlements, wallet/rebilling, provisioning and suspension | Accounting invariants and lifecycle tests |
| Reporting/attribution | Definitions, event sources, filters, timezone and eventual consistency | Fixed datasets with reconciled totals |
| Reputation | Requests, review sources, responses and external synchronization | Allowed-provider contracts and rate/failure behavior |
| Courses/memberships/community | Content, enrollment, access, progress and communications | Entitlement and lifecycle checks |
| AI/voice/conversation features | Prompting, retrieval, tools, quality, latency and cost | Licensed accessible pipeline or evaluated substitute |
| Snapshots/templates | Supported assets, versions, dependencies, merge/update conflicts | Round-trip configuration comparison; exclusions documented |
| Marketplace/API/webhooks | Auth scopes, install/uninstall, errors, quotas and event coverage | Versioned contract/replay fixtures |
| Mobile/white-label clients | Device lifecycle, push, deep links and platform integrations | Real-device/platform testing and signing readiness |
| Admin/support/operations | Audit, exports/deletion, monitoring, restore and incident workflows | Operating drills, ownership and environment proof |

The inventory must expand when discovery finds another domain, plan, experiment, country, role or lifecycle state. It is not acceptable to call the product complete because every row above has a UI.

## What tools close which gaps

Use Playwright for observed journeys and rendered comparisons, REA for available bundles/captures, and Ghidra only for a relevant accessible native artifact. Use typed contracts and property/fuzz tests for data/API semantics, a durable workflow engine for timers/retries/replay, and hosted PostgreSQL for independently designed durable state. See [TOOLCHAIN](TOOLCHAIN.md).

Communications, payments, external account connections, domain provisioning and delivery infrastructure need actual providers, test identities, credentials, configuration, operating budgets and failure tests. A framework cannot manufacture a provider agreement, historical sending reputation or missing private data. Similar service classes may be substituted, but differences must be disclosed and measured.

Model-backed features need a defined behavioral quality target. Accessible weights/configuration permit artifact-based work; inaccessible models require an evaluated substitute. Do not claim identical model internals or outputs.

## Highest-risk pilot

Prove one complete lead-to-appointment journey: isolated agency/sub-account, lead form, deduplicated contact, pipeline update, durable workflow, authorized sandbox message, booking, cancellation, audit trail and usage accounting. Inject duplicate/out-of-order events, delivery failure, worker restart, opt-out, revoked user, timezone/DST edge cases and tenant-boundary attempts.

This is an engineering prioritization example, not a complete acceptance suite. It should expose architectural and integration problems before building dozens of superficial screens.

## Closure requirements before a completeness claim

- An authorized access matrix for applicable agency, sub-account, plan, role, device and region states.
- A frozen reference date/version and source-backed feature/contract inventory with discovery blind spots.
- A requirement-level gap ledger with evidence, owner, method, dependency and closure result.
- Real integration/provider proof and data reconciliation, not mocks presented as completion.
- Differential tests across normal, edge, malformed, retry, concurrency and lifecycle scenarios.
- Measured performance, recovery, operational ownership and ongoing drift detection.
- Explicit substitute behavior and inaccessible internals that prevent stronger claims.

No account access or the above proof was supplied during preparation of this repository. Therefore the honest present status is **planning/discovery reference; GoHighLevel fidelity unverified**. Use [LIMITATIONS-AND-CLOSURE](LIMITATIONS-AND-CLOSURE.md) and the target-specific gap register to execute the work rather than assuming the library itself closes it.
