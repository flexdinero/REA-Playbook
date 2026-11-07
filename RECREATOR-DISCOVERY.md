# Find missing links before reconstructing them

The recreator must investigate omissions, not just implement the backlog it was
given. A missing-link investigation starts with an observable clue, explains why
something else may need to exist, and seeks an observation that could disprove
that explanation. A plausible dependency is a question, not recovered source.

## Build an evidence graph

Use the [executable graph audit](RECREATOR-GRAPH.md) and
[starting graph](templates/DISCOVERY-GRAPH.json) to check supplied evidence,
missing declared links and unsupported closure claims. The auditor does not
populate the product inventory automatically.

Maintain nodes for user outcomes, capabilities, UI states/actions, API operations,
entities, permissions, events/jobs, external providers, entitlements/metering,
deployment components and evidence. Connect them with typed edges: invokes,
reads, writes, schedules, authorizes, emits, consumes, bills, displays, depends-on,
supports and contradicts. Give each node/edge a stable ID, scope/version/date,
source location, evidence classification and unresolved questions. Distinguish
an observed edge from a dependency inferred from necessary behavior.

Trace critical outcomes end to end. Example: a scheduled campaign can involve
contact selection, suppression, enrollment, durable scheduling, permission checks,
provider submission, acknowledgements, delivery events, retries/reconciliation,
usage accounting and reporting. This is an investigation checklist. The actual
product may combine components or implement different semantics.

Look for unexplained edges and orphan nodes: a UI action without a known outcome,
a request without a mapped caller, an entity without a lifecycle, an event without
a consumer, a billable action without an accounting explanation, a permission
without tests, or a dependency with no failure behavior. Some orphans are valid
boundaries, obsolete code or inaccessible features. Resolve their meaning rather
than treating every orphan as a feature to invent.

## Clue families and discriminating observations

| Clue source | What it may reveal | Next useful investigation |
|---|---|---|
| Navigation, dialogs, disabled controls, validation, empty/error states | Undiscovered capabilities and prerequisites | Compare permitted states, document the enabling conditions and follow the actual action |
| Network initiators, response fields, error codes, pagination, IDs, headers | Client/server boundaries and operation dependencies | Link action to request and response; trace returned IDs into later reads/events |
| WebSocket/SSE messages, polling, status transitions, callbacks | Asynchronous completion and background work | Retain ordered histories; compare a second client and permitted closed-client observations |
| Available client bundles, schemas, exports, native artifacts, source maps | Routes, enum variants, serializers, migrations, provider contracts | Corroborate code paths at runtime; dormant or obsolete code is not active behavior |
| Stored entities, foreign keys, defaults, timestamps, tombstones | Ownership and creation/update/deletion lifecycles | Trace each critical field from input to persistence to reads, export and deletion |
| Official API/help docs, changelogs, setup guides, migration notices | States not reached in the present account | Record version/plan prerequisites and seek matching authorized observations |
| Roles, plans, quotas, upgrade gates, region and feature flags | Hidden branches and entitlement behavior | Build an access matrix; distinguish denied, unavailable, absent and unobserved |
| OAuth scopes, provider setup, webhooks and expired connections | Integration lifecycle and action permissions | Map connect, refresh, revoke, retry, duplicate, timeout and reconciliation states |
| Templates, imports/exports, audit logs, run history | Hidden schemas and multi-step behavior | Compare before/after versions and event lineage; test round trips with valid preconditions |
| Latency, caching, ordering, duplicate responses, restart behavior | Candidate scheduling/consistency explanations | Repeat controlled sequences and retain timing; timing alone does not identify architecture |
| Inconsistencies among docs, UI, API and code | Stale sources, experiments with confounders or missing rules | Preserve the contradiction and test alternatives; do not vote among correlated sources |
| Candidate failures and independently generated counterexamples | Omitted requirements or incorrect hypotheses | Minimize the failing sequence and replay against the applicable reference/contract |
| Similar open-source systems and domain fundamentals | Feasible substitute architectures and necessary invariants | Use as design candidates; they are not evidence that the target uses that implementation |

Chrome documents request initiators/dependencies in its
[Network reference](https://developer.chrome.com/docs/devtools/network/reference).
Schemathesis describes chaining operations through response-derived data and
[stateful testing](https://schemathesis.readthedocs.io/en/stable/explanations/stateful/).
[AALpy](https://github.com/DES-Lab/AALpy) supplies active automata-learning methods
for suitable interfaces. These are reviewed method references, not installed
adapters or proof that arbitrary SaaS state can be completely learned.

## Investigate each clue

1. Preserve the observation and exact source, version, role, plan and conditions.
2. State the suspected missing relationship and why it matters to an outcome.
3. List competing explanations, including obsolete/inaccessible behavior and an
   incomplete current model. State predictions and falsifiers for each.
4. Identify confounders: caching, tenant data, permissions, flags, feature rollout,
   locale/timezone, eventual consistency, random output or provider availability.
5. Choose the smallest authorized experiment that separates important alternatives.
   Prefer high impact and strong discrimination at acceptable cost/risk. Use
   ordinal priorities unless numeric probabilities/costs are actually calibrated.
6. Define reset/preconditions, negative controls, observation window and oracle.
   Absence is evidence only if the collector could have seen the predicted effect
   and the time/access/state conditions were sufficient. Retain positive controls.
7. Execute, preserve raw evidence, minimize counterexamples and revise the graph.
   Keep contradicted explanations; do not silently rewrite the history.
8. Convert supported requirements into independently testable implementation work.
   If several architectures remain consistent, choose a justified substitute and
   label it as a design decision. A match does not identify hidden source uniquely.

Use the [clue register](templates/CLUE-REGISTER.csv),
[hypothesis process](HYPOTHESIS-DRIVEN-RECONSTRUCTION.md) and
[executable experiments](RECREATOR-EXPERIMENTS.md). A clue can produce several
hypotheses; an experiment can leave all of them unresolved. Unsupported numerical
confidence and agreement between models do not close a gap.

## Discovery coverage and stopping rules

Track coverage across outcomes, modules, roles/plans, entity lifecycles, state
transitions, interactions, time horizons, platforms and external dependencies.
Report the observed inventory, unexplored frontiers, blocked access, contradictions
and newly discovered capabilities per exploration pass. Keep discovery coverage
separate from implementation and acceptance coverage. Do not calculate a whole-
product percentage when the denominator is unknown.

Use both forward tracing (action to durable outcome) and backward tracing
(report/bill/error back to originating events). Alternate documentation-led,
UI-led, request-led, data-led and failure-led passes. Review high-impact graph
boundaries independently. Revisit when the reference version, permissions or
feature set changes. Repeated passes yielding no new clues are evidence of
discovery saturation within those conditions, not proof that no feature is missing.

Release within a declared scope only after mandatory outcomes have complete
evidence chains, consequential contradictions are resolved or disclosed, and
required fidelity/security/integration/operational gates pass. Explicitly retain
unobserved plans, long-horizon behavior and inaccessible provider internals.
No finite black-box method can certify that every possible missing link was seen.

## GHL example: AI agent logs

The private discovery log observed Agent Studio, knowledge-base controls and Agent
Logs navigation. This suggests investigation of run identity, input snapshots,
tool permissions, execution state, cancellation/retry, approvals and usage events.
Those are hypotheses about necessary behavior; navigation alone does not prove
any schema, scheduler, provider or billing algorithm.

Useful next evidence includes an authorized existing run's visible history,
documented API schemas, approved test-draft configuration exports and observed
request/event relationships. Unknown execution semantics remain open until an
appropriate sandbox experiment is authorized and observed. A local substitute
must test these requirements independently without claiming it recovered the
vendor's internal implementation.
