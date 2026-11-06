# Operating the suite

Read [the suite contract](RECREATOR-SUITE.md), [research and architecture](RECREATOR-RESEARCH.md), and the target's own instructions first. Python 3.10+ is sufficient for the control plane; target runtimes are separate requirements. Run commands from the playbook checkout. No dependencies are installed automatically.

## Prepare a target

1. Inventory the existing implementation and current source commit before changing it. Preserve user work. List supported surfaces, roles, plans, platforms, locales and integrations. Use the existing target brief and limitation register.
2. Put the manifest and frozen scenario corpus in the private target project. Pick a separate private runtime directory outside both this public checkout and the target checkout. Keep a backup and set filesystem access appropriate to the data. Artifacts and logs can contain private data; they are not automatically redacted or encrypted.
3. List exact editable files and every acceptance dependency that must remain protected: tests, fixtures, comparison scripts, source captures, schemas, thresholds, relevant configuration and test dependencies. Protection is explicit per file, not a recursive directory policy. Resolve symlinks before use. A trusted process can still modify unlisted files; audit Git changes after every trial.
4. Define `acceptance` and `holdout` commands that fail on actual mismatches. A test that merely imports the implementation is insufficient. Identify independent cases and verify test sensitivity using a deliberately wrong candidate. Freeze reset rules, expected errors, ordering, clocks, permissions and downstream effects. Include the corpus file among protected files if commands read it from the target.

Example manifest; replace paths and commands with the target's actual executable checks:

```json
{
  "project_id": "my-owned-target",
  "repo": "C:/projects/my-owned-target",
  "repair_budget": 2,
  "required_profiles": ["acceptance", "holdout"],
  "editable": ["src/service.py"],
  "protected": ["tests/acceptance.py", "tests/holdout.py", "tests/holdout-b.py", "corpus.json"],
  "profiles": {
    "acceptance": {"cwd": ".", "argv": ["python", "tests/acceptance.py"], "timeout_seconds": 60},
    "holdout": {"cwd": ".", "argv": ["python", "tests/holdout.py"], "timeout_seconds": 60,
      "kind": "holdout", "case_ids": ["restart-a", "tenant-denial-a"]},
    "holdout_b": {"cwd": ".", "argv": ["python", "tests/holdout-b.py"], "timeout_seconds": 60,
      "kind": "holdout", "case_ids": ["restart-b", "tenant-denial-b"]}
  }
}
```

Use an explicit runtime executable, not a `.cmd` or `.bat` wrapper. For Node projects prefer a Node test aggregator over `npm.cmd`. Profile commands inherit a small environment allowlist; provider keys and database credentials are excluded. Integrations requiring secrets need a separately reviewed execution adapter and scoped secret broker; do not weaken the default by dumping the parent environment.

```text
python -m recreator --workspace C:/private/runtime/my-target init --manifest C:/projects/my-owned-target/recreator.json --corpus C:/projects/my-owned-target/corpus.json
python -m recreator --workspace C:/private/runtime/my-target run --trusted-local
python -m recreator --workspace C:/private/runtime/my-target handoff
```

`--trusted-local` explicitly executes owned code on this computer. It is not isolation: subprocesses can access the host and network. For reviewed untrusted artifacts use a dedicated environment. The optional `--sandbox-image registry/image@sha256:...` replaces local execution with Docker using a preloaded digest-pinned image, read-only source, no network, dropped capabilities and resource limits. The image must include the runtime and dependencies and support the fixed unprivileged user; tests may write only to `/tmp`. Docker setup is not implicit. The Docker path needs deployment validation on the selected host; a configured command is not proof of isolation.

## Repair without changing the answer key

An agent reads the handoff packet, relevant evidence and failing receipt, then proposes one replacement file outside the target repository. Supply the current file's SHA-256, not a guessed or stale digest:

```text
python -m recreator --workspace C:/private/runtime/my-target repair --path src/service.py --expected-sha256 SHA256_OF_CURRENT_FILE --candidate C:/private/candidate-service.py --trusted-local
python -m recreator --workspace C:/private/runtime/my-target status
```

The suite executes a baseline first. It requires at least one baseline failure and both `acceptance` and `holdout` profiles. It reserves a durable pending transaction and spends one repair attempt before changing the file. The candidate is retained as an artifact; all mandatory checks must pass with protected files unchanged. A rejected candidate restores the original editable file. It does not restore unrelated files modified by a trusted command. Inspect the full repository diff. Multi-file changes require a normal isolated branch/worktree and reviewed checks; this release's automatic repair transaction handles exactly one file.

Add target-specific security, migration, desktop or other gates to `required_profiles` before initialization. Default run/repair uses that frozen inventory; a repair cannot omit one by selecting a cheaper subset. Explicit named `run` profiles remain useful for diagnosis and lesson evaluation. A passing diagnostic subset is not a complete acceptance result.

Atomic replacement preserves existing permission bits. Custom Windows ACLs, ownership, extended attributes and security labels are not preserved by this portable implementation. Use ordinary development files in an isolated checkout; targets requiring those metadata need a platform-specific transactional adapter before automatic repair. Directory fsync and power-loss recovery are also deployment-specific; retain backups.

If interrupted, inspect status and run `recover`. Recovery restores the recorded original only when the current file matches the original or candidate hash. An unrelated edit requires manual reconciliation. If a stale writer lock remains after a crash, first verify that its recorded process is gone, retain the lock as incident evidence, and remove only that confirmed stale lock. Never run concurrent controllers against the same target. Resume does not imply exactly-once external side effects.

Exit codes: `0` successful operation, `1` failed checks or reverted repair, `2` invalid input, missing access or integrity/policy error. Read the JSON result and retained receipts. Check subprocess timeout and truncation flags. Local timeout stops the immediate process; it is not a process-tree containment guarantee. Raw output uses temporary disk before truncation; run hostile workloads only with an independently constrained environment.

## Research and competing explanations

Use the existing [hypothesis process](HYPOTHESIS-DRIVEN-RECONSTRUCTION.md) and retain primary sources. Register an artifact with `evidence --file PATH --kind observed --source DESCRIPTION --claim DESCRIPTION`. Classification is a reviewer assertion, not proof of truth. Preserve acquisition date, account/role, product version, scenario setup, action, result and capture mechanism inside the artifact.

Register `hypothesis --document PATH` with an object containing `question`, at least two distinct `explanations`, a discriminating `experiment`, and an `evidence` array of registered IDs. Resolve with `resolve-hypothesis --id ID --explanation ZERO_BASED_INDEX --evidence EVIDENCE_ID --status supported|contradicted|inconclusive`. Resolution needs at least one registered observation. `supported` applies to the recorded evidence and scope; it never means hidden source recovered. Reopen with a new hypothesis when contradictory evidence appears; retain the older event history.

## Learning and cost

Use `propose-lesson --document PATH` with `title`, `procedure` and `evidence` (artifact SHA-256 identities). The procedure starts quarantined as `proposed`. Replay it on separate held-out scenarios before `promote-lesson --id ID --reviewer NAME --runs RUN_A RUN_B`. The kernel requires passing receipts over disjoint frozen `case_ids` marked `kind: holdout`. A reviewer must verify that those labels correspond to genuinely independent scenarios and that the procedure caused the claimed benefit. Two renamed tests or repeated identical runs are not evidence of generalization. The command cannot verify reviewer independence or causal benefit by itself.

Only promoted lessons in the same project workspace appear in handoff. `revoke-lesson --id ID --reason TEXT` removes a lesson from retrieval while retaining history. No cross-project export, personal-memory update or model-weight training occurs. Cross-target reuse requires explicit sanitization, rights review, revalidation and a new scoped proposal. Store counterexamples and expiry conditions alongside procedures.

`select-model --candidates PATH --capabilities code vision --budget 1.0` chooses the lowest supplied `cost_per_task` among candidates with `quality_passed: true` and all required capabilities. Candidate objects contain `id`, `capabilities`, `quality_passed`, `cost_per_task`. This helper trusts the supplied qualification records; it does not measure quality, fetch prices, invoke APIs or enforce spending in a provider account. Preserve dated price and task-evaluation evidence outside the helper input. See [model policy](RECREATOR-MODEL-POLICY.md).

## Completion record

Report the exact commit, executed profiles, evidence hashes, scoped accepted behavior, open gaps and dependencies. Keep visual, functional, authorization, integration, resilience, performance and operational status separate. A self-reported success, passing unit suite or matching screenshot alone cannot close all dimensions. Publishing the framework does not complete a target migration or deploy a production service.
