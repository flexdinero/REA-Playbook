# Package validation

Validated 2026-11-06 using `python scripts/verify_package.py`.

- PASS: 185 local Markdown file references resolve.
- PASS: retained JSON files parse and CSV template headers are unique.
- PASS: 1,519 unique compound index IDs (records may share destination URLs).
- PASS: all 1,488 imported curated resource/paper records exactly match retained upstream JSON, in order and without dropping fields.
- PASS: 26 REAP prompt-pack links and five core navigation records included.
- PASS: master prompt has one copy boundary and agent-neutral instructions without prescribed vendor/model routing.
- PASS: 76 uniquely identified starting limitation checks remain UNASSESSED rather than claiming unexecuted closure.
- PASS: 15 supplementary research sources retain review scope and untested runtime status.

These checks validate the package structure and import fidelity. They do not execute upstream tools, verify every external URL, reproduce research benchmarks, or establish production readiness.
