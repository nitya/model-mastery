#!/usr/bin/env python3
"""Read-only catalog matching used by the preflight scripts."""

import argparse
import json
import os
import sys

parser = argparse.ArgumentParser(
    description="Verify configured workshop models against CATALOG_JSON."
)
parser.parse_args()

def flatten_models(value):
    if isinstance(value, dict):
        if isinstance(value.get("model"), dict):
            yield value
        for child in value.values():
            yield from flatten_models(child)
    elif isinstance(value, list):
        for child in value:
            yield from flatten_models(child)


catalog = json.loads(os.environ["CATALOG_JSON"])
rows = list(flatten_models(catalog))
purposes = {
    "campaign coordinator": "CAMPAIGN_COORDINATOR",
    "visual understanding": "VISUAL_UNDERSTANDING",
    "campaign reasoning": "CAMPAIGN_REASONING",
    "adaptive copy (initial)": "ADAPTIVE_COPY",
    "adaptive copy (router)": "MODEL_ROUTER",
    "creative image": "CREATIVE_IMAGE",
}
failed = False
for purpose, prefix in purposes.items():
    expected = {
        "name": os.environ[f"{prefix}_MODEL_NAME"],
        "version": os.environ[f"{prefix}_MODEL_VERSION"],
        "format": os.environ[f"{prefix}_MODEL_FORMAT"],
        "sku": os.environ[f"{prefix}_MODEL_SKU"],
    }
    matches = []
    for row in rows:
        model = row.get("model", {})
        if (
            str(model.get("name", "")).lower() == expected["name"].lower()
            and str(model.get("version", "")).lower() == expected["version"].lower()
            and str(model.get("format", "")).lower() == expected["format"].lower()
        ):
            matches.append(row)
    sku_names = {
        str(sku.get("name", "")).lower()
        for row in matches
        for sku in row.get("skus", row.get("model", {}).get("skus", []))
    }
    if matches and (not sku_names or expected["sku"].lower() in sku_names):
        print(f"[OK] {purpose}: exact model/version/format and SKU found.")
    else:
        print(
            f"[ACTION] {purpose}: catalog did not confirm "
            f"{expected['format']}/{expected['name']}/{expected['version']} "
            f"with {expected['sku']}.",
            file=sys.stderr,
        )
        failed = True
if failed:
    print(
        "[ACTION] Update the private env file from the live catalog. "
        "For visual understanding, use the documented GPT-5.4 fallback if Claude is unavailable.",
        file=sys.stderr,
    )
    sys.exit(1)
