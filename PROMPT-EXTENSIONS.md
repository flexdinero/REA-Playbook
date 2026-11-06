# Specialist prompt extensions

Use one packet at a time with MASTER-PROMPT and requirement/evidence IDs. These are original task prompts extending the combined operating process, not copies of upstream prompts. Each should yield an artifact and explicit PASS/FAIL/BLOCKED/UNTESTED findings where applicable.

## 1. Hidden feature and state discovery

> Map the target across roles, tenants, subscription tiers, settings, entry points and feature flags. Discover screens, actions and transitions, including empty, loading, permission, expiry, error and offline states. Cite what was observed. Separate absent, inaccessible and unknown behavior. Produce a route/state/action register and the next highest-value discovery tests.

## 2. Backend behavior from observable contracts

> From authorized traffic and UI outcomes, specify request/response/error contracts, pagination, sorting, validation, time handling and durable side effects for these requirement IDs. Propose a backend only where internals are unknown. Build independent compatibility tests with normal, boundary, duplicate and malformed inputs. Never label a proposed schema recovered.

## 3. Tenancy and authorization

> Map identities, sessions, memberships, roles and resource ownership. Define deny-by-default checks at API, job, export, search, storage and realtime boundaries. Test user A versus user B, two tenants, revoked membership and forged object IDs. Prove denial using responses and data-side effects; hiding a UI control is insufficient.

## 4. Billing and entitlements

> Specify plans, trials, seat changes, quotas, proration, cancellation, refunds, grace periods and entitlement transitions applicable to this product. Test webhook signature validation, replay, duplicate/out-of-order delivery and provider downtime. Separate provider payment status from product access. Produce a reconciliation test and support recovery procedure.

## 5. Durable automations and agent services

> Model triggers, schedules, timezone/DST, retries, cancellation, approval waits and external side effects. Define idempotency keys and compensating actions. Inject worker crashes and duplicate events. Show which steps can replay and which require reconciliation. Do not claim exactly-once external effects without evidence from the endpoint semantics.

## 6. Data migration and recovery

> Inventory schemas, relationships, encodings, timezone/precision rules, large objects and retention constraints. Define migration invariants, compatibility window and rollback limits. Rehearse on representative data, reconcile counts and business totals, and restore an actual backup into a separate recovery environment. Record measured recovery objectives and untested cases.

## 7. Mobile platform fidelity

> Test the applicable device/OS matrix: lifecycle, permissions, keyboard/safe areas, deep links, push, background jobs, offline sync, reconnect conflicts, camera/files and accessibility. Separate emulator, simulator and real-device proof. Record native-service, signing and store-delivery prerequisites that remain unavailable.

## 8. Visual and interaction fidelity

> Compare the same reference and implementation states with matched fonts, data, viewport, device scale and animation time. Inventory typography, spacing, layout, focus, hover, touch, motion and responsive changes. Define dynamic masks with reasons. Pair visual diffs with working actions, keyboard navigation and persisted results. Preserve a separate enhancement backlog.

## 9. ML/AI product reproduction

> Inventory model/tokenizer versions, templates, preprocessing, retrieval corpus/indexing, tools, sampling, postprocessing and safety/business rules visible in the authorized inputs. Distinguish exact accessible artifacts from substitutes. Build a labeled holdout spanning ordinary, adversarial, long-context, abstention and tool-failure cases. Report task quality, variation, latency, cost and data access limits; do not promise identical hosted-model outputs.

## 10. Video, motion and audio reconstruction

> Preserve original-file metadata and create a shot/layer timeline with timecodes, camera/motion, text, overlays, audio stems and evidence uncertainty. Treat production method as a hypothesis unless production records establish it. For every output segment declare generated, independently recreated, licensed reuse, reference-only or missing. Prevent original-footage/audio fallback in a deliverable claiming independent reconstruction. Compare duration, sync, content and all replacement layers.

## 11. File formats, protocols and plugin ABI

> Specify observed versions, layouts, encoding, alignment, endianness, handshake/state, errors and compatibility limits. Separate static declarations from exercised behavior. Build a minimal independent implementation and interoperability corpus. Include unknown fields and version skew. Use property/fuzz tests and report every divergence by requirement and artifact identity.

## 12. Native algorithm ambiguity

> For this function/question, compare pseudocode with instructions, types, calls and observed inputs/outputs. State competing interpretations and find the cheapest counterexample. Account for integer width, sign, overflow, floating-point rules, ABI and aliasing. Return an independently implemented candidate with differential results and unresolved assumptions.

## 13. Scale and resilience

> Convert the target workload into dataset size, concurrent activity, request mix, job rates and third-party limits. Define latency/error/cost budgets. Measure saturation and inject dependency/worker/network failure in a controlled environment. Show recovery, backpressure and degraded UX. Do not infer capacity from framework choice or a short single-user test.

## 14. Adoption review

> Evaluate this candidate from the reference index against a specific missing capability. Check canonical origin, exact release/SHA, license, host/runtime, maintenance, advisories, required permissions, data egress and dependency footprint. Run the smallest harmless fixture that proves the intended integration. Return adopt, trial, reject or blocked with evidence and a removal path.

## 15. Release adversarial review

> Review the frozen scope against evidence and code. Seek omitted roles, transitions, side effects, admin/support flows, destructive actions, cross-tenant access, integration failures and recovery gaps. Reject fabricated verification, mocks presented as working integrations, copied reference content presented as recreated, and metrics without measured conditions. Return concrete findings and release blockers, not a reassuring summary.

## 16. Resume without losing evidence

> Read the target brief, requirement matrix, decisions, current gaps and last evidence index. Verify repository/build identity before resuming. List completed proof, unresolved hypotheses and the next bounded task. Reuse immutable evidence where valid; recollect when target version or extraction settings changed. Do not restart investigation solely because conversation context changed.
