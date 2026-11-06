# Release evidence checklist

Unfilled template. Every applicable item needs evidence, environment and an owner. Use PASS / FAIL / BLOCKED / UNTESTED / accepted NOT-APPLICABLE; unchecked boxes do not mean passed. Severity exceptions and scope changes must be explicit.

## Scope and fidelity

- [ ] Frozen target/build and requirement baseline recorded; mandatory denominator stated.
- [ ] Roles, tenants, plans, routes, actions, states and integrations covered.
- [ ] Every requirement links to evidence/spec, implementation, acceptance test and result.
- [ ] Visual, behavioral, API/data, operational and applicable model fidelity reported separately.
- [ ] Known differences, inaccessible areas and unobserved behavior listed.
- [ ] Material hidden-behavior hypotheses tested with controlled experiments and counterexamples; surviving ambiguity recorded.
- [ ] Applicable limitation-register rows have closure evidence or block the corresponding claim.
- [ ] Required oracles and collectors/adapters independently validated; fixture resets and normalization preconditions checked.
- [ ] Seeded errors or relevant mutation testing demonstrate test sensitivity; history and temporal coverage match the claim.
- [ ] Formal/state-learning claims disclose assumptions, bounds, unresolved outcomes and approximation limits.
- [ ] Enhancements distinguished from reference fidelity.
- [ ] Source/assets/data/model provenance and applicable notices retained.

## Product behavior

- [ ] Real critical journeys pass end-to-end, including durable side effects.
- [ ] Empty/loading/error/permission/expiry/partial states work.
- [ ] Retries, duplicate actions, concurrency, cancellation and timeout behavior verified.
- [ ] Imports/exports, search, notifications, admin/support controls and destructive actions checked where applicable.
- [ ] Real sandbox integrations tested; mock limitations explicit.
- [ ] Applicable mobile permissions, lifecycle, deep links, push, offline/reconnect and real-device cases checked.
- [ ] Rendered viewport/device states and keyboard/focus/accessibility checked.

## Security, privacy and money

- [ ] API/job/search/export/storage/realtime tenant boundaries tested negatively.
- [ ] Session revocation, role changes and required enterprise identity verified.
- [ ] Secrets, dependencies, code/config and shipped artifacts reviewed/scanned appropriately.
- [ ] Sensitive inputs/captures/model logs redacted and data handling verified.
- [ ] Webhook signatures, replay and duplicate/out-of-order behavior checked.
- [ ] Billing/entitlements and recovery/reconciliation checked where applicable.
- [ ] Retention, export, deletion and audit behavior validated.

## Operations

- [ ] Named workload/dataset/environment meets measured latency, error and cost budgets.
- [ ] External limits, timeouts, backpressure and graceful degradation exercised.
- [ ] Logs/metrics/traces correlate failures without exposing secrets.
- [ ] Alerts tested and ownership/escalation established.
- [ ] Backup restore rehearsed and recovery objectives measured.
- [ ] Migration rehearsal, data reconciliation and rollback/roll-forward limits recorded.
- [ ] Environment isolation, infrastructure configuration and secret scopes verified.
- [ ] Build/dependency identities, deployment result and intended-environment smoke evidence retained.

## AI/video additions

- [ ] Model/config/data identity and holdout quality/variation documented.
- [ ] Any optional model/tool combination meets evaluated task-class thresholds; no automatic routing is required.
- [ ] Tool/API failure and abstention/escalation cases tested.
- [ ] Video/audio outputs have complete replacement and provenance manifests.
- [ ] No unauthorized reference-only footage/audio remains in independent reconstructions.
- [ ] Fresh decoding/evaluation performed after extraction or preprocessing changes.

## Handoff

- [ ] Commands and artifacts are reproducible by the next owner.
- [ ] Local/staging/production proof clearly distinguished.
- [ ] Open blockers/unknowns and next required actions listed.
- [ ] No unsupported claims of universal equivalence, perfection or production readiness.
