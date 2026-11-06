# Agentic Recreator Suite

Status: implementation in progress; the command reference and verification record below are updated as increments pass. This extends the research playbook with a small, agent-neutral control plane. It does not recover inaccessible source or prove universal equivalence.

## Implementation contract

The Python 3.10+ standard-library package `recreator` runs owned-project checks, freezes acceptance inputs, retains hashed receipts, bounds repair attempts, restores rejected edits, and gates reusable lessons on independent evaluation. Runtime state belongs outside this public repository. The target repository remains the implementation home.

Mandatory acceptance: refuse implicit execution; reject escaping paths and corrupt state; detect changed protected inputs; execute actual checks rather than accept model-supplied pass flags; retain failed candidate evidence; restore rejected file edits; stop after the repair budget; preserve a pending repair across process interruption; promote only evaluated lessons in their original project scope. Independent acceptance remains a human/agent responsibility: an exit-zero command is only as useful as its assertions.

The first release deliberately uses a single-writer private artifact workspace, not a distributed scheduler. Hashes detect accidental alteration, not a malicious owner rewriting the entire workspace. Trusted-local execution is not a sandbox. Docker execution requires a locally available digest-pinned image and an operational daemon; source mounts are read-only and outbound networking is disabled. No model API, provider billing, live target mutation or package installer runs implicitly.

## Increment order

1. Artifact integrity, explicit execution and negative tests.
2. Frozen profiles, receipts and bounded file-repair transactions.
3. Evidence-backed learning promotion and agent-neutral handoff.
4. Research/tool/skill reference and private GoHighLevel integration.
5. Full package checks and publication verification.
