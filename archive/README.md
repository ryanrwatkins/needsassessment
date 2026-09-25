# Archive evidence

This directory is the private-to-the-repository recovery record; Quarto does
not publish it to the site.

- `manifest.json` is the inventory of requested URLs and their recovery status.
- `html/` contains raw recovered WordPress HTML.
- individual JSON files retain per-URL retrieval metadata.
- `listing-observations.json` records bibliography rows observed in the
  recovered lists.
- `removed-injections.json` records source content deliberately excluded from
  public conversion.

The recovered raw source may contain malformed markup or historical spam. Use
the Quarto pages and CSV as the public-facing reconstruction.
