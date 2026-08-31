# Why this repo exists, and why the pipeline runs elsewhere

Moved out of the README to keep that short — this is the reasoning
behind the shape of this repo, for anyone (human or otherwise) who needs
the "why," not just the "what."

## Why WikDict, not other downloadable-dictionary sources

WikDict's data (sourced from Wiktionary via DBnary) is licensed
**Creative Commons Attribution-ShareAlike 4.0**, which explicitly permits
copying, modification, and redistribution provided attribution and
share-alike are honored. That's what makes mirroring it here legitimate.

A different well-known source, dict.cc, was evaluated for the same
purpose and rejected outright, not just deprioritized: its own terms grant
**personal use only**, explicitly forbid the data being "given away to
third parties or published in any way," require any program that reads
their format to itself be GPL-licensed, and forbid bundling their data
with a program at all. Downloaded files carry per-requester tracking
identifiers specifically to catch this kind of redistribution. Mirroring
that here would be straightforward copyright/ToS infringement, not a gray
area — which is why the license rule in `dictionaries/manual/README.md`
exists and isn't optional.

## Why this repo is separate from Lichtung's own source

Lichtung's app repo is private. That's not a detail to work around
quietly — it makes the original single-repo plan (device downloads a
release asset directly, no server in between) impossible as written:

- `GET /repos/{owner}/{repo}/releases` on a private repo returns 404
  without authentication.
- A release asset's `browser_download_url` also needs an `Authorization`
  header for a private repo — it only "works" in a browser because a
  logged-in session cookie covers it, not for a bare device request.
- The only way around that is shipping a token in the app that can read
  the private repo — and GitHub has no scope granular enough to grant
  "read this repo's releases" without also granting "read this repo's
  source." Any working token exposes the whole private codebase if
  extracted from the app binary.

So the data that needs to be fetched by an anonymous device lives here,
public, separate from the app's actual source.

## Why the mirror pipeline still runs in the private repo, not here

The pipeline that decides *what* to mirror has a step that calls LingQ's
own API to get the current language list, which needs a real LingQ
account credential. Even though a public repo's secrets aren't otherwise
exposed just by being public, there's no good reason for a passive
data-host repo to hold a production credential at all — so that whole
pipeline (language lookup, then the WikDict mirror itself) runs from the
private Lichtung repo, where the credential legitimately lives already,
and only its last step — publishing the finished Release — reaches into
this repo, authenticated with a token scoped to *only* this repo's
contents. That token can create releases here; it can't read anything
back out of the private side, and it can't touch anything in this repo
beyond releases either.

Net effect: this repo holds no secrets and runs no automation of its own.
`sync.py`/`lingq_languages.py` are kept here anyway, as MIT-licensed
reference copies — useful if anyone wants to see exactly how a release
was built, or run the same mirror against their own language list — but
they aren't wired to anything that executes in this repo.
