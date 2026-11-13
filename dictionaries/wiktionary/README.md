# dictionaries/wiktionary/ — English Wiktionary extracts, one source

Twelve StarDict dictionaries for languages the WikDict mirror has no
headword dictionary for (see `../wikdict/`). All come from one place, so
the source, license and checksums are recorded once, here, instead of per
folder. Folder names are `<headword-language>-en/`; the gloss language is
always English. Headword codes follow the convention in `../manual/README.md`
(`sh` is Serbo-Croatian).

## Source
- Built by [xxyzz/wiktionary_stardict](https://github.com/xxyzz/wiktionary_stardict), release `20261029` (2026-10-29), one `<code>-en.tar.zst` asset per dictionary.
- Data: English Wiktionary, snapshot 2026-10-01, via Wikimedia Enterprise / Kiwix dumps as processed by that tool.

## License
**CC BY-SA 4.0**, the Wiktionary content license: https://creativecommons.org/licenses/by-sa/4.0/
Each `.ifo` states it: `description=Snapshot 2026-10-01, Wiktionary license CC BY-SA 4.0`.
CC BY-SA allows copying and redistribution with attribution and the same license. The upstream tool's repo is GPL-3.0-or-later, which covers its code; its output labels the data CC BY-SA 4.0, and CC BY-SA 4.0 content may be used inside GPL-3.0 works, so the two do not conflict.

**Attribution:** content from English Wiktionary (https://en.wiktionary.org) contributors, via xxyzz/wiktionary_stardict.

## Changes made here
None. Each folder is its archive extracted as-is (`.ifo`, `.idx`, `.dict.dz`, `.syn`, `.css`, and `res/` images where the archive has them). Verify with the archive SHA-256 below.

## Contents
| Folder | Dictionary | Headwords | `.syn` entries | SHA-256 of release archive |
|---|---|---|---|---|
| `af-en/` | Afrikaans-English | 6,657 | 8,411 | `e7ff990f2c13472a5ab88390f1df2c517e6264ea6f91115ab8b4aa31e7d37ccd` |
| `ar-en/` | Arabic-English | 151,695 | 1,700,936 | `04db651ae0c896e53a9924d2c1e39af8e7c678b14d7b9184fe40e9245dd722b4` |
| `fa-en/` | Persian-English | 17,463 | 121,421 | `d331aed9edc1ee5bf5e7847fe5990197b041179c7e7af873acc52824b8a892f4` |
| `he-en/` | Hebrew-English | 17,847 | 240,311 | `c7de256308d586210cc511870bc6c3096a3b42b2663f155e0b24f6aa7c3c3182` |
| `id-en/` | Indonesian-English | 37,129 | 48,242 | `f59c3504cfe18c6912e3d360f9cdbf3dfba261fd51f25b67c95ed8199cb5b8fe` |
| `is-en/` | Icelandic-English | 19,932 | 212,199 | `deb8482171fe81877da441b7e9fae5e70a8f487dc521534c16779bf7ad1921bb` |
| `ko-en/` | Korean-English | 55,552 | 395,791 | `c1d2454e7fcd5c7c11bf6dd065deaf8da089ccdf5ce08be2c668cedcdc9a8372` |
| `la-en/` | Latin-English | 206,068 | 2,197,472 | `b309279e482a1a08b0c56c16ccd895023f3fe1663175042e524b16414e8ecbae` |
| `ro-en/` | Romanian-English | 104,132 | 724,890 | `fa1371cf9d794b6af00276b16e33dbb30a2515ad417796340469347deef6b028` |
| `sh-en/` | Serbo-Croatian-English | 59,846 | 1,175,387 | `6c40608fbd89e3f67c610d66667756bc324eefcc237844f158e0ed1277de1e33` |
| `uk-en/` | Ukrainian-English | 32,859 | 825,955 | `812380796a7dd024d08ab77dfc48ebb33057455cd838bac0b02275a116c4bce2` |
| `zh-en/` | Chinese-English | 193,328 | 170,509 | `c33689735c5e424dac4a395c88933c486c875e3fbad793675acf89224bf7a562` |

## Notes
- Entries are full Wiktionary article HTML (`sametypesequence=h`). Lichtung's parser currently shows extra senses (pronunciation, examples, etymology) and ignores the `.syn` index, where inflected forms and alternate spellings live; the app-side fix is planned separately. The data here is intentionally untouched.
- `sh` is the only English-gloss Wiktionary extract covering Serbian and Croatian (LingQ `srp`, `hrv`); Cyrillic and most Latin spellings resolve only through `.syn`.
- `zh` adds Traditional headwords (LingQ `zh-t`); WikDict already has `zh`→`en`. Simplified forms resolve only through `.syn`.
- `la` and `id` appear in WikDict only as gloss targets, never as headwords.
- Cantonese (LingQ `hk`) is not covered; CC-CEDICT or CC-Canto would be the source.
- The Lichtung app does not read this folder yet.
