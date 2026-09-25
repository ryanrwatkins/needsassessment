"""Render the canonical CSV as accessible, searchable HTML before Quarto builds."""

import argparse
import csv
import html
import json
import logging
import os
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
LOGGER = logging.getLogger(__name__)
FIELDS = [
    "id",
    "title",
    "author",
    "year",
    "year_original",
    "resource_type",
    "description",
    "url",
    "topics",
    "language",
    "journal",
    "publisher",
    "doi",
    "pages",
    "volume",
    "issue",
    "edition",
    "editors",
    "source_urls",
    "record_status",
    "extra_fields",
]


def values(value: str) -> list[str]:
    """Split the documented multi-value delimiter."""
    return [part.strip() for part in value.split(";") if part.strip()]


def read_rows(path: Path) -> list[dict[str, str]]:
    """Read quoted UTF-8 CSV and reject missing columns or malformed rows."""
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            raise ValueError(f"{path}: expected columns {FIELDS}")
        rows = list(reader)
    if any(None in row or None in row.values() for row in rows):
        raise ValueError("Malformed CSV: wrong number of fields")
    validate(rows)
    return rows


def validate(rows: list[dict[str, str]]) -> None:
    """Fail the build for unsafe links, invalid dates, and duplicate identifiers."""
    seen = set()
    for row in rows:
        if not row["id"].strip() or row["id"] in seen or not row["title"].strip():
            raise ValueError("Resources require unique IDs and nonempty titles")
        seen.add(row["id"])
        if row["year"] and not re.fullmatch(r"[0-9]{4}", row["year"]):
            raise ValueError("Year must be a four-digit year or blank")
        for url in [row["url"], *values(row["source_urls"])]:
            if url and (
                urlsplit(url).scheme not in {"https", "http"}
                or not urlsplit(url).netloc
            ):
                raise ValueError(f"Invalid resource URL: {url}")


def select_control(rows: list[dict[str, str]], field: str, label: str) -> str:
    """Build filter choices directly from the catalog."""
    options = sorted({v for row in rows for v in values(row[field])})
    choices = '<option value="">All</option>' + "".join(
        f"<option>{html.escape(v)}</option>" for v in options
    )
    return f'<label>{label}<select id="filter-{field}">{choices}</select></label>'


def render_row(row: dict[str, str]) -> str:
    """Escape catalog text and attributes, keeping descriptions searchable."""
    escaped = {key: html.escape(value, quote=True) for key, value in row.items()}
    attributes = " ".join(
        f'data-{field.replace("_", "-")}="{html.escape(json.dumps(values(row[field])))}"'
        for field in ["topics", "resource_type", "language", "year"]
    )
    title = escaped["title"]
    if row["url"]:
        title = f'<a href="{escaped["url"]}">{title}</a>'
    recorded = escaped["year"] if row["year"] else "Not available"
    return f"""<tr class="resource-row" id="{escaped["id"]}" {attributes}
 data-title="{escaped["title"]}" data-date="{escaped["year"]}">
<td><strong>{title}</strong>
<details><summary>Details</summary><p>{escaped["description"] or "No description recorded."}</p>
<p>{html.escape(" · ".join(row[f] for f in ["journal", "publisher", "volume", "issue", "pages", "doi"] if row[f]))}</p><p>Reference recovery: {escaped["record_status"]}</p></details></td>
<td>{escaped["author"] or "Not available"}</td>
<td>{escaped["resource_type"] or "Not available"}</td>
<td>{recorded}</td></tr>"""


def main(
    source: Path = ROOT / "data/resources.csv", output: Path = ROOT / "_catalog.html"
) -> None:
    """Build from CSV; no network or third-party runtime packages are required."""
    rows = read_rows(source)
    topics = sorted({v for row in rows for v in values(row["topics"])})
    buttons = (
        '<button type="button" data-topic="" aria-pressed="true">All topics</button>'
    )
    buttons += "".join(
        f'<button type="button" data-topic="{html.escape(t)}" aria-pressed="false">{html.escape(t)}</button>'
        for t in topics
    )
    controls = "".join(
        select_control(rows, f, label)
        for f, label in [
            ("resource_type", "Resource type"),
            ("language", "Language"),
            ("year", "Year"),
        ]
    )
    output.write_text(
        f"""<div id="resource-catalog">
<div id="catalog-controls" hidden>
<div class="topic-buttons" role="group" aria-label="Topics">{buttons}</div>
<label class="catalog-search">Search resources<input id="catalog-search" type="search" placeholder="Search titles, authors, and references"></label>
<div class="catalog-filters">{controls}
<label>Sort by<select id="catalog-sort"><option value="title">Title A–Z</option><option value="newest">Year: newest first</option><option value="oldest">Year: oldest first</option></select></label>
<button id="catalog-reset" type="button">Clear filters</button></div></div>
<p id="catalog-count" role="status" aria-live="polite">{len(rows)} resources</p>
<noscript><p>Search and filters require JavaScript. All resources are listed below.</p></noscript>
<div class="catalog-table-wrap"><table class="catalog-table">
<caption class="visually-hidden">Recovered needs assessment references</caption>
<thead><tr><th scope="col">Resource</th><th scope="col">Author</th><th scope="col">Type</th><th scope="col">Year</th></tr></thead>
<tbody>{''.join(render_row(row) for row in rows)}</tbody></table></div>
<p id="catalog-empty" hidden>No resources match. Try another search or clear the filters.</p>
</div>""",
        encoding="utf-8",
    )
    LOGGER.info("Built %s resources from %s into %s", len(rows), source, output)


def index_catalog(source: Path, search_path: Path) -> None:
    """Add resource-level search hits because Quarto omits raw HTML from its index."""
    rows = read_rows(source)
    entries = json.loads(search_path.read_text(encoding="utf-8"))
    entries = [entry for entry in entries if not entry.get("catalog_resource")]
    for row in rows:
        href = f"resources.html#{row['id']}"
        entries.append(
            {
                "objectID": href,
                "href": href,
                "title": "Resources",
                "section": row["title"],
                "text": " ".join(
                    row[field]
                    for field in [
                        "title",
                        "description",
                        "topics",
                        "resource_type",
                        "author",
                        "language",
                        "journal",
                        "year",
                    ]
                ),
                "catalog_resource": True,
            }
        )
    search_path.write_text(json.dumps(entries, ensure_ascii=False), encoding="utf-8")
    LOGGER.info("Indexed %s resources for site search", len(rows))


def cli() -> None:
    """Run the pre-render builder or post-render site-search integration."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", action="store_true")
    args = parser.parse_args()
    if args.index:
        output = ROOT / os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site")
        index_catalog(ROOT / "data/resources.csv", output / "search.json")
    else:
        main()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    cli()
