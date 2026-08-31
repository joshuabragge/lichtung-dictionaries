# dictionaries/wikdict/ — placeholder, not the real data

The automated WikDict mirror publishes to this repo's
[Releases](../../../../releases) page, not to this folder. Each release is
tagged `wikdict-mirror-YYYY-MM-DD` and holds:

- `wikdict-<source>-<target>.zip` — one per mirrored language pair,
  `source` = headword language, `target` = the language definitions are
  given in (both lowercase ISO 639-1 codes, or 639-3 where no 639-1 code
  exists — same codes WikDict and LingQ both use). This naming is fixed by
  WikDict's own upstream filenames; don't rename these if you download one.
- `manifest.json` — every pair in that release, with size and a SHA-256
  checksum, plus the license/attribution string.

This folder exists only so the repo's layout is discoverable — the data
itself stays out of git history on purpose (a monthly mirror re-uploading
every pair's full binary would bloat this repo's history for no benefit;
Releases don't have that problem). See `../../CLAUDE.md` and
`../../docs/why-separate-repo.md` for why.
