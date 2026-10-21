# Stage 2 · Search strategy and search strings

**Goal of this stage:** run the same conceptual search in every database, adapted to each database's syntax, and record exactly what was run so anyone can repeat it.

## 3.1 Principles

1. **Build the string from concept blocks, not from a sentence.** Blocks come from the key concepts of the RQs in [Stage 1](02-research-objective-and-questions.md): `A (crop) AND B (disease) AND C (method)`. Terms *within* a block are joined with `OR`; blocks are joined with `AND`.
2. **The crop term must be compulsory.** If `rice` is only one option inside an `OR` group (for example `"object detection" OR "rice leaf disease detection"`), the database returns every object-detection paper, and screening load explodes. Putting the crop in its own `AND` block keeps results on topic.
3. **Search the same fields everywhere.** Use title, abstract and keywords in every database (WoS `TS=`, Scopus `TITLE-ABS-KEY`, IEEE metadata/abstract, ScienceDirect "Title, abstract or author-specified keywords"). Mixing "All fields" in one database with "title-abstract-keywords" in another makes the hit counts incomparable.
4. **Filters go after the string and are written down.** Year range, document type, language and source type are applied the same way in every database and recorded in the search log.
5. **Pilot before you freeze.** Check that the string finds 5–10 "known" relevant papers (from Stage 1). If one is missing, find out why and adjust the string. Record the final version and the date.
6. **Deployment terms are not a filter.** Block D (edge, embedded, mobile, real-time) is used to *tag* papers for RQ3 after screening, not to restrict the search.

Worked example settings: **2021–2025**, **English**, **journal articles and review articles**, search run on **[date]**.

## 3.2 Search strings per database

### Web of Science Core Collection (Advanced Search)

```text
TS=((rice OR paddy OR "Oryza sativa")
 AND ("leaf disease*" OR "plant disease*" OR "leaf blight" OR "bacterial blight" OR blast
      OR "brown spot" OR "leaf smut" OR tungro OR "sheath blight" OR lesion*)
 AND ("deep learning" OR "convolutional neural network*" OR CNN OR YOLO* OR "object detection"
      OR detector* OR "Faster R-CNN" OR "vision transformer*" OR transformer*
      OR "attention mechanism*" OR segmentation))
AND PY=(2021-2025) AND DT=(Article OR Review) AND LA=(English)
```

`TS=` searches title, abstract, author keywords and Keywords Plus.

### Scopus (Advanced document search)

```text
TITLE-ABS-KEY((rice OR paddy OR "Oryza sativa")
 AND ("leaf disease*" OR "plant disease*" OR "leaf blight" OR "bacterial blight" OR blast
      OR "brown spot" OR "leaf smut" OR tungro OR "sheath blight" OR lesion*)
 AND ("deep learning" OR "convolutional neural network*" OR cnn OR yolo* OR "object detection"
      OR detector* OR "Faster R-CNN" OR "vision transformer*" OR transformer*
      OR "attention mechanism*" OR segmentation))
AND PUBYEAR > 2020 AND PUBYEAR < 2026
AND (LIMIT-TO(DOCTYPE, "ar") OR LIMIT-TO(DOCTYPE, "re"))
AND (LIMIT-TO(LANGUAGE, "English"))
AND (LIMIT-TO(SRCTYPE, "j"))
```

### IEEE Xplore (Advanced Search → Command Search, field: All Metadata)

```text
(rice OR paddy)
AND ("leaf disease" OR "leaf diseases" OR "plant disease" OR "plant diseases" OR blight
     OR blast OR "brown spot" OR "leaf smut" OR tungro OR lesion OR lesions)
AND ("deep learning" OR "convolutional neural network" OR CNN OR YOLO OR "object detection"
     OR "Faster R-CNN" OR "vision transformer" OR transformer OR attention OR segmentation)
```

Filters: *Journals* and *Early Access Articles* (if early access is accepted in your criteria), years 2021–2025. IEEE Xplore limits the number of search terms and wildcards in one query, so plural forms are written out instead of truncated. If the query is rejected, split block C into two queries and merge the exports.

### ScienceDirect (Advanced search, field: Title, abstract or author-specified keywords)

ScienceDirect accepts **at most 8 Boolean connectors per field** and does not support wildcards, so the full string must be split into complementary queries. Run all three, export each, and let Zotero remove the overlap.

```text
Q1: (rice OR paddy) AND ("leaf disease" OR blight OR blast OR "brown spot") AND ("deep learning" OR YOLO OR "object detection")
Q2: (rice OR paddy) AND ("leaf smut" OR tungro OR "sheath blight" OR lesion) AND ("deep learning" OR transformer OR attention)
Q3: (rice OR paddy) AND ("plant disease" OR "leaf disease") AND (CNN OR "convolutional neural network" OR segmentation)
```

Filters: Article type = *Research articles*, *Review articles*; Years = 2021–2025.

### ACM Digital Library (Advanced Search, Search within: Abstract)

```text
(rice OR paddy) AND (disease OR blight OR blast OR lesion)
AND ("deep learning" OR CNN OR YOLO OR "object detection" OR transformer OR attention OR segmentation)
```

Filters: Content type = *Research Article*, *Survey*; Publication date 01/01/2021 – 12/31/2025. ACM indexes mostly computing venues, so expect few hits; it is included for coverage of computing journals.

### Optional sources

| Source | Role | Note |
|---|---|---|
| SpringerLink | Extra coverage of Springer journals | Use the same three blocks; record filters |
| Google Scholar | **Snowballing only**, not a primary database | Results are ranked and change over time, so they cannot be reproduced exactly |
| Reference lists of included papers | Backward snowballing | Record every paper added this way, with the paper it came from |
| Papers citing included papers (scite, Google Scholar "Cited by") | Forward snowballing | As above |

## 3.3 Record every search

Fill in [`templates/search_log.csv`](../templates/search_log.csv) on the day you search:

| Field | Example |
|---|---|
| database | Scopus |
| date_searched | 2026-11-03 |
| interface | Advanced document search |
| fields_searched | TITLE-ABS-KEY |
| search_string | (exact string as run) |
| filters | 2021–2025; ar, re; English; journals |
| hits | (number shown by the database) |
| export_file | `exports/scopus_2026-11-03.ris` |
| notes | Exported in two batches |

Report these numbers in the PRISMA flow diagram (*records identified from each database*) and give the full strings in a table or supplementary file, so the search can be repeated.

## 3.4 Export

Export each result set as **RIS** (with abstracts and keywords). Some databases cap the number of records per export, so export large sets in batches and note this in the log. Keep the raw exports unchanged in an `exports/` folder; all cleaning happens in Zotero ([Stage 3](04-reference-management-and-screening.md)).
