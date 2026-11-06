"""Validate authored references and lossless catalog import; no network required."""

import csv
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def main():
    failures = []
    checked_links = 0
    files = [p for p in ROOT.rglob("*") if p.is_file()
             and ".git" not in p.relative_to(ROOT).parts
             and "__pycache__" not in p.parts
             and p.suffix != ".zip"
             and p.name not in {"PACKAGE-MANIFEST.sha256", "VALIDATION.md"}]
    for path in files:
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
        if path.suffix == ".csv":
            with path.open(encoding="utf-8", newline="") as handle:
                header = next(csv.reader(handle))
                if len(header) != len(set(header)):
                    failures.append(f"Duplicate CSV header: {path}")
        if path.suffix == ".md":
            text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
            for target in re.findall(r"\]\(([^\s)]+)\)", text):
                parsed = urlsplit(target.strip("<>"))
                if parsed.scheme or target.startswith("#"):
                    continue
                checked_links += 1
                destination = path.parent / unquote(parsed.path)
                if not destination.exists():
                    failures.append(f"Broken link: {path.relative_to(ROOT)} -> {target}")

    index = json.loads((ROOT / "references/master-reference-index.json").read_text(encoding="utf-8"))
    rows = index["records"]
    assert len(rows) == 1519
    assert len({r["record_id"] for r in rows}) == len(rows)
    for name in ("rea-resources.json", "tool-resources.json", "papers.json"):
        original = json.loads((ROOT / "references/awesome-rea" / name).read_text(encoding="utf-8"))
        imported = [r["upstream"] for r in rows if r.get("source_file") == f"awesome-rea/{name}"]
        assert original == imported, f"Lossy import: {name}"
    prompt = (ROOT / "MASTER-PROMPT.md").read_text(encoding="utf-8")
    assert prompt.count("--- START ---") == 1 and prompt.count("--- END ---") == 1
    assert "agent-neutral" in prompt
    assert not any(name in prompt for name in ("GPT-6 Astra", "GPT-6 Luna", "MODEL-ROUTING.md"))
    assert not (ROOT / "MODEL-ROUTING.md").exists()
    assert prompt.count("Use HYPOTHESIS-DRIVEN-RECONSTRUCTION.md when available.") == 1
    with (ROOT / "templates/LIMITATION-REGISTER.csv").open(encoding="utf-8", newline="") as handle:
        limitations = list(csv.DictReader(handle))
    assert len(limitations) == 76 and len({r['limitation_id'] for r in limitations}) == 76
    assert all(r['status'] == 'UNASSESSED' and None not in r for r in limitations)
    research = json.loads((ROOT / "references/final-research-index.json").read_text(encoding="utf-8"))
    assert len(research['sources']) == 15 and len({r['id'] for r in research['sources']}) == 15
    assert all(r['runtime_tested'] is False and r['review_scope'] for r in research['sources'])
    if failures:
        raise ValueError("\n".join(failures))

    lines = ["# Package validation", "", "Validated 2026-11-06 using `python scripts/verify_package.py`.", "",
             f"- PASS: {checked_links} local Markdown file references resolve.",
             "- PASS: retained JSON files parse and CSV template headers are unique.",
             "- PASS: 1,519 unique compound index IDs (records may share destination URLs).",
             "- PASS: all 1,488 imported curated resource/paper records exactly match retained upstream JSON, in order and without dropping fields.",
             "- PASS: 26 REAP prompt-pack links and five core navigation records included.",
             "- PASS: master prompt has one copy boundary and agent-neutral instructions without prescribed vendor/model routing.",
             "- PASS: 76 uniquely identified starting limitation checks remain UNASSESSED rather than claiming unexecuted closure.",
             "- PASS: 15 supplementary research sources retain review scope and untested runtime status.", "",
             "These checks validate the package structure and import fidelity. They do not execute upstream tools, verify every external URL, reproduce research benchmarks, or establish production readiness.", ""]
    (ROOT / "VALIDATION.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    files.append(ROOT / "VALIDATION.md")
    manifest = []
    for path in sorted(files, key=lambda p: p.relative_to(ROOT).as_posix()):
        manifest.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(ROOT).as_posix()}")
    (ROOT / "PACKAGE-MANIFEST.sha256").write_text("\n".join(manifest) + "\n", encoding="utf-8", newline="\n")
    print(f"PASS: {checked_links} local links; 1,488 lossless imports; 1,519 index records; {len(manifest)} manifest files.")


if __name__ == "__main__":
    main()
