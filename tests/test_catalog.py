"""CSV validation and build behavior."""

import csv
import importlib.util
import json
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "build_catalog", Path(__file__).parents[1] / "scripts/build_catalog.py"
)
catalog = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(catalog)


@pytest.fixture
def source(tmp_path: Path) -> Path:
    path = tmp_path / "resources.csv"
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=catalog.FIELDS)
        writer.writeheader()
        writer.writerow(
            dict.fromkeys(catalog.FIELDS, "")
            | {
                "id": "one",
                "title": 'A, "quoted" <title>',
                "description": "Two lines\nof text & detail.",
                "url": "https://example.com/",
                "topics": "Tutorials; Examples",
                "year": "2025",
                "source_urls": "https://web.archive.org/",
            }
        )
    return path


def test_main_preserves_csv_and_escapes_html(source: Path, tmp_path: Path) -> None:
    output = tmp_path / "include.html"
    catalog.main(source, output)
    html = output.read_text()
    assert "A, &quot;quoted&quot; &lt;title&gt;" in html
    assert "Two lines\nof text &amp; detail." in html
    assert 'data-date="2025"' in html
    assert html.count('class="resource-row"') == 1
    assert 'data-topic="Tutorials"' in html


@pytest.mark.parametrize(
    "field,value",
    [
        ("year", "not-a-year"),
        ("url", "javascript:alert(1)"),
        ("title", ""),
        ("source_urls", "javascript:alert(1)"),
    ],
)
def test_rejects_invalid_rows(source: Path, field: str, value: str) -> None:
    rows = catalog.read_rows(source)
    rows[0][field] = value
    with pytest.raises(ValueError):
        catalog.validate(rows)


def test_duplicate_ids_rejected(source: Path) -> None:
    rows = catalog.read_rows(source)
    with pytest.raises(ValueError):
        catalog.validate(rows + rows)


def test_canonical_catalog_is_valid() -> None:
    rows = catalog.read_rows(Path(__file__).parents[1] / "data/resources.csv")
    catalog.validate(rows)


def test_search_index_is_complete_and_idempotent(source: Path, tmp_path: Path) -> None:
    search = tmp_path / "search.json"
    search.write_text(json.dumps([{"objectID": "index.html", "text": "Home"}]))
    catalog.index_catalog(source, search)
    catalog.index_catalog(source, search)
    entries = json.loads(search.read_text())
    assert len(entries) == 2
    assert entries[0]["text"] == "Home"
    assert entries[1]["href"] == "resources.html#one"
    assert "Two lines" in entries[1]["text"]


def test_cli_build(
    source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls = []
    monkeypatch.setattr("sys.argv", ["build_catalog.py"])
    monkeypatch.setattr(catalog, "main", lambda: calls.append("build"))
    catalog.cli()
    assert calls == ["build"]
