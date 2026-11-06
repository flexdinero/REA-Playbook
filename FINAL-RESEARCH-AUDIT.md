# Final research audit: missing links and stronger reconstruction

Research date: 2026-11-06. Baseline reviewed: published commit `699fdbbcb61b87fdaf6c4e679a86c44777c5faf2`. This pass inspected the current authored guidance, templates, validator and CI, then selected primary research/tool documentation. It is not an exhaustive review of all literature, all catalog projects or all possible software.

## Finding

The previous package contained useful discovery and hypothesis-driven methods, but several verification requirements were named without sufficient operating detail. The most consequential missing layer was **an executable evidence and oracle process**: establish what counts as a correct observation, reproduce its conditions, detect counterexamples, verify test sensitivity, and limit each conclusion to its actual evidence.

This revision adds fifteen research-source records, sixteen additional limitation checks, an oracle/assurance packet and an offline deterministic comparison harness with failure-oriented tests. No newly researched external tool was installed or executed. GoHighLevel behavior and any other private target remain untested.

## 1. Test-oracle design

**Missing:** requiring an “independent oracle” did not explain how to proceed when exact outputs are unavailable or expensive to obtain.

**Apply:** classify each requirement's oracle: reference observation; explicit contract/known answer; domain invariant; metamorphic relation; independent implementation; or human adjudication. Record its authority, applicable inputs, independence, uncertainty and failure mode. An agreement among correlated model-generated answers is weak evidence, not an independent ground truth.

Metamorphic tests compare related executions when a complete answer is unavailable. Examples such as export/import round trips or pagination-total conservation require validated preconditions; lossy formats, mutable data and time-sensitive behavior can invalidate them. Treat candidate relations as hypotheses until supported. [The Oracle Problem in Software Testing: A Survey](https://discovery.ucl.ac.uk/id/eprint/1471263/1/06963470.pdf), [primary application study](https://www.cs.columbia.edu/wp-content/uploads/sites/7/2011/03/3478-Xie-QSIC09.pdf).

## 2. Active learning needs a real equivalence strategy

**Missing:** state-machine discovery could be read as eventually proving a whole SaaS correct merely by asking enough questions.

**Apply:** define input/output abstractions, reset semantics and the supported state class. Distinguish exact equivalence queries from approximations such as random walks or bounded suites. Angluin's foundational result assumes a teacher that can answer membership questions and provide equivalence counterexamples; an arbitrary web application does not automatically supply that teacher. State what an unsuccessful counterexample search establishes. [Angluin 1987, original paper](https://homepages.math.uic.edu/~lreyzin/papers/angluin87.pdf).

## 3. Controlled reset, repeatability and record/replay

**Missing:** “reset where possible” was too weak for stateful experiments. Browser resets can leave server jobs, external accounts, feature flags or caches unchanged.

**Apply:** define a reset contract for client, server fixture, clock, randomness, background jobs and external sandbox. Check its postconditions before each run; use a fresh isolated fixture when reset cannot be trusted. Retain raw event timing and conditions. For applicable Linux native processes, rr can support deterministic recorded debugging, but it has CPU/syscall/process-boundary restrictions and does not replay an entire remote SaaS service. [rr capabilities and limitations](https://rr-project.org/).

## 4. Distributed behavior requires histories

**Missing:** comparing final records can conceal duplicate effects, transient unauthorized access, lost updates or invalid operation ordering.

**Apply:** record invocation/completion intervals, operation identity, acknowledged/unknown outcomes and durable effects. Choose the actual consistency contract—do not demand linearizability for an intentionally weaker system or call eventual agreement proof of transactional correctness. Use Jepsen-style histories and controlled faults on your own test environment when appropriate. [Jepsen framework](https://github.com/jepsen-io/jepsen), [consistency definitions](https://jepsen.io/consistency).

## 5. Test the tests

**Missing:** coverage and passing tests can coexist with an oracle that cannot detect meaningful errors.

**Apply:** introduce representative deliberate deviations in a controlled copy: wrong tenant, duplicate charge, missing durable effect, timer boundary error or incorrect numerical sign. Require the acceptance suite to detect them. Where suitable, use mutation testing and review surviving/equivalent mutants; no universal score establishes product correctness. [Stryker documentation](https://stryker-mutator.io/docs/).

The included harness tests deliberately exercise missing observations, altered artifacts, wrong context, extra cases, event order and incorrect durable effects. They test the comparator's behavior, not a target's fidelity.

## 6. Coverage-guided discovery and counterexample reduction

**Missing:** property tests were listed without a mechanism for seeking unvisited executable behavior or minimizing failures.

**Apply:** for an available suitable native/library target, build a bounded harness, seed it with representative valid inputs, use instrumentation/sanitizers as appropriate, retain interesting inputs and minimize reproducible failures. AFL++ is a candidate. Coverage growth and absence of crashes do not establish semantic equivalence. Fuzz only authorized local/test systems; do not direct arbitrary generated traffic at a vendor's production service. [AFL++ in-depth guidance](https://github.com/AFLplusplus/AFLplusplus/blob/stable/docs/fuzzing_in_depth.md).

## 7. Formal evidence must expose its bounds

**Missing:** generic formal-model guidance did not distinguish finite model exploration, bounded bug finding and component refinement.

**Apply:** record the model/harness, assumptions, bit widths, environment/library models, loop/recursion bounds, checked properties, solver status and unresolved paths. A timeout or insufficient unwind is UNKNOWN. CBMC's tutorial distinguishes bounded checks and unwinding assertions; Alive2 targets LLVM transformations and warns about unsupported inter-procedural transformations. These can strengthen selected component claims, not verify every aspect of a reconstructed enterprise system. [CBMC tutorial](https://diffblue.github.io/cbmc/cprover-manual/md_cbmc-tutorial.html), [Alive2 scope](https://github.com/AliveToolkit/alive2).

## 8. Normalization can manufacture apparent equivalence

**Missing:** approved normalizations were required, but there was no default comparator that refused missing/extra cases and distinguished output, errors and durable effects.

**Apply:** use the [offline observation harness](OBSERVATION-HARNESS.md) for a frozen deterministic corpus. It performs exact JSON-value comparison with object key order ignored, array order retained and no automatic masks or tolerance. It checks case coverage, input/context alignment and local evidence-file hashes. Its numeric representation policy is deliberately strict. Other oracles require separate validated adapters/tests; do not force stochastic models, video similarity or concurrent histories through this comparator.

Any external normalization must retain original artifacts, have a reason tied to the contract and be tested against important differences it must preserve. Do not mask timestamps that determine billing, drop error fields, sort meaningful event order or ignore tenant identifiers to make a test pass.

## 9. Integrity, provenance and reproducible builds differ

**Missing:** the package's SHA-256 manifest establishes byte identity, not the truth of a capture or reproduction of an original program.

**Apply:** record capture actor/tool/build/run, retain original bytes and derived transformations, and verify authenticity/provenance when the source supplies it. For exact build claims, preserve source, toolchain, dependencies, environment and build instructions and demonstrate independent artifact reproduction. Reproducible-build and SLSA guidance address different assurance needs; neither is a universal behavioral proof. [Reproducible Builds definition](https://reproducible-builds.org/docs/definition/), [SLSA specification](https://slsa.dev/spec/v1.2/).

## 10. Discovery needs interaction and temporal coverage

**Missing:** a feature/state checklist can miss higher-order interactions and long-horizon lifecycle behavior.

**Apply:** enumerate factors and constraints, prioritize interactions by failure impact, and record which combinations are covered. Include subscription renewal, expiry, DST, background completion, account deletion, reconnection, version migration and eventual-consistency horizons where applicable. Pairwise coverage is a prioritization technique, not proof that higher-order defects are absent. Use virtual time in your implementation and permitted observation windows for the reference; disclose unobserved horizons.

## 11. The reference can be wrong

**Missing:** fidelity and correctness can conflict when the observed product has a defect or insecure behavior.

**Apply:** preserve the observation, classify intentional compatibility versus independently required correctness/security, and record the decision. Do not silently copy an observed defect or fix it while claiming identical behavior. Separate reference fidelity tests from product policy tests. Treat undocumented observations from one account/build as evidence for that context rather than a universal specification.

## 12. The remaining universal boundary is not a missing framework

For any finite observation set over an unbounded input space, two programs can agree on every observed input and disagree on an unobserved input. This constructive ambiguity explains why an apparently perfect black-box recreation need not recover the original hidden implementation. Stronger access/specifications can resolve specific uncertainties.

Separately, equivalence of arbitrary programs is undecidable in general; this does not prevent proofs for restricted components or finite models. It rules out a universal terminating verifier that settles every arbitrary program pair. [University of Rochester, program-equivalence discussion](https://www.cs.rochester.edu/u/nelson/courses/csc_173/computability/undecidable.html).

Therefore this review found **valuable missing methods, but no substantiated tool or research result that removes every limitation for every target**. The applicable next step is target-specific evidence acquisition and verification, using the improved process. No authenticated private target was available to execute that work in this research pass.

## Applied artifacts and acceptance

### Benchmark triangulation

Qualification must match the intended work. [Reveree](https://arxiv.org/abs/2609.01185v1) studies RE-agent progress and possible solution recall on public CTF tasks; it does not establish enterprise reconstruction. [Design2Code](https://aclanthology.org/2025.naacl-long.199/) evaluates screenshot-based frontend generation; this is not backend/service parity. [WebArena](https://webarena.dev/og/) checks task completion in supplied websites; operating an environment is different from reconstructing it. These scope distinctions are inferences from the primary task definitions, not reproduced benchmark results.

Use blind or independently authored target-representative fixtures, holdout cases, actual tools, observed milestones and result verification to qualify the current agent. Include unknown/incomplete evidence and a deliberate near-miss implementation. Do not infer cloning capability from a leaderboard, public answer recall or a model's confident narrative. This is an evaluation requirement, not prescribed model routing.

- [Oracle and assurance packet](templates/ORACLE-ASSURANCE.md) defines the evidence claim and independent checks.
- [Limitation register](templates/LIMITATION-REGISTER.csv) preserves L001–L060 and adds L061–L076 for these findings.
- [Comparison harness and format](OBSERVATION-HARNESS.md) make deterministic case comparison executable.
- The master prompt, entry points, playbook, release checklist and CI incorporate the additions without prescribing model routing.
- [Research source ledger](references/final-research-index.json) records fifteen sources and the review depth. Literature-tool discovery had no existing workspace; no external research workspace or paid deep search was created.

Completion of this research revision means the documented gaps were assessed and the package additions were tested/published. It does not mean every target limitation is closed or that every possible missing method has been discovered.
