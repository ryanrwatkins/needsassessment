# Resource catalog data

`resources.csv` is the editable source for the Resources catalog. Each row is
one original Participants Database record. IDs are stable (`reference-<id>`)
and must remain unique.

`year` is a validated four-digit publication year where one was available.
`year_original` retains the source value. `record_status` distinguishes a full
reference record recovered from the archive from a record recovered only from a
bibliography listing. `source_urls` records the archived page or pages that
support the row.

Use semicolons for multiple values in `topics` and `source_urls`. Values are
rendered as text, so editing the CSV never inserts HTML into the site.
