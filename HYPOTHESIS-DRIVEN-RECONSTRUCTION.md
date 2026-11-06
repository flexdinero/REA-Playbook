# Reconstruct hidden behavior through research and elimination

The objective is the strongest defensible recreation of a target's observable capabilities. Missing internal visibility is an investigation problem: research it, propose explanations, collect discriminating evidence, eliminate inconsistent explanations, and validate an independent implementation. Multiple hidden architectures may remain consistent with all observations; matching the required contract is then the practical goal.

## 1. Establish first principles

Before guessing frameworks, identify the target's inputs, outputs, persistent state, time semantics, authorization boundaries, resource constraints and external dependencies. Derive necessary invariants: records must remain tenant-scoped; a completed payment needs reconciled accounting; a retried action must have defined duplicate behavior; observable changes must have a state transition or external event behind them.

Keep separate ledgers for observed facts, hypotheses, derived requirements and independent design choices. Use precise source locations and version dates. Do not turn a plausible architecture into a recovered fact.

## 2. Research before probing

Inspect available source, official product/developer/help documentation, schemas, change logs, exported configurations, client bundles/source maps, native artifacts, authorized network captures and integration documentation. Use the reference index to locate relevant methods and tools; confirm consequential claims at primary sources.

For each feature create a fact sheet with observed actions, outputs, timing, state and unresolved questions. External dependency documentation can explain candidate behavior but cannot prove the target uses that exact configuration. Similar open-source implementations are design references, not evidence of the target's internals.

## 3. Generate competing explanations

For each material unknown, list at least two plausible explanations when possible. State what each predicts, what would falsify it, assumptions, confounders and the cheapest useful observation. Include a fallback hypothesis that the current model is incomplete. Use [the hypothesis register](templates/HYPOTHESIS-REGISTER.csv) and [experiment packet](templates/EXPERIMENT-PACKET.md).

Avoid invented numeric confidence. Unless probabilities are calibrated, use evidence-supported status: proposed, consistent-with-evidence, contradicted, insufficient-evidence, or accepted-as-implementation-choice. Consistency is not uniqueness.

## 4. Select informative experiments

Prioritize observations that distinguish plausible explanations and reduce a high-impact implementation risk. A useful heuristic is expected reduction in important uncertainty divided by time/cost/risk; state how you estimated it rather than claiming a calibrated Bayesian result.

Control starting state, user/tenant/role, inputs, locale/timezone, feature flags, target version, browser/device and external sandbox responses. Reset state where possible. Change one relevant factor at a time, then test interactions. Repeat runs to distinguish stable semantics from noise, cache, load or randomness. Retain failed experiments and contradictions.

Tests against third-party services must remain within actual authorization, documented quotas and safe test access. Run invasive failure injection on your own implementation or an authorized sandbox; lack of permission is not a prompt-engineering problem.

## 5. Experiment families

| Unknown behavior | Discriminating observation | Tools/method |
|---|---|---|
| Client/server responsibility | Compare loaded code, requests and controlled disconnected behavior | REA, DevTools, Playwright |
| Validation/order/defaults | Vary boundary/malformed fields and record exact errors/side effects | Schema corpus, Schemathesis, contract tests |
| Stateful workflow | Replay event sequences from reset state and vary order | State machines, LearnLib/AALpy where suitable |
| Duplicates/idempotency | Repeat the same operation with controlled identity/key/state | Replay harness and durable side-effect accounting |
| Timer semantics | Compare delay, cancellation, timezone/DST and restart cases | Controlled clock in your implementation; observed reference timing |
| Concurrency/atomicity | Controlled simultaneous edits and conflicting operations | Barrier-based tests, transaction/invariant checks |
| Eventual consistency/cache | Compare read paths and repeated observations over time | Timestamped traces; do not infer a specific cache product |
| Provider/network failure | Controlled timeout, partial reply and recovery | WireMock/Toxiproxy on authorized test systems |
| Native algorithm | Boundary inputs that distinguish instruction/pseudocode interpretations | REA/Ghidra, differential/property tests |
| Numerical behavior | Signedness, overflow, rounding and extreme values | Known-answer corpus, exact arithmetic or stated tolerances |
| Search/ranking | Controlled corpus with one changed factor and repeated queries | Labeled retrieval tests and order comparisons |
| AI stochastic behavior | Repeated task trials with fixed accessible settings | Protected holdout and distribution/task metrics |
| UI/motion | Same state, viewport, input and animation time | Playwright, visual review, frame/timeline comparisons |

## 6. Eliminate, update, and preserve alternatives

Reject an explanation only when the observation conflicts with its prediction under verified test conditions. A failed experiment can also mean a broken fixture, hidden flag, race, quota, changed build or incorrect assumption. Investigate confounders before declaring a conclusion.

Turn each accepted counterexample into a regression case. If explanations remain observationally indistinguishable, record that fact and choose an implementation by correctness, simplicity, maintainability and measured operating requirements. Do not spend unlimited calls trying to infer an unidentifiable implementation detail.

## 7. Build the smallest executable model

Implement a state machine, parser, algorithm or service slice that predicts the observed outcomes. Compare it with the reference on a shared corpus. Include generated and adversarial cases as well as examples used to derive the model. Keep a holdout to detect overfitting the reconstruction to known examples.

For suitable finite state/protocol interfaces, active automata learning can help discover candidate state machines. It requires an appropriate input abstraction, state reset/repeatability and a meaningful test oracle. Real SaaS may be unbounded, nondeterministic or externally stateful; treat any learned model as an abstraction with explicit limits.

## 8. Escalate evidence only when useful

If UI/API evidence leaves a consequential ambiguity, inspect relevant client code, data files or native instructions. Use runtime instrumentation on an authorized executable when execution can discriminate the question. If no artifact or permitted observation can expose the hidden component, implement the documented observable semantics and test them as a substitute.

Formal models can check declared invariants and explore bounded interleavings. They do not reveal the original server code, and their value depends on the accuracy of the model and assumptions.

## Example: a delayed workflow action

Suppose an action becomes visible after a delay. Candidate explanations include a durable scheduled job, periodic polling, or a client-only timer. Closing the UI and checking a separate authorized client can contradict a strictly client-local explanation. Controlled repeated timing may distinguish coarse polling behavior from other scheduling semantics, but cannot uniquely prove the vendor's queue/database design.

Next test cancellation, duplicate enrollment, edits during the wait, timezone changes and dependency failure in permitted environments. Implement a durable scheduler with explicit idempotency and cancellation semantics that passes these observations. Record its architecture as an independent design. This recreates verified behavior without claiming to have recovered an unseen implementation.

## Specialist tools and primary references

- [LearnLib](https://github.com/LearnLib/learnlib) / [AALpy](https://github.com/DES-Lab/AALpy): automata-learning candidates for suitable stateful interfaces.
- [Hypothesis](https://github.com/HypothesisWorks/hypothesis) / [fast-check](https://github.com/dubzzz/fast-check): property-based input generation and counterexamples.
- [WireMock](https://github.com/wiremock/wiremock): controlled HTTP test doubles; not proof of a real provider integration.
- [Toxiproxy](https://github.com/Shopify/toxiproxy): controlled network faults in your test infrastructure.
- [TLA+/TLC](https://github.com/tlaplus/tlaplus) / [Alloy](https://github.com/AlloyTools/org.alloytools.alloy): specification/model exploration for selected invariants and state spaces.
- [OpenAPI](https://www.openapis.org/) / [AsyncAPI](https://www.asyncapi.com/): explicit HTTP/event contracts; recovered schemas still require validation.
- [OWASP ASVS](https://asvs.owasp.org/): security requirements to select and map to project tests, not an automatic certification.

These primary sources were checked for method/tool relevance, not installed or benchmarked here. Select and verify individual candidates; the framework does not require every tool. Broader application/analysis tools remain in [TOOLCHAIN](TOOLCHAIN.md).

## Done condition

For each mandatory feature: a stated contract; evidence-backed observations; a recorded hypothesis/experiment history for significant unknowns; a working implementation; independent tests with counterexamples/holdout cases; operational proof where applicable; and residual differences clearly reported. That is the best-supported reconstruction claim the available evidence permits.
