# Stage 3a · Reference management and screening (Zotero ⇄ Rayyan)

**Goal of this stage:** one clean, de-duplicated library, screened in two passes against the eligibility criteria, with every decision recorded.

## 4.1 Flow

```text
Database exports (.ris)
      │
      ▼
Zotero ── merge collections ── remove duplicates ──► export one .ris
      │                                                   │
      │                                                   ▼
      │                                  Rayyan: title/abstract screening
      │                                  (blind, ideally 2 reviewers)
      │                                                   │
      ◄────────────── export "included" as .ris ◄─────────┘
      │
      ▼
Full-text retrieval → full-text eligibility → quality assessment
```

## 4.2 Zotero

1. Create one collection per database (`WoS`, `Scopus`, `IEEE`, `ScienceDirect`, `ACM`) and import each RIS file into its collection. The collection sizes must equal the `hits` in the search log; if not, an export batch is missing.
2. Copy all items into a collection named `00_all_records` and run **Duplicate Items → Merge**. Zotero matches on DOI, ISBN and title. Check each merge; records of the same paper from different databases sometimes have slightly different titles.
3. Optional, reproducible alternative: run [`scripts/dedup_ris.py`](../scripts/dedup_ris.py) on the raw exports. It removes duplicates by DOI and by normalised title and writes a log of what was removed.
4. Record the number of duplicates removed (PRISMA: *duplicate records removed*).
5. Export `00_all_records` as one RIS file for Rayyan.

## 4.3 Rayyan: title and abstract screening

1. Create a review, upload the RIS file, and invite a second reviewer (supervisor or colleague).
2. Turn on **blind mode** so reviewers cannot see each other's decisions.
3. Before screening everything, **calibrate**: both reviewers screen the same 30–50 records, compare decisions, discuss disagreements and refine the wording of the criteria. Repeat if agreement is low.
4. Screen all records against the criteria in [Stage 3b](05-inclusion-exclusion-criteria.md). Use *Include*, *Exclude* (with a reason label) or *Maybe*. When in doubt, mark *Maybe*: excluding at full text is cheap, missing a relevant paper is not.
5. Turn off blind mode, resolve conflicts by discussion (or a third reviewer), and record agreement with Cohen's kappa ([`scripts/qa_score.py --kappa`](../scripts/qa_score.py) computes it from the two reviewers' decisions).
6. Export the included and *Maybe* records as RIS and import them back into a Zotero collection `01_title_abstract_included`.

Rayyan's reason labels map directly to the exclusion codes (EC1–EC7) in [Stage 3b](05-inclusion-exclusion-criteria.md), so the PRISMA counts per reason can be read straight from Rayyan.

## 4.4 Full-text screening

1. Retrieve full texts (Zotero *Find Available PDF*, library access, or request from authors). Count the reports you could not retrieve (PRISMA: *reports not retrieved*).
2. Assess every full text against the criteria again, now using the methods and results sections. Record the decision and **one** main exclusion reason per paper in [`templates/screening_log.csv`](../templates/screening_log.csv).
3. Papers that pass go to quality assessment ([Stage 3c](06-quality-assessment.md)).

## 4.5 If you screen alone

Postgraduate students often screen alone. That is acceptable if it is reported honestly. Two practical safeguards:

- ask a second person to screen a random 10–20% sample and report the agreement on that sample;
- re-screen your own first 50 decisions at the end of screening, when the criteria are better understood.

State in the paper which of these was done.
