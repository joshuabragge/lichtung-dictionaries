# dictionaries/manual/ — dictionaries added by hand

For StarDict dictionaries you want mirrored here that aren't WikDict —
unlike `../wikdict/`, these are committed directly into git, since
one-off additions don't have the "monthly re-upload bloats history"
problem the automated mirror has.

## Before adding anything: the license rule

**Only add a dictionary you can confirm is actually licensed for
redistribution** — CC BY-SA, CC BY, GPL, public domain, or an explicit
grant from the source. This repo is public; anything committed here is
being redistributed the moment it's pushed.

**Do not add a dictionary converted from a source whose terms forbid
that**, even if the StarDict *format* itself is fine. dict.cc's
translation files are the concrete example: personal-use-only,
explicitly forbidding redistribution, regardless of what format you
convert them to. Converting a file to StarDict changes its format, not
its license. See `../../docs/why-separate-repo.md` for the full reasoning.

If you're not sure a source's license allows this, don't add it here —
keep it local (e.g. imported directly into the Lichtung app via its
folder-picker import) instead of committing it to a public repo.

## Naming convention

One folder per dictionary:

```
dictionaries/manual/<source>-<target>-<slug>/
    <basename>.ifo
    <basename>.idx      (or .idx.gz)
    <basename>.dict      (or .dict.dz)
```

- **`<source>` / `<target>`** — lowercase ISO 639-1 codes (639-3 if no
  639-1 code exists), same codes WikDict and LingQ both use. `source` is
  the headword language, `target` the language definitions are given in
  — same convention `../wikdict/` uses, so a language code always means
  the same thing everywhere in this repo.
- **`<slug>`** — short, lowercase, hyphen-separated identifier for where
  the dictionary came from (e.g. `freedict`, `jmdict`, `mueller7`). No
  spaces, no version numbers unless the source itself is meaningfully
  versioned.
- **Example**: `dictionaries/manual/de-en-freedict/`.
- Inside the folder: the StarDict trio exactly as extracted, any
  basename — this is the same shape Lichtung's own folder-picker import
  already expects (exactly one `.ifo` plus matching `.idx`/`.dict`
  siblings), so a folder here is already drag-and-drop compatible with
  that import flow even without any special support for this location.
- Add a short `SOURCE.md` inside the folder recording where the
  dictionary came from, its exact license, and why redistribution is
  confirmed permitted — required, not optional, given the license rule
  above.

**Out of scope for now:** the Lichtung app doesn't discover or download
from `dictionaries/manual/` at all — not a bug to fix, just not built.
This folder is a place to put a dictionary for a human to find and import
by hand today; wiring it into the app's "Browse Dictionaries" screen
(its own manifest, a second catalog source alongside the WikDict one)
would be a deliberate follow-on, not something assumed here.
