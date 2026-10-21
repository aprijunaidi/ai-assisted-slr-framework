# Stage 3b · Inclusion and exclusion criteria

**Goal:** decide, before screening starts, exactly which papers count as evidence for the RQs, and write the rules so that two people applying them independently reach the same decision.

## 5.1 How to write good criteria

- **Derive each criterion from the RO, the RQs or a practical limit**, and say which one. A criterion with no reason behind it is hard to defend to reviewers.
- **Make each criterion testable from the paper itself** (title/abstract at stage 1, full text at stage 2). "High quality" is not a screening criterion; that is what quality assessment is for.
- **Keep inclusion and exclusion criteria as mirror images** where possible, so every excluded paper fails a named criterion.
- **Give every exclusion criterion a code** (EC1, EC2, …). The codes become Rayyan reason labels and PRISMA exclusion reasons.
- **Decide the edge cases in advance:** conference papers, preprints, journal extensions of conference papers, review articles, papers on several crops, classification-only papers.
- **Pilot the criteria** on 30–50 records with a second reviewer and refine the wording before full screening.

## 5.2 Criteria for the worked example (rice leaf disease detection, 2021–2025)

| Code | Inclusion criterion | Code | Exclusion criterion | Basis | Stage applied |
|---|---|---|---|---|---|
| IC1 | The study detects, localises or segments **diseases on rice leaves** from images | EC1 | Other crops only; rice pests, weeds, nutrient deficiency or grain quality only; no rice leaf disease | Review scope (RO) | T/A |
| IC2 | The study proposes or evaluates a **deep learning** model (CNN, YOLO family, R-CNN family, transformer, hybrid) | EC2 | Only traditional image processing or classical machine learning (e.g. SVM on hand-crafted features) | Methods of interest (RQ2) | T/A |
| IC3 | The study reports **quantitative results** on a described image dataset (at least one of precision, recall, F1, mAP, accuracy) | EC3 | Concept, position or opinion papers; no experiment or no dataset described | Data needed for RQ1–RQ3 | Full text |
| IC4 | **Peer-reviewed journal article**, published 2021–2025 | EC4 | Conference papers, book chapters, theses, preprints, editorials, letters; published outside 2021–2025 | Practical limit (stated in protocol) | T/A |
| IC5 | Written in **English** | EC5 | Not in English | Practical limit | T/A |
| IC6 | **Full text available** to the reviewers | EC6 | Full text could not be retrieved after library request and contacting the authors | Practical limit | Full text |
| — | — | EC7 | **Duplicate publication** of the same study (same data and model); the most complete version is kept | Avoid double counting | Full text |

T/A = title and abstract screening.

### Decisions on edge cases (worked example)

| Case | Decision | Reason to state in the paper |
|---|---|---|
| Image **classification** papers (one label per image, no localisation) | Include under IC1–IC2 **only if** the RO covers classification; in this example, keep them and tag `task = classification` so RQ2 can compare tasks separately | Classification and detection answer different questions; mixing them without a tag biases comparisons |
| Studies on **several crops including rice** | Include if rice leaf disease results are reported separately | Results for rice must be extractable |
| **Review articles** | Not counted as primary studies; used for snowballing and for positioning the review in the Introduction | Reviews do not report new experiments |
| **Conference papers** | Excluded (EC4) in this example | A team may decide otherwise; in computer vision many strong papers appear at conferences. Whatever the choice, state it and apply it consistently |
| **Early access / in-press** articles | Included if peer-reviewed and dated within the window | Record the online date used |
| Extended journal version of a conference paper | Journal version kept | Most complete report |

## 5.3 Screening decision rule

```text
For each record:
  if any EC applies          → Exclude (record the FIRST applicable EC code)
  elif all IC can be confirmed → Include
  else (information missing)   → Maybe  → decide at full text
```

At full text, every paper must end as *Include* or *Exclude with one EC code*. Use [`templates/eligibility_checklist.csv`](../templates/eligibility_checklist.csv) to record each criterion per paper.

## 5.4 What goes into the paper

- The criteria table (as above, with codes).
- The decisions on edge cases, in one or two sentences.
- The number of records excluded at each stage and, at full text, the number excluded per EC code (PRISMA 2020 flow diagram).
- Who screened, whether screening was blind and independent, and the agreement (Cohen's kappa) where two reviewers took part.

Next: [Stage 3c · Quality assessment](06-quality-assessment.md).
