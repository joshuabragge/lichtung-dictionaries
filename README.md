# lichtung-dictionaries

Dictionary data for [Lichtung](https://lichtung.xyz) — a reading app that
highlights vocabulary and shows definitions as you read.

- **`dictionaries/wikdict/`** — automated mirror of [WikDict](https://www.wikdict.com)'s
  CC BY-SA dictionaries, published as dated [Releases](../../releases).
- **`dictionaries/manual/`** — dictionaries added by hand. See its own
  `README.md` for the folder-naming convention and the license rule
  before adding one.
- **`sync.py`, `lingq_languages.py`, `languages.json`** — the scripts that
  build the automated mirror, kept here for transparency (MIT-licensed —
  free to reuse). They don't run from this repo; see `CLAUDE.md`.

**Licensing:** the code here is [MIT](LICENSE). The dictionary data in
Releases is not ours — it's WikDict's own CC BY-SA 4.0 data (Wiktionary
via DBnary). See `CLAUDE.md` and `docs/` for the full detail.
