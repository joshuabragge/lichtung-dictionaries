# lichtung-dictionaries

Mirrored dictionary data for [Lichtung](https://github.com/joshuabragge/Web-Reader-for-LingQ)
(a Safari/Chrome/Firefox extension + iOS/macOS app for reading with LingQ
vocabulary highlighting) and its standalone in-app ereader. Lichtung's own
source is private; this repo exists only to host the one thing that
*needs* to be public — the redistributable dictionary data its app
downloads on demand — decoupled from the private app repo so the app never
needs a credential that could also read Lichtung's source.

## What's here

- **This repo's own code** (`sync.py`, `lingq_languages.py`,
  `languages.json`, `.github/workflows/mirror.yml`): a small pipeline that
  mirrors [WikDict](https://www.wikdict.com)'s StarDict-format bilingual
  dictionaries, filtered to whatever languages
  [LingQ](https://www.lingq.com) currently supports, and publishes the
  result as a dated GitHub Release.
- **The dictionary data itself**, published only as [Release assets](../../releases) —
  never committed into this repo's git history. Each release has a
  `manifest.json` (pair list, file sizes, SHA-256 checksums) alongside the
  `wikdict-<source>-<target>.zip` files.

## Licensing — code vs. data

These are two separate things under two separate licenses:

- **The code in this repo** (the sync scripts and workflow) is original
  and licensed under [MIT](LICENSE) — free to reuse, including by anyone
  wanting to mirror WikDict for their own project.
- **The dictionary data in each release** is **not** ours — it's WikDict's
  own [Creative Commons Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
  data, sourced from Wiktionary via [DBnary](http://kaiko.getalp.org/about-dbnary/).
  CC BY-SA explicitly permits this kind of mirroring/redistribution,
  provided attribution is kept — which is why every release's
  `manifest.json` carries an `attribution` field, and why this README says
  so plainly: **dictionary data credit: Wiktionary via DBnary, via
  WikDict (wikdict.com), CC BY-SA 4.0.**

This repo deliberately mirrors only WikDict, never other
"downloadable-dictionary" sources — see the Lichtung app repo's
`docs/wikdict-mirror-plan.md` for why (short version: WikDict's license
explicitly allows this; a different well-known source, dict.cc, was
evaluated and rejected outright because its terms forbid it).

## Why a separate repo from the app itself

The app downloads a release's assets directly, device to GitHub, with no
server of Lichtung's own in the loop. That only works unauthenticated
because this repo is public — a private repo's release assets require a
token to fetch even by direct URL, and no GitHub token can be scoped to
"just this repo's releases" without also being able to read that repo's
source. Keeping the mirrored (already-public-by-license) data here, and
the app's actual source private and separate, means the app never ships a
credential that could expose anything it shouldn't.

## Running the mirror yourself

```bash
python3 sync.py --out dist/wikdict --languages languages.json
# or, to fetch the language allowlist live from LingQ instead of the
# checked-in fallback:
LINGQ_API_KEY=... python3 lingq_languages.py --out /tmp/languages.generated.json
python3 sync.py --out dist/wikdict --languages /tmp/languages.generated.json
```

`.github/workflows/mirror.yml` runs this on a monthly schedule (plus
manual `workflow_dispatch`) and publishes the result as a
`wikdict-mirror-YYYY-MM-DD` release. It needs one repo secret,
`LINGQ_API_KEY`, to fetch the live language allowlist — falls back to the
checked-in `languages.json` if that secret is missing or the call fails.
