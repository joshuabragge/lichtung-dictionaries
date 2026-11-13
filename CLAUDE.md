# lichtung-dictionaries

Dictionary data host for [Lichtung](https://lichtung.xyz) (iOS/macOS app +
Safari/Chrome/Firefox extension; source is a separate private repo). This
repo exists only because that source repo is private, and a private
repo's release assets can't be fetched by an unauthenticated device — see
`docs/why-separate-repo.md` for the full reasoning. This repo itself is
deliberately simple: no secrets, no GitHub Actions workflow, nothing that
executes. It's a public data host and a landing place for manually-added
dictionaries, nothing more.

## Layout

| Path | What |
|---|---|
| `dictionaries/wikdict/` | Placeholder only — the automated WikDict mirror publishes to this repo's [Releases](../../releases), not a git-tracked folder, to avoid bloating history with monthly binary re-uploads. See its own `README.md`. |
| `dictionaries/wiktionary/` | English Wiktionary extracts from one third-party source (xxyzz/wiktionary_stardict), git-tracked, one `<code>-en/` folder per language WikDict lacks. Source, CC BY-SA 4.0 license and per-archive checksums are recorded once in its `README.md`. Same rule as `manual/`: confirm the license before adding. |
| `dictionaries/manual/` | Dictionaries added by hand, one folder per dictionary, git-tracked (infrequent additions, unlike the monthly mirror, so no bloat concern here). **Naming convention and the license rule are in its own `README.md` — read that before adding anything.** The app doesn't discover this folder — out of scope for now, not a bug. |
| `sync.py`, `lingq_languages.py`, `languages.json` | The actual scripts behind the WikDict mirror, kept here (MIT) for transparency and reuse. **Not wired to any workflow in this repo** — see "Where the pipeline actually runs" below. |
| `LICENSE` | MIT — covers the code in this repo only, not the dictionary data. |
| `docs/` | Deeper design rationale that doesn't need to be in the README — why this repo exists, why the pipeline runs elsewhere, licensing detail per data source. |

## Where the pipeline actually runs

Not here. The private Lichtung app repo runs the actual mirror on a
schedule (fetch LingQ's current language list, mirror WikDict's data for
those languages) and publishes the result into this repo's Releases via a
fine-grained token scoped to only this repo's contents. That's deliberate:
the LingQ API key that step needs should never live in a public repo, even
though GitHub secrets aren't otherwise exposed by repo visibility alone —
see `docs/why-separate-repo.md`.

Practical effect: don't expect to find a workflow file here, and don't add
one that needs `LINGQ_API_KEY` — that's a smell that pipeline logic is
leaking back into the wrong repo. `sync.py`/`lingq_languages.py` staying
here is for transparency/reuse only.

## Conventions

- **Never commit dictionary data (zips, `.ifo`/`.idx`/`.dict` files) from
  the automated mirror into git.** It ships as Release assets only —
  `dictionaries/wikdict/` stays a placeholder.
- **Manually-added dictionaries (`dictionaries/manual/`) and single-source extracts (`dictionaries/wiktionary/`) are the exception** — small, one-time
  additions are fine to commit directly under `dictionaries/manual/`,
  following its naming convention.
- **Before adding any dictionary by hand, confirm its license actually
  permits redistribution** (CC BY-SA, GPL, public domain, etc.). This repo
  is public. A dictionary whose source terms are personal-use-only or
  forbid redistribution (dict.cc's translation files are the concrete
  example that came up building this — see `docs/why-separate-repo.md`)
  must never go here, converted or not — converting a format doesn't
  change what the license allows.
- Any link to the Lichtung app itself should point at
  [lichtung.xyz](https://lichtung.xyz), not the private source repo —
  a GitHub link there is a dead end for anyone outside the org.
