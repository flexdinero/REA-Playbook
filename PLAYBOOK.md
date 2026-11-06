# Master operating playbook

Use [MASTER-PROMPT.md](MASTER-PROMPT.md) as the agent instruction and this file as the execution sequence. Use [REFERENCE-INDEX.md](REFERENCE-INDEX.md) to select specialist material without loading every prompt and repository into context.

## 1. Frame a measurable target

Complete [TARGET-BRIEF](templates/TARGET-BRIEF.md). Freeze a reference build/date and define must-have journeys, platforms, roles, integrations, fidelity dimensions and numeric budgets. For greenfield work, use explicit user outcomes as the oracle. For reconstruction, separate reference behavior from proposed improvements.

Create `project/REQUIREMENTS.md`, `project/GAPS.md`, `project/DECISIONS.md`, `project/PLAN.md` and an evidence directory. These paths describe a future target project; this package does not pretend to have already filled them with target findings.

Assign stable IDs to requirements, questions, evidence, tests and deviations. Record accepted exclusions explicitly. A feature that cannot be observed is unknown, not absent. A feature added by the new design is proposed, not recovered.

**Exit evidence:** completed brief, defined fidelity boundary, ranked risks, access map, initial requirements/gaps, and a first experiment that could disprove feasibility.

## 2. Verify the workstation and connection

Start with read-only inventory. Identify installed Node/npm, Java/JDK, Ghidra and REA, client registrations and existing skill folders. Inspect junction targets before copying skills. Do not run third-party bulk installers over existing skill folders without reviewing their behavior.

Research snapshot: npm `rea-agents` 6.8.0; Node requirement `^22.23.4 || ^24.22.1 || >=26.12.1`. Ghidra latest release was 12.2. Recheck versions/advisories before adoption. REA documents bridge verification with Ghidra 12.1.4/JDK 21; 12.2 requires JDK 25. Test the chosen pairing rather than assuming either older verified or newer released means automatically suitable. Sources: [REA installation](https://github.com/morluto/rea/blob/main/docs/installation.md), [Ghidra install](https://github.com/NationalSecurityAgency/ghidra#install).

Prefer the official prebuilt Ghidra release for ordinary use. Cloning its repository downloads source; it does not produce a runnable installation. Use the source build only when developing Ghidra or needing an unshipped change.

Illustrative PowerShell sequence, to run only after selecting actual installed paths. These are preparation instructions; none was executed as an installation during this research.

```powershell
Get-Command node,npm,npx,java,javac,rea -ErrorAction SilentlyContinue
node --version
npm --version
java -version
javac -version

# Example paths: replace with the actual compatible installations.
$env:GHIDRA_INSTALL_DIR = 'C:\tools\ghidra_12.2_PUBLIC'
$env:JAVA_HOME = 'C:\tools\jdk-25'

# Acquires/runs the pinned package; run from a trusted directory.
npx.cmd rea-agents@6.8.0 doctor --provider ghidra --json
npx.cmd rea-agents@6.8.0 providers --json

# Preview client changes; this is a plan, not a verified connection.
npx.cmd rea-agents@6.8.0 setup --client codex --dry-run --json

# When installation/configuration is authorized, apply through its own review.
npx.cmd rea-agents@6.8.0 setup --client codex
```

Restart the agent as instructed, discover its live REA tools, and analyze a small known fixture through MCP. Confirm its known result and limitations. Retain both diagnostics and live results. `doctor` alone cannot prove the desktop agent inherited the environment or can analyze a target.

On native Windows check fixed local NTFS paths and the experimental Ghidra P0 admission boundary. Use a separate Linux environment for workflows requiring Linux. Verify process tools, architecture and file mappings inside that environment. Use macOS/Xcode/device infrastructure when an Apple build or platform behavior requires it. Treat each host as a separate lane in the toolchain manifest.

**Exit evidence:** installed versions and paths, provider diagnosis, successful live fixture, known host limits, isolated target workspace, and source preservation hashes.

## 3. Choose the investigation lane

| Target evidence | Start with | Move deeper only when |
|---|---|---|
| Available source | Repo/file inventory, build/test map, contracts, dependencies | Native dependency or undocumented behavior remains unresolved |
| Website/SaaS | Authorized role-by-role journeys, screenshots, client/network contracts | Loaded JS/WASM or client logic contains an unanswered rule |
| Electron | Static package/ASAR, modules, IPC, native addons | A native boundary controls the feature |
| Native desktop | Artifact metadata, relevant strings/imports, function inventory | Instructions/pseudocode or runtime tracing can discriminate a hypothesis |
| APK | Manifest/resources, DEX classes, JNI boundaries and device journeys | Obfuscation/native code/platform behavior blocks a testable question |
| Managed assembly | Metadata/CIL, source/decompiler where appropriate | NativeAOT or external native logic needs a native lane |
| Model/AI service | Pipeline/configuration, accessible artifact metadata and evaluation cases | Licensed weights/data and infrastructure permit deeper reproduction |
| Video/motion reference | Original-file metadata, shot timeline, audio/text/overlay evidence | Ambiguous methods require human/vision review or original production records |
| Firmware/device | Image layout/extraction and hardware identity | Emulation or hardware observation is required to resolve peripheral/timing behavior |

A video of an app can establish visible timing and interaction observations. It does not expose the app's backend or internal state. Use the software and video lanes together when both are available.

## 4. Capture evidence through focused experiments

Apply [hypothesis-driven reconstruction](HYPOTHESIS-DRIVEN-RECONSTRUCTION.md) for material hidden behavior and execute the [limitation closure process](LIMITATIONS-AND-CLOSURE.md). Use the [hypothesis register](templates/HYPOTHESIS-REGISTER.csv) and [experiment packet](templates/EXPERIMENT-PACKET.md) to make elimination reproducible.

Maintain a question queue. Each question specifies the behavior, current evidence, candidate explanations, one discriminating test, time/cost budget and stop condition. For example: “Does retrying a timed-out create request produce one record or two?” Capture the request, response, durable record count and retry schedule.

Reference observations should cover supported roles, tenant membership, empty/full/large data, fresh/returning sessions, disabled features, expiry, error paths and integrations. Record account role, feature flags, locale, timezone, viewport, device/OS and target version. Use dedicated test identities and safe test data.

REA native command examples are documented patterns, not executed results. Replace the path and select a real function from the inventory. CLI calls are separate processes; prefer a retained MCP session for repeated analysis and export evidence before closing.

```powershell
rea inspect 'C:\analysis\target.exe' --provider ghidra --json
rea search 'C:\analysis\target.exe' 'export' --kind procedures --provider ghidra --json
rea function 'C:\analysis\target.exe' 'EXACT_DISCOVERED_FUNCTION' --provider ghidra --json
rea analyze-javascript-application 'C:\analysis\electron-app' --json
rea inspect-model-artifact 'C:\analysis\model.safetensors' --hash full --json
```

These workflows come from [native investigation](https://github.com/morluto/rea/blob/main/docs/native-investigation.md), [CLI documentation](https://github.com/morluto/rea/blob/main/docs/cli.md), and [model-artifact documentation](https://github.com/morluto/rea/blob/main/docs/model-artifacts.md). Validate help/schema on the pinned release before automation.

Retain raw evidence and a concise index. Include source/hash identity, tool/provider/model/version, capture settings, run/session/evidence IDs, relevant locations, coverage, omissions and redactions. Keep paths/addresses in their proper coordinate system; source-file offset and loaded memory address are not interchangeable.

Use REAP specialist prompts as question starters, then add the evidence schema and acceptance gate from this playbook. Never paste its entire library into every session. See [ECOSYSTEM-AUDIT.md](ECOSYSTEM-AUDIT.md) for installer and documentation findings.

**Exit evidence:** enough behavior and contracts to implement the chosen slice, with unresolved questions clearly recorded.

## 5. Specify the behavior and architecture

For each feature write inputs, validation, state transitions, role checks, persistence, outputs, side effects and errors. Include examples derived from reference observations. Specify numerical precision, file encoding, ordering and time semantics where relevant. Document inferred internal designs as choices.

Define API/event schemas, authorization/tenant boundary, entity ownership, transaction boundaries, job semantics, search consistency and external contracts. Prefer a modular monolith initially when it meets requirements. Split services only for measured scaling, deployment, failure isolation or ownership needs. Do not choose Kubernetes, a message broker or a vector database without a requirement.

Record whether each borrowed input is an original, licensed reuse, independent implementation, demonstration or substitute. For independent reconstruction, keep the implementation packet focused on observable contracts rather than restricted source/assets.

**Exit evidence:** behavior specification, architecture decisions, a requirement-to-test plan, and bounded tasks with dependencies. Each task names its result, acceptance criteria, verification and affected modules.

## 6. Prove one complete slice

Choose the slice most likely to reveal a feasibility problem. For a SaaS example: user signs in, creates a tenant-scoped item, triggers a durable background job, receives a result, and sees a useful failure/retry state. Prove that another tenant cannot retrieve it. Use a real test provider where the integration is part of the claim.

For binary interoperability: isolate one algorithm, parser, record type or ABI; implement it independently; run identical normal and malformed inputs against the reference and replacement. For ML: run a fixed pipeline on representative/holdout cases with defined metrics and settings. For video: remake one representative hard shot and verify its timing/content before generating the whole timeline.

**Exit evidence:** a working end-to-end result and a divergence report. If it fails, revise the evidence or architecture before scaling the attempt.

## 7. Expand systematically

Add the remaining vertical slices in dependency order. Keep the reference baseline unchanged while evaluating enhancements separately. Run regressions after shared contract, auth, schema or infrastructure changes. Preserve version comparisons and investigation state across sessions.

Use risk-based testing to prioritize deep adversarial cases, while ensuring every mandatory requirement has an acceptance test. Do not claim exhaustive state-space coverage because each route was visited once.

**Exit evidence:** no mandatory requirement without implementation/test links; explicit unresolved gaps; tested negative paths and integration behavior.

## 8. Run the acceptance and operations gates

Use [RELEASE-CHECKLIST](templates/RELEASE-CHECKLIST.md). Freeze the requirement baseline before reporting coverage. Count `PASS`, `FAIL`, `BLOCKED`, `UNTESTED`, and accepted `NOT-APPLICABLE` separately. Mandatory-pass coverage is passing mandatory requirements divided by all mandatory requirements in that frozen baseline. Do not hide unknown features by manipulating the denominator.

Use [the oracle assurance packet](templates/ORACLE-ASSURANCE.md) for consequential claims and apply [the final research additions](FINAL-RESEARCH-AUDIT.md). Confirm fixture reset, oracle independence, normalization sensitivity, counterexample detection and relevant history/time coverage. The [offline comparator](OBSERVATION-HARNESS.md) can compare frozen deterministic capture records; collectors/adapters and other oracle classes require their own validation.

Publish separate fidelity results. For visuals use viewport/state-specific diffs and documented dynamic masks; do not choose an arbitrary universal pixel percentage. For behavior compare outputs and durable side effects. For stochastic models report confidence intervals or repeated-trial variation and task-specific metrics. Load tests must name environment, dataset, concurrency and duration. A restore drill must demonstrate recovery from an actual backup in a non-production recovery environment.

Deploy only within granted authority, to the declared environment, with a reversible release/migration plan where possible. Distinguish local checks, staging proof and production observations. Mark production readiness unverified until production-specific prerequisites are established.

**Exit evidence:** release report, artifact/build identity, live smoke results for the intended environment, operating owner, recovery proof and known limitations.

## 9. Maintain the result

Track upstream changes, reference version drift, dependencies/advisories, external API changes, flaky tests, customer defects and model regressions. Revalidate important borrowed references before acting on them. Keep deployment costs, workflow failure rates, latency and model accepted-task costs visible. Update the prompt and reference selection from demonstrated failure modes rather than adding motivational language.

## Working rules

- Never replace missing observations with confident invention.
- Never equate decompilation with exact source recovery.
- Never call an untested feature absent, complete or equivalent.
- Never use a screenshot as backend verification.
- Never silently retain reference footage/audio in an independently recreated output.
- Never treat stars, catalog inclusion, an author's benchmark or an agent's confidence as your acceptance result.
- Never auto-install an entire catalog. Select, review, pin, isolate and verify the tools actually required.
- Never spend repeated expensive calls on the same unchanged evidence without a new question.
- Never “enhance” the reference before preserving a measurable baseline.

## Short session prompts

**Discovery:** “Inventory this target by roles, states, contracts and operations. Cite evidence, list blind spots, and identify the first experiment that could invalidate the plan.”

**Investigation:** “Resolve question Q using the smallest discriminating observation. Return raw evidence IDs, interpretation, counterexamples, limitations and the next unresolved question.”

**Implementation:** “Implement requirement IDs X from the behavior packet, preserving its contracts. Return code, acceptance results and deviations. Do not weaken tests to fit the implementation.”

**Independent review:** “Compare the implementation with the frozen requirements and reference evidence. Prioritize concrete omissions, incorrect behavior and unverified claims. Challenge the happy path.”

**Handoff:** “Show what passes, fails, is blocked and remains unknown. Include commands/artifacts, environment, coverage denominator, differences and next required action.”
