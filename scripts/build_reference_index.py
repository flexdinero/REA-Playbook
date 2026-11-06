"""Build local navigation without network access or executing upstream software."""

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "references"
SNAPSHOT = "0898a94bb7b1fecbddb890c8c8fbf637b7ab78c8"
INPUTS = ("rea-resources.json", "tool-resources.json", "papers.json")
EXPECTED = {"rea-resources.json": 123, "tool-resources.json": 1130, "papers.json": 235}


def markdown_text(value):
    return str(value or "").replace("\n", " ").replace("[", "\\[").replace("]", "\\]")


def main():
    records = []
    counts = {}
    for name in INPUTS:
        rows = json.loads((REFS / "awesome-rea" / name).read_text(encoding="utf-8"))
        if not isinstance(rows, list) or len(rows) != EXPECTED[name]:
            raise ValueError(f"Unexpected snapshot shape/count: {name}")
        counts[name] = len(rows)
        for row in rows:
            if not row.get("id") or not row.get("url"):
                raise ValueError(f"Missing upstream identity: {name}")
            records.append({
                "record_id": f"awesome-rea:{name}:{row['id']}",
                "origin": "Awesome-REA",
                "source_file": f"awesome-rea/{name}",
                "source_commit": SNAPSHOT,
                "local_review": "imported-not-independently-validated",
                "upstream": row,
            })

    file_index = json.loads((REFS / "upstream-file-index.json").read_text(encoding="utf-8"))
    reap = next(x for x in file_index["repos"] if x["repo"] == "JoasASantos/REA-Prompts")
    packs = [x for x in reap["tree"] if x["path"].endswith("/SKILL.md")]
    if len(packs) != 26:
        raise ValueError("Unexpected REAP pack count")
    for pack in packs:
        records.append({
            "record_id": f"reap:{pack['path']}",
            "origin": "REA-Prompts",
            "source_commit": reap["sha"],
            "local_review": "indexed-not-runtime-tested",
            "upstream": {"name": pack["path"].split("/")[-2], "url": pack["url"],
                         "kind": "prompt-pack", "targets": [], "blob_sha": pack["blob_sha"]},
        })

    for repo in ("morluto/rea", "NationalSecurityAgency/ghidra", "JoasASantos/REA-Prompts",
                 "JuneYaooo/rea-video", "reacher-z/Awesome-REA"):
        records.append({
            "record_id": f"core:{repo}", "origin": "core-navigation",
            "local_review": "selected-documentation-reviewed-not-runtime-tested",
            "upstream": {"name": repo, "url": f"https://github.com/{repo}",
                         "kind": "core-repository", "targets": []},
        })

    identifiers = [r["record_id"] for r in records]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("Duplicate compound record identity")
    document = {
        "schema_version": 1, "snapshot_date": "2026-11-06",
        "description": "Upstream records preserved; local verification is separate.",
        "counts": {**counts, "upstream_curated_records": sum(counts.values()),
                   "reap_prompt_packs": len(packs), "core_navigation": 5,
                   "total_index_records": len(records)},
        "records": records,
    }
    (REFS / "master-reference-index.json").write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    lines = ["# Complete master reference index", "",
             "Generated from preserved local snapshots. See [navigation and adoption rules](../REFERENCE-INDEX.md).", "",
             f"1,488 upstream curated records + 26 prompt packs + 5 core navigation records = {len(records):,} indexed records.", "",
             "Record counts are not unique tested-tool counts. Upstream claims/review labels are preserved, not independently verified here.", "",
             "Original descriptions, limits, review dates and evidence URLs are retained in [the JSON index](master-reference-index.json).", "",
             "Imported Awesome-REA data: [MIT notice](awesome-rea/LICENSE).", ""]
    grouped = {}
    for record in records:
        row = record["upstream"]
        group = f"{record['origin']} / {row.get('kind', 'resource')}"
        grouped.setdefault(group, []).append(record)
    for group in sorted(grouped):
        rows = grouped[group]
        lines.extend([f"## {group} ({len(rows)})", ""])
        for record in rows:
            row = record["upstream"]
            name = markdown_text(row.get("name") or row.get("title") or row.get("id"))
            tags = ", ".join(row.get("targets", [])) or "general"
            verification = row.get("verification", "navigation-only")
            date = row.get("verified_at", "date not specified")
            url = str(row["url"]).replace(" ", "%20").replace(")", "%29")
            lines.append(f"- [{name}]({url}) — {tags}; upstream: {verification}, {date}; local: {record['local_review']}.")
        lines.append("")
    (REFS / "MASTER-REFERENCE-INDEX.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(document["counts"], sort_keys=True))
    print("Kinds:", dict(Counter(r["upstream"].get("kind", "resource") for r in records)))


if __name__ == "__main__":
    main()
