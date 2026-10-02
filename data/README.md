# Resource catalog data

`resources.csv` is the editable source for the Resources catalog. It combines
the cleaned bibliography export with records retained from the earlier catalog.
IDs are stable (`reference-<id>` or `reference-clean-<id>`) and must remain
unique. `resources_archived.csv` preserves the prior catalog for reference.

`year` is a validated four-digit publication year where one was available.
`year_original` retains the source value. `record_status` distinguishes a full
reference record from a record recovered only from a bibliography listing.
`source_urls` records any available non-archival source pages that support the
row.

Use semicolons for multiple values in `topics` and `source_urls`. The public
catalog renders reference information as text and does not expose catalog URLs.
Editing the CSV never inserts HTML into the site.
