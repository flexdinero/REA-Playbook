# Acceptance and remaining boundaries

The public kernel has 47 discovered unittest cases: 16 recorded-observation comparator cases, 19 control-plane/model-policy cases and 12 executable-experiment cases. On Windows, 46 pass and the POSIX permission case is skipped. The [first full hosted run](https://github.com/flexdinero/REA-Playbook/actions/runs/42293200666) passed the then-current 32-case suite on Windows/Linux with Python 3.10/3.13, including the Linux permission regression. Consult the current run before relying on a later revision.

| Capability | Executed evidence | Boundary |
|---|---|---|
| Recorded-case comparison | Existing 16 adversarial comparator tests | Offline supported contract only; no collector execution |
| Explicit execution | Implicit execution rejection plus actual CLI subprocess tests | Trusted-local is not a sandbox |
| Frozen inputs | Protected-test mutation rejection and artifact/state hash checks | Explicitly inventoried files; hashes are not signatures |
| Check source stability | A real mutating subprocess is rejected | Commands may modify unlisted files; audit full diff |
| Repair acceptance | Failing baseline, candidate, mandatory acceptance and holdout pass | Single existing file; one controller per target |
| Repair rejection | Failed candidate retained, original bytes restored, attempt ceiling enforced | External side effects cannot be undone by file rollback |
| Interruption | Pending recovery and unrelated-user-edit refusal | No distributed leases or process-tree guarantee |
| Intervening edits | Changes after baseline or during checks remain intact; CLI requires reconciliation | Boundary hash checks, not atomic filesystem CAS; concurrent target editing remains unsupported |
| File metadata | Permission-bit preservation; POSIX mode regression in Linux matrix | Custom ACLs, ownership, xattrs and security labels need an adapter |
| Executable experiments | Real subprocess preparation/observation, malformed/truncated output rejection, failed reset blocking, source-mutation rejection and CLI execution | Supplied adapters/oracles need independent review; interrupted experiments require inspection |
| Hypothesis ledger | Competing explanations and artifact requirements | Classification and experiment validity require review |
| Learning | Reflections alone rejected; disjoint case IDs required; promotion/revocation tested | Independence and causal improvement require external review |
| Cost selection | Cheapest qualified candidate; over-budget capability refused | Caller supplies current qualifications and total task cost |
| Real target | Private GHL: 22 module suites, 11 resilience tests, 6 required-auth groups and desktop contracts pass on Windows Node 22 and an owned Linux VM with Node 24 | Declared input hashes match across hosts, with checkout-root metadata normalized; not complete live fidelity |

Docker daemon/image execution was unavailable on the development host; that backend is implemented but has not been validated there. No hosted scheduler, database, object store, secrets broker, model gateway, production rollout, live provider messaging/payment, mobile device farm or load/failover experiment was provisioned. These are explicit integrations in [the research architecture](RECREATOR-RESEARCH.md), not hidden CLI capabilities.

The original owned Linux VM integration also passed its then-current 33 controller tests. Its target tests ran with
the trusted-local backend inside a temporary network namespace with loopback;
this is distinct from Docker validation. Windows separately passed an actual
Electron 45 hidden-window/renderer-to-main bridge smoke and an unsigned unpacked
build. The renewed desktop lockfile's npm audit reports zero vulnerabilities.
These are scoped test/build/advisory results, not signed-release or whole-product
security certification. Private evidence remains in the target repository.

The private GHL review found gaps in authentication/administrative authorization, production persistence, visual fidelity, external providers and newer AI surfaces. Restart handling and failure-reporting repairs improve resilience without closing those domains. Consult the private project's renewed acceptance record. No account identifiers, sessions, raw private captures or source are included here.

Run the package checks, inspect code and private/public boundaries, review side effects, and verify negative cases for changed gates. Add platform tests for atomic writes, subprocesses and paths. Keep manifests synchronized. Source review is not runtime proof. A changed target acceptance contract needs a new runtime workspace and review of old/new cases; never overwrite historical receipts.
