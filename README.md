# REA Playbook

An evidence-led operating system for authorized software reconstruction and enterprise engineering: web, mobile, desktop, APIs, automations, SaaS, agent services, and AI/model applications.

**Canonical home: [github.com/flexdinero/REA-Playbook](https://github.com/flexdinero/REA-Playbook).** Give this repository to your engineering agent, use the master prompt, and keep the target's requirements and evidence in its own project.

This combines the roles of [REA](https://github.com/morluto/rea), [Ghidra](https://github.com/NationalSecurityAgency/ghidra), [REA-Prompts](https://github.com/JoasASantos/REA-Prompts), [rea-video](https://github.com/JuneYaooo/rea-video), and [Awesome-REA](https://github.com/reacher-z/Awesome-REA), with an original delivery process, agent capability checks, specialist prompts, and acceptance templates.

**Start:** [Agent entry point](AGENT-START-HERE.md) · [Master prompt](MASTER-PROMPT.md) · [Operating playbook](PLAYBOOK.md) · [Reference index](REFERENCE-INDEX.md)

**Executable suite:** [Agentic Recreator Suite](RECREATOR-SUITE.md) adds explicit target checks, hashed evidence, frozen acceptance inputs, recoverable repair transactions, and project-scoped learning. It runs with Python 3.10+ and the standard library. Any capable agent can supply candidate edits; no vendor is required.

[Executable experiments](RECREATOR-EXPERIMENTS.md) connect frozen experiment
packets to real preparation/observation commands and independent recorded oracles.

[Missing-link discovery](RECREATOR-DISCOVERY.md) explains how clues, contradictions,
dependency tracing and controlled experiments uncover omitted requirements.

For complete use, follow [setup and commands](RECREATOR-OPERATIONS.md), [research/tool decisions](RECREATOR-RESEARCH.md), [quality and cost policy](RECREATOR-MODEL-POLICY.md), [agent operating packet](prompts/RECREATOR-ORCHESTRATOR.md), and [executed acceptance and boundaries](RECREATOR-ACCEPTANCE.md). Self-healing means bounded, tested repair with rollback; learning means reviewed, scoped procedures with holdout checks and revocation. Neither means autonomous permission changes or guaranteed equivalence.

For best-supported recreation of behavior you cannot directly inspect, use [Hypothesis-driven reconstruction](HYPOTHESIS-DRIVEN-RECONSTRUCTION.md): research, first principles, competing explanations, discriminating experiments, counterexamples and independent validation. Apply the [76-item limitation register](templates/LIMITATION-REGISTER.csv) through [the closure process](LIMITATIONS-AND-CLOSURE.md). For a large SaaS example, read [the GoHighLevel assessment](GHL-RECONSTRUCTION.md). These are actionable methods; unexecuted checks do not count as solved target limitations.

The [final research audit](FINAL-RESEARCH-AUDIT.md) adds test-oracle design, metamorphic testing, reset/replay discipline, distributed histories, test sensitivity and scoped formal verification. The [offline comparison harness](OBSERVATION-HARNESS.md) makes deterministic recorded-case comparison executable; it is not a target collector or universal equivalence verifier.

## Give this to your AI agent

Copy this instruction, replace the bracketed fields, and provide authorized reference artifacts or test access:

```text
Use https://github.com/flexdinero/REA-Playbook as the operating reference for this project.

First read README.md, AGENTS.md, AGENT-START-HERE.md, and MASTER-PROMPT.md.
Then read PLAYBOOK.md and task-relevant parts of CAPABILITY-AUDIT.md,
AGENT-COMPATIBILITY.md, TOOLCHAIN.md, ECOSYSTEM-AUDIT.md, and REFERENCE-INDEX.md.
Load specialist prompts and catalog entries only as needed.

For hidden behavior read HYPOTHESIS-DRIVEN-RECONSTRUCTION.md and
LIMITATIONS-AND-CLOSURE.md. Maintain competing explanations, research evidence,
controlled experiments, counterexamples and closure tests rather than guessing.

For verification apply FINAL-RESEARCH-AUDIT.md and templates/ORACLE-ASSURANCE.md.
Use OBSERVATION-HARNESS.md only for its supported deterministic capture contract.
Validate reset conditions, oracle independence and the capture/adapter evidence chain.
For executable orchestration read RECREATOR-SUITE.md, RECREATOR-OPERATIONS.md,
prompts/RECREATOR-ORCHESTRATOR.md and RECREATOR-ACCEPTANCE.md. Keep runtime state
private. Use bounded repairs and holdout-gated lessons; select cheaper models only
when task qualifications pass, following RECREATOR-MODEL-POLICY.md.

My target: [product/repository/authorized application/artifact]
Mode: [greenfield / reconstruction / interoperability / migration / enhancement]
Result: [working deliverables and mandatory journeys]
References/access: [source, artifacts, URL, accounts, captures, docs]
Constraints: [platforms, budget, hosting, data handling, deadline]
Actions authorized: [local work / installation / sandbox resources / publishing]

Complete templates/TARGET-BRIEF.md in the target project. Keep its requirements,
decisions, gaps, evidence and tests there. Inventory the actual workspace, access,
tools, providers and versions before installing anything.

Apply the master prompt's evidence and agent-capability rules. Use the current agent and its actual tools; do not require named models, automatic
routing, model switching, or multiple agents.
Define the fidelity boundary and acceptance criteria, identify the highest-risk
unknown, and execute the first authorized end-to-end slice. Continue through the
agreed scope. Report missing access and unknowns precisely; never invent test results.
```

A repository URL does not install REA/Ghidra, register MCP, configure models, or grant target access. If your agent cannot read GitHub, give it a local clone or the relevant Markdown files. Context-limited agents should follow the reading order rather than ingest every catalog record.

## What is included

| File | Purpose |
|---|---|
| [AGENTS.md](AGENTS.md) | Discoverable instructions for agents working in this repository |
| [AGENT-START-HERE.md](AGENT-START-HERE.md) | Entry point and evidence boundaries |
| [MASTER-PROMPT.md](MASTER-PROMPT.md) | Copy-ready instruction covering scope through verified operation |
| [PLAYBOOK.md](PLAYBOOK.md) | Execution sequence, commands and acceptance gates |
| [CAPABILITY-AUDIT.md](CAPABILITY-AUDIT.md) | REA/Ghidra capabilities and missing proof |
| [ECOSYSTEM-AUDIT.md](ECOSYSTEM-AUDIT.md) | Findings across the added repositories |
| [TOOLCHAIN.md](TOOLCHAIN.md) | Tools/frameworks mapped to capability gaps |
| [AGENT-COMPATIBILITY.md](AGENT-COMPATIBILITY.md) | Use with Grok, Claude, Gemini, ChatGPT/Codex and other agents |
| [PROMPT-EXTENSIONS.md](PROMPT-EXTENSIONS.md) | Sixteen focused enterprise, reconstruction, AI and media prompts |
| [WORKED-EXAMPLE.md](WORKED-EXAMPLE.md) | CSV-export pilot showing the complete evidence-to-acceptance loop |
| [FINAL-RESEARCH-AUDIT.md](FINAL-RESEARCH-AUDIT.md) | Additional missing links, primary evidence, applied methods and remaining boundaries |
| [OBSERVATION-HARNESS.md](OBSERVATION-HARNESS.md) | Executable deterministic comparison format, command and limits |
| [REFERENCE-INDEX.md](REFERENCE-INDEX.md) | Task-oriented navigation and adoption rules |
| [Complete reference index](references/MASTER-REFERENCE-INDEX.md) | Every indexed record as browsable Markdown |
| [Structured index](references/master-reference-index.json) | Original upstream records with separate local review status |
| [RESEARCH-SOURCES.md](RESEARCH-SOURCES.md) | Sources, inspected versions and research limits |
| [VALIDATION.md](VALIDATION.md) | Generated package-check results |
| [PACKAGE-MANIFEST.sha256](PACKAGE-MANIFEST.sha256) | Package file hashes; excludes the manifest itself |

The preserved snapshot contains **1,488 curated upstream records**: 123 REA resources, 1,130 tool resources and 235 papers. Navigation adds 26 REAP prompt packs and five core repositories: **1,519 index records**. These are records, not 1,519 unique or locally tested tools. Repeated URLs and upstream evidence distinctions are retained.

## Reading order

1. Read this README and [AGENT-START-HERE](AGENT-START-HERE.md).
2. Complete the [target brief](templates/TARGET-BRIEF.md).
3. Apply [MASTER-PROMPT](MASTER-PROMPT.md) and [PLAYBOOK](PLAYBOOK.md).
4. Check [capability limits](CAPABILITY-AUDIT.md), then select the smallest suitable [toolchain](TOOLCHAIN.md) and [agent capability checks](AGENT-COMPATIBILITY.md).
5. Consult [ECOSYSTEM-AUDIT](ECOSYSTEM-AUDIT.md) before adopting installers or media workflows.
6. Use one [specialist prompt](PROMPT-EXTENSIONS.md) and relevant [reference entries](REFERENCE-INDEX.md) at a time.
7. Maintain target evidence and run the [release checklist](templates/RELEASE-CHECKLIST.md).

For a manageable first session, follow [WORKED-EXAMPLE](WORKED-EXAMPLE.md) before attempting a large reconstruction.

## Clone and validate

Git obtains the package. Python **3.10 or newer**, using only its standard library, runs the builder/validator. Neither script installs tools, calls models or contacts the network.

```bash
git clone https://github.com/flexdinero/REA-Playbook.git
cd REA-Playbook
python scripts/build_reference_index.py
python -m unittest discover -s tests -v
python scripts/verify_package.py
git diff --exit-code
```

Use `python3` where that is your Python command, or `py -3` on Windows when configured. Run commands separately and stop on failure. A clean checkout should have no diff after rebuilding. If you intentionally changed files, review and commit the regenerated index, validation report and manifest together.

Alternatively, use GitHub **Code → Download ZIP**. Repository source is the maintained package; no separate binary release is required.

Checks cover local file references, JSON/CSV structure, lossless catalog import, record identities, prompt boundaries and file hashes. They do not execute REA/Ghidra, check every external URL, reproduce upstream benchmarks or certify a target product.

## Set up REA and Ghidra when needed

First inventory installed tools, client registrations and existing skill folders. Read [the readiness workflow](PLAYBOOK.md#2-verify-the-workstation-and-connection) and [official REA installation documentation](https://github.com/morluto/rea/blob/main/docs/installation.md). Obtaining this playbook is separate from installing an analysis toolchain.

The **2026-11-06 research snapshot** recorded REA 6.8.0 and Ghidra 12.2. REA's guide separately described bridge verification with Ghidra 12.1.4/JDK 21; Ghidra 12.2 requires JDK 25. Recheck current releases, advisories and the selected pairing before adoption.

1. Select a supported Node.js/npm runtime for your pinned REA version.
2. Obtain an official prebuilt Ghidra release and compatible full JDK if native analysis is needed. A source clone is not a runnable installation.
3. Point `GHIDRA_INSTALL_DIR` and, where needed, `JAVA_HOME` at actual compatible installations.
4. Run scoped diagnostics and preview agent-configuration changes.
5. Apply setup within granted authority, restart the client and discover live MCP tools.
6. Analyze a harmless known fixture through the agent and retain its result.

Illustrative commands for the pinned research release:

```bash
npx rea-agents@6.8.0 doctor --provider ghidra --json
npx rea-agents@6.8.0 providers --json
npx rea-agents@6.8.0 setup --client codex --dry-run --json
npx rea-agents@6.8.0 setup --client codex
```

On Windows PowerShell, use `npx.cmd` if script-execution policy blocks `npx`. Replace `codex` with a supported client ID confirmed for the chosen release. Review setup changes before applying them. A terminal diagnostic is not proof of a live agent connection.

REA's native Windows Ghidra adapter has an experimental, bounded P0 surface. Linux-only workflows need an independently verified Linux environment; Apple builds/platform behavior can require macOS/Xcode and devices. See [CAPABILITY-AUDIT](CAPABILITY-AUDIT.md). For source-based or greenfield work, use source, contracts and active journeys first; add native analysis only for a concrete question.

## Apply it to a target project

Keep this repo as the shared operating reference. Keep target requirements, implementation, credentials, captures and binaries in the target workspace. Private artifacts do not belong in this public repository.

Suggested structure, adapted to the target's conventions:

```text
target-project/
  project/
    TARGET-BRIEF.md
    REQUIREMENTS.md
    DECISIONS.md
    PLAN.md
    GAPS.csv
    TRACEABILITY.csv
    RELEASE-CHECKLIST.md
    evidence/
      INDEX.md
      raw/
      comparisons/
  ...application source and tests...
```

| Template | Use |
|---|---|
| [Target brief](templates/TARGET-BRIEF.md) | Outcomes, access, constraints and acceptance contract |
| [Task packet](templates/TASK-PACKET.md) | Bounded inputs, ownership, model role, tests and stop conditions |
| [Evidence record](templates/EVIDENCE-RECORD.json) | Artifact identity, capture settings, claims and limitations |
| [Traceability](templates/TRACEABILITY.csv) | Requirement → evidence/spec → implementation → test → result |
| [Gap register](templates/GAP-REGISTER.csv) | Missing evidence, access and behavior; explicit decisions |
| [Tool adoption](templates/TOOL-ADOPTION.md) | Version, license, host support, trial result and owner |
| [Release checklist](templates/RELEASE-CHECKLIST.md) | Product, security, operations and applicable AI/media proof |
| [Oracle assurance](templates/ORACLE-ASSURANCE.md) | Oracle independence, reset assumptions, bounds, counterarguments and evidence chain |

Do not overwrite a target project's existing `AGENTS.md` with this repository's instructions. Add a reference to its existing instructions or give the bootstrap prompt directly to the agent.

## Execution workflow

| Stage | Deliverable | Gate |
|---|---|---|
| Scope/access | Brief, mandatory requirements, blind spots | Explicit acceptance boundary |
| Readiness | Versions and live fixture evidence | Connection proven; host limits recorded |
| Discovery | Roles/screens/states/contracts and question queue | Observations separated from inference |
| Investigation | Evidence and behavior specification | Critical unknowns resolved or blocked explicitly |
| Architecture | Contracts, boundaries and dependencies | Suitable design with testable invariants |
| First slice | One real end-to-end journey | Independent acceptance and divergence evidence |
| Expansion | Remaining mandatory slices | Traceability and regressions maintained |
| Release | Environment proof, recovery and operating owner | Mandatory gates pass; blockers remain visible |

For reconstruction preserve the reference baseline; track enhancements separately. For greenfield work use explicit user outcomes as the oracle. For migrations add data reconciliation and recovery rehearsal. For AI/media add statistical, timeline and provenance checks.

## Use with any capable agent

The playbook is vendor-neutral: use Grok, Claude, Gemini, ChatGPT/Codex or another agent. There are no required model assignments, automatic routing rules, model switches or effort settings. See [AGENT-COMPATIBILITY](AGENT-COMPATIBILITY.md) for capability-based setup and handoff instructions.

A coding agent with repository, shell and browser/MCP tools can execute the relevant steps. An ordinary chat interface without those tools can prepare specifications and review supplied evidence, but cannot claim local execution. Discover actual capabilities rather than assuming them from a product name. Missing capabilities need a concrete handoff or a visible block, not fabricated results.

Use one agent sequentially by default. Delegation, paid API use and resource provisioning require the existing project authority; this reference does not grant them by itself. Deterministic code owns hashes, parsing, arithmetic, comparisons and release gates.

## What “1:1” means

| Dimension | Evidence |
|---|---|
| Visual | Matched screen, state, viewport, fonts and data |
| Behavioral | Declared inputs, outputs, transitions and durable side effects |
| API/contract | Schemas, errors, versioning, auth and interoperability |
| Operational | Measured load, resilience, recovery, security and cost |
| Source/build | Accessible source/toolchain provenance or reproducible identity |
| Model | Accessible artifact/configuration identity or bounded statistical evaluation |

No prompt or tool guarantees universal cloning or perfection. Hidden server logic, private data, inaccessible weights and unobserved behavior remain evidence limits. Screenshot similarity does not establish backend equivalence; pseudocode is not original source.

Every mandatory requirement needs evidence-backed acceptance. Report PASS, FAIL, BLOCKED, UNTESTED and accepted NOT-APPLICABLE separately. Freeze the scope before reporting coverage, and expose discovery blind spots. See [CAPABILITY-AUDIT](CAPABILITY-AUDIT.md).

## Search and adopt references

Start with [REFERENCE-INDEX](REFERENCE-INDEX.md), then the [full Markdown index](references/MASTER-REFERENCE-INDEX.md) or structured JSON. Retain upstream dates, evidence links, limitations and review labels; local verification is separate.

```bash
rg -n -i 'android|protocol|firmware' references/MASTER-REFERENCE-INDEX.md
rg -n -i 'tenant|billing|migration' PROMPT-EXTENSIONS.md PLAYBOOK.md
```

The catalog is for discovery. Select by a concrete capability gap; check the primary source, current license, host/runtime, permissions and data handling; run a minimal harmless integration fixture. Do not install everything or treat catalog inclusion as endorsement.

The snapshot excludes unreviewed discovery queues and the broad source-scan index from its curated total. [Upstream file navigation](references/upstream-file-index.json) gives commit-pinned links for the three added repositories, not an audit of every file.

## Important upstream findings

- **REA-Prompts:** inspected installers remove existing same-named skill folders; documented generator scripts were absent from the inspected tree. Preserve local edits and review individual packs.
- **rea-video:** classifications and benchmark reproduction have documented limits. Assembly can retain original footage/audio. Independent recreation needs a complete replacement manifest and fresh decoding after extraction changes.
- **Awesome-REA:** source-review labels and dated prerequisites are discovery metadata, not local execution proof.
- **REA/Ghidra:** diagnostics, live connection, useful target analysis and product acceptance are distinct milestones.

Exact revisions and static-versus-runtime distinctions are in [ECOSYSTEM-AUDIT](ECOSYSTEM-AUDIT.md) and [RESEARCH-SOURCES](RESEARCH-SOURCES.md).

## Maintain and verify the repository

1. Edit authored guidance/templates for operating changes.
2. For catalog refreshes, record the new upstream commit, preserve notices, review drift, and deliberately update expected counts/schema handling. The builder does not fetch upstream.
3. Preserve original records and evidence distinctions; keep local measurements separate.
4. Rebuild, validate and review:

```bash
python scripts/build_reference_index.py
python -m unittest discover -s tests -v
python scripts/verify_package.py
git diff --check
git diff --stat
```

Commit authored changes with regenerated indexes, validation and manifest. GitHub Actions repeats the builder/validator and checks committed outputs are current. `.gitattributes` enforces LF text endings for cross-platform hashes. The manifest excludes itself, ZIP files, Git internals and Python caches. Keep local virtual environments outside this reference repository.

## Troubleshooting

| Symptom | Check |
|---|---|
| Agent cannot read the URL | Repository/network access; provide a local clone or selected files |
| Instructions visible but no REA tools | MCP registration, client restart, live discovery and provider readiness |
| Terminal works but agent fails | Registered runtime/environment/paths; run a live fixture |
| Windows Ghidra fails | P0 target/path limits, NTFS requirements and JDK/architecture pairing |
| Index counts change | Inspect source drift before adjusting pinned expectations |
| Missing local link | Restore the file or correct the link; regenerate outputs |
| Clean rebuild changes files | Line endings, unexpected files, interpreter or stale generated outputs |
| Agent produces plausible but incorrect results | Independent oracle, raw evidence, reset conditions, task size and counterexamples |
| Video renders but recreation is incomplete | Missing replacements and retained reference segments/audio |

## Provenance and attribution

Research snapshot: **2026-11-06**. [RESEARCH-SOURCES](RESEARCH-SOURCES.md) records exact scope and unverified areas. [THIRD-PARTY-NOTICES](THIRD-PARTY-NOTICES.md) attributes retained catalog material; its [MIT notice](references/awesome-rea/LICENSE) remains alongside the original JSON.

Linked tools, code, datasets, weights and media retain their own terms. A catalog's license does not grant rights to everything it links. This repo supplies operating guidance and reference artifacts; installing tools and proving a target implementation remain separate project work.
