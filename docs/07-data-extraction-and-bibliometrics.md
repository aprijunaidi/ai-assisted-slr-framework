# Stage 4 · Data extraction, bibliometric analysis and synthesis

**Goal:** turn the included papers into a structured table that answers each RQ, then describe the literature (bibliometrics) and synthesise the findings across studies.

## 7.1 Data extraction form

Use [`templates/data_extraction.csv`](../templates/data_extraction.csv), one row per included study. Every column maps to an RQ:

| Column | RQ | What to record |
|---|---|---|
| `study_id`, `citation_key`, `year`, `venue`, `doi` | — | Identification |
| `country` | RQ1 | Country where images were collected |
| `diseases`, `n_classes` | RQ1 | Disease names as given in the paper |
| `dataset_name`, `n_images`, `public` | RQ1 | Dataset; `yes / no / on request` |
| `imaging` | RQ1 | `lab / controlled / field / mixed`; device |
| `task` | RQ2 | `detection / segmentation / classification` |
| `model_family`, `baseline_models` | RQ2 | e.g. YOLOv8; Faster R-CNN |
| `enhancement` | RQ2 | attention type, multi-scale fusion, lightweight backbone, transformer |
| `params_M`, `gflops`, `input_size` | RQ2 | As reported |
| `metric_name`, `metric_value` | RQ2 | **Exactly** as reported (do not convert mAP@0.5 to mAP@0.5:0.95 or accuracy to F1) |
| `n_runs`, `variability_reported` | RQ3 | e.g. `1`; `SD over 3 seeds` |
| `split_described`, `cross_dataset` | RQ3 | `yes / partly / no` |
| `hardware`, `latency_ms`, `fps` | RQ3 | Device on which speed was measured |
| `edge_deployed` | RQ3 | `yes / no` |
| `code_available` | RQ3 | `yes / no` |
| `qa_percent` | — | From Stage 3c |
| `limitations` | — | As stated by the authors |
| `locator` | — | Table or page numbers for the values above |

Rules: copy values exactly, with the table or page they come from; write `not reported` instead of guessing; pilot the form on five papers and adjust columns before extracting the rest.

## 7.2 Bibliometric analysis

Export the final included set from Zotero as RIS. Then:

| Tool | What it shows |
|---|---|
| [VOSviewer](https://www.vosviewer.com) | Keyword co-occurrence network (Create map → based on bibliographic data → read RIS file, or the Scopus/WoS export directly) |
| [`scripts/bibliometrics.py`](../scripts/bibliometrics.py) | Publications per year, top venues and top author keywords from the RIS file, saved as PNG and CSV |
| [Napkin](https://www.napkin.ai) | Turning a written summary into a conceptual illustration (taxonomy, framework) |

```bash
python scripts/bibliometrics.py included.ris --out results/
```

Bibliometric figures describe the literature; they do not answer the RQs on their own. Keep them short in the paper and spend the space on the synthesis.

## 7.3 Synthesis

- Group studies by theme for each RQ (e.g. for RQ2: attention-based, multi-scale, transformer, lightweight), not paper by paper.
- For each theme, report where studies **agree**, where they **disagree** (and whether dataset, input size, metric or imaging conditions explain the difference) and where evidence is **thin** (fewer than two studies).
- Compare numbers only when the metric, dataset and input size match, and say so when they do not.
- Weight conclusions by quality score (Stage 3c).
- End with a gap list phrased as answerable questions for future work.

## 7.4 PRISMA 2020 flow diagram

Fill in [`templates/prisma_counts.csv`](../templates/prisma_counts.csv) from the search log, Zotero, Rayyan and the screening log, then draw the diagram:

```bash
python scripts/prisma_flow.py templates/prisma_counts.csv --out figures/prisma_flow.png
```

The script checks that the counts add up before drawing.
