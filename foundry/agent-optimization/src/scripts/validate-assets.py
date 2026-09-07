#!/usr/bin/env python3
"""Validate workshop data and the attributed PNG locally without network access."""

import argparse
import json
from pathlib import Path
import struct
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
    root / "assets/traillite-daypack.png",
    root / "assets/workshop-banner.svg",
    root / "assets/PROVENANCE.md",
    root / "assets/contoso-web-MIT-LICENSE.md",
]
missing = [str(path) for path in required if not path.is_file()]
if missing:
    raise SystemExit("Missing required files:\n" + "\n".join(missing))

provenance = (root / "assets/PROVENANCE.md").read_text(encoding="utf-8")
for marker in (
    "https://github.com/Azure-Samples/contoso-web",
    "e13b0d346bdc0f2139552df6b9268cbe71b5b644",
    "public/images/16/1b0d996c-bf9a-439b-8341-77ee41dc5859.png",
    "public/products.json",
    "public/manuals/product_info_16.md",
    "MIT",
):
    if marker not in provenance:
        raise SystemExit(f"assets/PROVENANCE.md: missing attribution marker {marker!r}")
print("[OK] assets/PROVENANCE.md: source, commit, paths, and license recorded")

license_text = (root / "assets/contoso-web-MIT-LICENSE.md").read_text(encoding="utf-8")
if "MIT License" not in license_text or "Copyright (c) Microsoft Corporation" not in license_text:
    raise SystemExit("assets/contoso-web-MIT-LICENSE.md: expected upstream MIT license text")
print("[OK] assets/contoso-web-MIT-LICENSE.md: upstream MIT license present")

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

png_path = root / "assets/traillite-daypack.png"
with png_path.open("rb") as png:
    signature = png.read(8)
    chunk_length = png.read(4)
    chunk_type = png.read(4)
    dimensions = png.read(8)

if signature != b"\x89PNG\r\n\x1a\n":
    raise SystemExit(f"{png_path}: invalid PNG signature")
if len(chunk_length) != 4 or struct.unpack(">I", chunk_length)[0] != 13:
    raise SystemExit(f"{png_path}: missing 13-byte IHDR chunk")
if chunk_type != b"IHDR" or len(dimensions) != 8:
    raise SystemExit(f"{png_path}: missing PNG dimensions")

width, height = struct.unpack(">II", dimensions)
if (width, height) != (1024, 1024):
    raise SystemExit(f"{png_path}: expected 1024x1024, found {width}x{height}")
print(f"[OK] {png_path.relative_to(root)}: valid PNG, {width}x{height}")

ET.parse(root / "assets/workshop-banner.svg")
print("[OK] assets/workshop-banner.svg: valid XML")
