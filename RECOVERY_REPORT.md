# Recovery report

## Scope

The site was reconstructed from the Internet Archive version requested by the
project owner (`2026-01-01 05:02:02 UTC`) and, where that capture did not
return a resource, from the Archive's closest available historical captures.
The original WordPress database was not available.

The recovery collected all pages from the visible original navigation. The
current public build focuses on Home, Overview, Foundations, Resources, Guide,
and FAQ; Connect and Expert Chat were intentionally removed from public
navigation. The recovered Guide to Assessing Needs now has its own page.

## Results

The recovery inventory contains 402 requested URLs. 203 were recovered and
199 did not have a usable Archive response. The recovered material includes
171 HTML documents and 32 first-party downloadable assets. Archive response
captures span 2016, 2022–2026; the closest available capture was retained for
each successful item rather than asserting that every item came from one date.

The bibliography CSV contains 247 unique original reference IDs. 133 archive
record pages were recovered; records with no recovered detail remain in the
catalog as listing-only entries, with their title, author, and publication year
as shown in the archived bibliography listing.

## Provenance and limitations

- `archive/manifest.json` records each requested URL, status, resolved archive
  capture URL, and local path where recovered.
- `archive/listing-observations.json` preserves the bibliography-listing facts
  used to create CSV rows.
- `archive/html/` preserves the recovered source HTML. `assets/` holds
  recovered first-party downloads.
- Metadata in the original Participants Database was occasionally incomplete
  or malformed. Those values are retained in `extra_fields`; this project does
  not infer missing bibliographic facts.
- Numerous single-record pages and some legacy images/audio files had no
  usable archived response. Their source pages and all available items remain
  documented in the manifest.
- The original contact form and an original local-file case-study link could
  not be restored because neither is present in the Archive. The Contact page
  directs visitors to GitHub issues instead.
- A hidden pharmaceutical spam block present in recovered WordPress HTML was
  removed only from the public conversion. Its removal is logged in
  `archive/removed-injections.json`; raw source evidence is retained.

## Preservation guidance

Do not overwrite existing archive evidence with an unverified retrieval. A
future recovery should add new evidence, update `archive/manifest.json`, then
rebuild the CSV and Quarto pages.
