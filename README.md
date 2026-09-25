# NeedsAssessment.org

This repository preserves and republishes the static content of the former
NeedsAssessment.org WordPress site as a Quarto website.

The public site is published at
https://ryanrwatkins.github.io/needsassessment/.

## What is here

- Six readable Quarto pages built from the original navigation: Home, Overview,
  Foundations, Resources, Connect, and Expert Chat.
- A CSV-backed bibliography of recovered books, articles, and chapters. The
  Resources page supports topic, text, type, language, and publication-year
  filtering without a separate database.
- Downloaded first-party files that could be retrieved from the Internet
  Archive, plus a local archive of the source HTML and retrieval metadata.

## Update the catalog

Edit `data/resources.csv`, retaining its header and UTF-8 CSV format, then run:

```bash
python3 scripts/build_catalog.py
quarto render
```

`scripts/build_catalog.py` validates the CSV before building the catalog. The
published page always derives its catalog from this one editable file.

## Local development

Install Quarto and the development checks, then run:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
ruff check scripts tests
black --check scripts tests
bandit -r scripts
quarto preview
```

GitHub Actions runs those checks and publishes a successful `main` build to
GitHub Pages.

## Recovery record

See `RECOVERY_REPORT.md` for the retrieval scope, archive limitations, and
provenance. `archive/` contains source evidence and is intentionally not part
of the public site build.
