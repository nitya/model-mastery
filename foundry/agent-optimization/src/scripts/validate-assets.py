#!/usr/bin/env python3
"""Validate workshop data and XML locally without network access."""

import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET


parser = argparse.ArgumentParser()
parser.add_argument("--root", type=Path, required=True)
args = parser.parse_args()
root = args.root.resolve()

required = [
    root / "azure.yaml",
    root / "infra/main.bicep",
    root / "data/campaign-brief.md",
    root / "data/eval-cases.jsonl",
    root / "data/router-complexity-cases.jsonl",
    root / "data/evaluators/campaign-quality.yaml",
    root / "assets/contoso-trailpack.svg",
]
missing = [str(path) for path in required if not path.is_file()]
if missing:
    raise SystemExit("Missing required files:\n" + "\n".join(missing))

for path, expected_count in [
    (root / "data/eval-cases.jsonl", range(5, 9)),
    (root / "data/router-complexity-cases.jsonl", range(3, 4)),
]:
    rows = []
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row.get("query"), str) or not isinstance(
            row.get("expected_behavior"), str
        ):
            raise SystemExit(f"{path}:{line_number}: query and expected_behavior are required strings")
        rows.append(row)
    if len(rows) not in expected_count:
        raise SystemExit(f"{path}: expected {expected_count}, found {len(rows)} rows")
    print(f"[OK] {path.relative_to(root)}: {len(rows)} valid JSONL rows")

ET.parse(root / "assets/contoso-trailpack.svg")
print("[OK] assets/contoso-trailpack.svg: valid XML")
