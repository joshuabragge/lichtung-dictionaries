# lichtung-dictionaries

Mirrored dictionary data for [Lichtung](https://github.com/joshuabragge/Web-Reader-for-LingQ)
(a Safari/Chrome/Firefox extension + iOS/macOS app for reading with LingQ
vocabulary highlighting) and its standalone in-app ereader. Lichtung's own
source is private; this repo exists only to host the one thing that
*needs* to be public — the redistributable dictionary data its app
downloads on demand.

**This repo holds no secrets and runs no automation of its own.** The
mirroring pipeline (fetching LingQ's current language list, then WikDict's
data for those languages) runs from Lichtung's private repo, which is
where the LingQ API credential that step needs actually lives — it stays
there, never here. That job's last step pushes the finished result into
this repo as a new Release, using a token scoped to *only* this one
repo's contents, so nothing crossing that boundary can read anything back
out of the private side. This repo is just where the output lands.

## What's here

- **`sync.py`, `lingq_languages.py`, `languages.json`**: the actual
  scripts that produce each release, kept here (MIT-licensed) for
  transparency and reuse — you can see exactly how a release was built,
  or run this yourself against your own language list. They aren't
  executed by anything in this repo; the private pipeline that actually
  runs them on a schedule lives elsewhere (above).
- **The dictionary data itself**, published only as [Release assets](../../releases) —
  never committed into this repo's git history. Each release has a
  `manifest.json` (pair list, file sizes, SHA-256 checksums) alongside the
  `wikdict-<source>-<target>.zip` files.

## Licensing — code vs. data

These are two separate things under two separate licenses:

- **The code in this repo** (the sync scripts) is original and licensed
  under [MIT](LICENSE) — free to reuse, including by anyone wanting to
  mirror WikDict for their own project.
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

Both scripts are stdlib-only Python — no dependencies to install.
