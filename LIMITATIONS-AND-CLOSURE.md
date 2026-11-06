# Limitations: identify, address and prove closure

This playbook applies concrete remedies to addressable engineering gaps. It does not claim that naming a tool solves a problem, that every possible limitation has been discovered, or that unknowable behavior can be recovered by prompting harder.

## Closure classes

| Class | Meaning | How to handle it |
|---|---|---|
| Engineering | A tool/design/test can address the known gap | Implement the remedy and run its closure test |
| Access/resource | Depends on artifacts, accounts, credentials, hosts, devices, budget or third parties | Obtain authorized prerequisites; test; keep blocked until then |
| Evidence boundary | Evidence cannot support the desired universal claim | Narrow the claim to measured scope, obtain stronger evidence, or disclose a substitute |

The [limitation register](templates/LIMITATION-REGISTER.csv) supplies specific starting checks and closure methods. Every row is initially UNASSESSED: this is a reusable checklist, not a report that a target has passed. The [GoHighLevel assessment](GHL-RECONSTRUCTION.md) shows how to apply it to a large SaaS.

## Apply the process

1. Copy the register into the target project's evidence system. Assign an owner and mark applicability with a reason. Add target-specific gaps as they are discovered.
2. Identify actual failure evidence and the requirement it affects. Classify the missing knowledge/capability rather than guessing at a tool.
3. Select the smallest method/tool/host that can answer the question. Read its current primary documentation, pin versions and complete a tool-adoption record.
4. Obtain actual authorized prerequisites. A catalog entry does not supply source, API access, provider service, device, signing certificate or compute budget.
5. Run a discriminating experiment, implement the remedy and independently verify it.
6. Retain inputs, raw outputs, environment/build identity, limitations and the test oracle.
7. Mark VERIFIED only when the closure test passes. Otherwise use FAIL, BLOCKED, UNTESTED or accepted NOT-APPLICABLE. Preserve known residual differences.
8. Repeat when reference versions, dependencies, external APIs, extraction settings or relevant requirements change.

## Required target artifacts

A target project needs a brief; requirements/roles/state inventory; access map; question and limitation registers; behavior/API/event/data specifications; architecture decisions; a toolchain/host manifest; traceability; raw evidence; implementation; independent tests; deployment/migration/recovery plans; operational ownership; and an evidence-backed release report.

These must contain actual project findings. Templates are not finished artifacts. Scaffolding is not implementation. Passing local structure checks is not target acceptance.

## What does not have a universal technical remedy

Finite black-box observations admit multiple possible hidden implementations. Compilation generally erases information, so decompilation does not uniquely identify the original source. Private server source/data, inaccessible weights, lost historical events and undisclosed future behavior cannot be conjured from client output. Exhaustive equivalence for arbitrary programs is not obtainable through a general-purpose finite test process.

Stronger access, formal specifications and bounded verification can establish stronger claims for specific components. They do not certify every possible product or future environment. A new implementation may intentionally meet the user's outcomes better while differing internally; label that as an independent design or evaluated substitute.

## Release rule

Every mandatory limitation relevant to a declared requirement must have verified closure or block the corresponding release claim. An evidence boundary blocks “perfect universal clone,” even when a narrower useful product can be accepted. Do not reclassify an unresolved issue as solved to satisfy wording.
