"""Responses hosted-agent entry point and deterministic local runner."""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from product_launch_studio.config import AppSettings
from product_launch_studio.local import run_local_request


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Product Launch Studio.")
    parser.add_argument(
        "--local",
        metavar="REQUEST_JSON",
        help="Run deterministically from a request file without Azure calls.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.local:
        settings = AppSettings.from_environment(mode_override="local")
        request_path = Path(args.local)
        payload = json.loads(request_path.read_text(encoding="utf-8"))
        result = asyncio.run(run_local_request(payload, settings=settings))
        print(json.dumps(result, indent=2, sort_keys=True))
        return

    from dotenv import load_dotenv

    load_dotenv(override=False)
    settings = AppSettings.from_environment()
    if settings.mode != "hosted":
        raise RuntimeError("Use --local REQUEST_JSON for local mode.")

    from product_launch_studio.hosted import run_responses_server

    run_responses_server(settings)


if __name__ == "__main__":
    main()
