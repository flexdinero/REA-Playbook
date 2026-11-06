# Target brief

Copy into the actual target project and replace every undecided field. This file is a template, not a populated target specification.

## Assignment

- Project/product:
- Mode: greenfield / source-assisted reconstruction / black-box reconstruction / binary interoperability / migration / enhancement
- User outcomes and must-have journeys:
- Reference URL/artifact paths and exact version/build/date:
- Available source, docs, binaries, captures, production records and test accounts:
- Authorized analysis scope and permitted code/assets/data/model reuse:
- Required outputs: source, running build, deployments, migration, documentation, operations
- Definition of “AaaS” for this project, if applicable: agent / automation / analytics / another service

## Coverage

- Platforms, supported OS/browser/device versions:
- Roles/admin/support personas, tenant model, plans/features:
- Locales, timezones, accessibility needs:
- APIs/protocols/file formats/integrations:
- Applicable enterprise requirements: identity, billing, privacy, audit, recovery, support
- Required fidelity dimensions and accepted differences:
- Known blind spots/access limits:
- Out of scope and reason:
- Enhancements requested separately from the reference:

## Architecture and operating constraints

- Existing repository/stack and instructions:
- Hosting and hosted database provider; environment separation:
- Data residency, sensitivity and allowed model providers:
- Retention/export/deletion rules:
- Expected dataset, traffic/concurrency, job rates and growth:
- Latency/throughput/error budgets:
- Backup recovery point/time objectives:
- Infrastructure, model and third-party spend ceilings:
- Deadline/team/maintenance owner:
- Actions already authorized versus requiring additional authority:

## Acceptance contract

| Dimension | Scope | Metric/test oracle | Threshold | Required evidence |
|---|---|---|---|---|
| Visual | To define | Matched-state diff/manual comparison | To define | Captures/diffs |
| Behavior | To define | Reference outcomes and side effects | To define | Differential corpus |
| API/data | To define | Contract/invariant checks | To define | Test artifacts |
| Performance | To define | Named workload/environment | To define | Load report |
| Security | To define | Threat model and negative cases | To define | Review/test evidence |
| Recovery | To define | Backup restore/failure drill | To define | Measured drill |
| Model/video | If applicable | Holdout/timeline/provenance | To define | Evaluation/manifest |

Mandatory requirements need evidence-backed PASS. Unknown and untested requirements block claims of completeness. Changes to scope must be recorded and accepted; do not remove a failing requirement merely to improve a percentage.
