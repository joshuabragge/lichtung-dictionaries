#!/usr/bin/env python3
"""Fetch LingQ's current language catalog and write it in the same
{"languages": [...]} shape sync.py's --languages flag expects.

This replaces a hand-maintained allowlist with the live source of truth:
whatever languages LingQ itself supports right now, per
GET /api/v2/languages/ (the same endpoint and tolerant parse shape as the
Lichtung app's own Swift APIClient.getLanguages()/parseLanguages,
reimplemented here since this script has no Swift runtime to call into).

Run fresh on every scheduled mirror (see CLAUDE.md) rather than caching/
committing the result back to the repo -- one API call per month costs
nothing and means the allowlist can never go stale between runs.
languages.json stays checked in as the fallback the real (privately-run)
workflow uses when LINGQ_API_KEY is unavailable (e.g. a local dry run) or
the call fails.

Usage:
    LINGQ_API_KEY=... python3 lingq_languages.py --out languages.generated.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

LINGQ_LANGUAGES_URL = "https://www.lingq.com/api/v2/languages/"


def fetch_language_codes(api_key: str, timeout: int = 30) -> list[str]:
    req = Request(
        LINGQ_LANGUAGES_URL,
        headers={
            "Authorization": f"Token {api_key}",
            "User-Agent": "wikdict-mirror-sync/1 (+lichtung app)",
        },
    )
    with urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read())

    # Same tolerant shape as APIClient.parseLanguages: usually a bare
    # array of {"code": ..., ...} rows, but tolerate a dict wrapping one.
    if isinstance(data, dict):
        rows = next(
            (v for v in data.values() if isinstance(v, list) and any(isinstance(r, dict) and "code" in r for r in v)),
            [],
        )
    else:
        rows = data

    codes = sorted({row["code"].lower() for row in rows if isinstance(row, dict) and row.get("code")})
    return codes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Output path for the generated {\"languages\": [...]} file")
    args = parser.parse_args()

    api_key = os.environ.get("LINGQ_API_KEY")
    if not api_key:
        print("LINGQ_API_KEY not set -- nothing to fetch.", file=sys.stderr)
        return 1

    try:
        codes = fetch_language_codes(api_key)
    except (URLError, HTTPError) as e:
        print(f"LingQ languages fetch failed: {e}", file=sys.stderr)
        return 1

    if not codes:
        print("LingQ returned zero language codes -- refusing to write an empty allowlist.", file=sys.stderr)
        return 1

    with open(args.out, "w") as f:
        json.dump({"languages": codes}, f, indent=2, sort_keys=True)
        f.write("\n")
    print(f"Wrote {len(codes)} language codes to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
