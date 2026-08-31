#!/usr/bin/env python3
"""Mirror WikDict's CC BY-SA StarDict dictionaries into a local output
directory, ready to be uploaded as GitHub Release assets.

See README.md for the design and licensing rationale (WikDict's data is
CC BY-SA -- explicitly redistributable with attribution, unlike dict.cc's
personal-use-only terms, which is why this script exists only for
WikDict). The consuming app's own design doc is
joshuabragge/Web-Reader-for-LingQ's docs/wikdict-mirror-plan.md (private).

Usage:
    python3 sync.py --out dist/wikdict [--all] [--languages languages.json]

Stdlib only -- no pip install needed, so this runs in CI with nothing but
a Python interpreter. Network access required (fetches from
download.wikdict.com).
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
import zipfile
from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

LISTING_URL = "https://download.wikdict.com/dictionaries/stardict/"
FILE_URL_TEMPLATE = "https://download.wikdict.com/dictionaries/stardict/{filename}"
LICENSE = "CC-BY-SA-4.0"
ATTRIBUTION = "Data from Wiktionary via DBnary, via WikDict (wikdict.com)"

# Matches e.g. "wikdict-de-en.zip". Deliberately does not assume anything
# about which pairs exist -- the listing itself is the source of truth.
PAIR_RE = re.compile(r'href="(wikdict-([a-z]{2,3})-([a-z]{2,3})\.zip)"')


@dataclass
class PairEntry:
    source: str
    target: str
    filename: str
    sizeBytes: int
    sha256: str


def fetch(url: str, timeout: int = 60) -> bytes:
    req = Request(url, headers={"User-Agent": "wikdict-mirror-sync/1 (+lichtung app)"})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read()


def list_available_pairs() -> list[tuple[str, str, str]]:
    """Returns (filename, source, target) tuples actually present on the
    server -- never a guessed combination matrix."""
    html = fetch(LISTING_URL).decode("utf-8", errors="replace")
    seen = set()
    pairs = []
    for filename, source, target in PAIR_RE.findall(html):
        if filename in seen:
            continue
        seen.add(filename)
        pairs.append((filename, source, target))
    return pairs


def load_allowlist(path: Path) -> set[str]:
    data = json.loads(path.read_text())
    return set(data["languages"])


def validate_stardict_zip(zip_bytes: bytes, filename: str) -> bool:
    """Same shape check DictionaryStore.importDictionary does on-device:
    exactly one .ifo plus a same-basename .idx(.gz)/.dict(.dz) pair. A
    malformed or unexpectedly-shaped upstream zip is skipped with a
    warning rather than failing the whole run."""
    try:
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            names = zf.namelist()
    except zipfile.BadZipFile:
        print(f"  SKIP {filename}: not a valid zip", file=sys.stderr)
        return False

    ifo_files = [n for n in names if n.lower().endswith(".ifo")]
    if len(ifo_files) != 1:
        print(f"  SKIP {filename}: expected exactly one .ifo, found {len(ifo_files)}", file=sys.stderr)
        return False

    basename = ifo_files[0][: -len(".ifo")]
    has_idx = any(n in (basename + ".idx", basename + ".idx.gz") for n in names)
    has_dict = any(n in (basename + ".dict", basename + ".dict.dz") for n in names)
    if not (has_idx and has_dict):
        print(f"  SKIP {filename}: missing matching .idx/.dict siblings for {basename}", file=sys.stderr)
        return False

    return True


def sync(out_dir: Path, allowlist: set[str] | None) -> list[PairEntry]:
    print(f"Fetching listing: {LISTING_URL}")
    available = list_available_pairs()
    print(f"  {len(available)} pair files found on server")

    if allowlist is not None:
        available = [
            (filename, source, target)
            for (filename, source, target) in available
            if source in allowlist and target in allowlist
        ]
        print(f"  {len(available)} pairs remain after allowlist filter")

    out_dir.mkdir(parents=True, exist_ok=True)
    entries: list[PairEntry] = []

    for filename, source, target in sorted(available):
        url = FILE_URL_TEMPLATE.format(filename=filename)
        print(f"Downloading {filename} ...")
        try:
            data = fetch(url, timeout=120)
        except (URLError, HTTPError) as e:
            print(f"  SKIP {filename}: download failed ({e})", file=sys.stderr)
            continue

        if not validate_stardict_zip(data, filename):
            continue

        sha256 = hashlib.sha256(data).hexdigest()
        (out_dir / filename).write_bytes(data)
        entries.append(PairEntry(
            source=source, target=target, filename=filename,
            sizeBytes=len(data), sha256=sha256,
        ))
        print(f"  OK ({len(data):,} bytes, sha256={sha256[:12]}...)")

    return entries


def write_manifest(out_dir: Path, entries: list[PairEntry]) -> None:
    from datetime import datetime, timezone

    manifest = {
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "license": LICENSE,
        "attribution": ATTRIBUTION,
        "sourceListing": LISTING_URL,
        "pairs": [asdict(e) for e in entries],
    }
    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(f"Wrote {manifest_path} ({len(entries)} pairs)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True, help="Output directory for mirrored zips + manifest.json")
    parser.add_argument("--languages", type=Path, default=Path(__file__).parent / "languages.json",
                         help="Allowlist config (ignored with --all)")
    parser.add_argument("--all", action="store_true", help="Mirror every pair present on the server, ignoring the allowlist")
    args = parser.parse_args()

    allowlist = None if args.all else load_allowlist(args.languages)
    entries = sync(args.out, allowlist)
    if not entries:
        print("No pairs mirrored -- nothing to write a manifest for.", file=sys.stderr)
        return 1

    write_manifest(args.out, entries)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
