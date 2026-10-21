# Reference review: how the framework was first used

This framework grew out of the systematic review:

> A. Junaidi, S. Z. Mohd Hashim, M. S. Othman, M. M. Mohamad, H. Alhussian, S. J. Abdulkadir, M. Nasser and Y. A. Bena, "Deep Learning and Edge Computing in Agriculture: A Comprehensive Review of Recent Trends and Innovations," *IEEE Access*, vol. 13, pp. 137464–137490, 2025, doi: [10.1109/ACCESS.2025.3595621](https://doi.org/10.1109/ACCESS.2025.3595621).

Read the paper for the full method. In short:

| Element | In the 2025 review | In this repository |
|---|---|---|
| Topic | Deep learning, edge computing and vision transformers for rice leaf disease detection | Worked example on rice leaf disease detection, with RQs on datasets, architectures and evaluation rigour |
| Research questions | 3 RQs with motivations | 3 RQs with motivations ([docs/02](../docs/02-research-objective-and-questions.md)) |
| Databases | Web of Science, Scopus, ScienceDirect, IEEE Xplore, ACM Digital Library | Same five, plus optional SpringerLink and snowballing |
| Period | 2020–2024 | 2021–2025 (adjust to your review) |
| Records identified → included | 2,072 → 76 (abstract; Section IV reports 75) | Depends on your search |
| Screening tools | Zotero, Rayyan | Zotero, Rayyan, plus `dedup_ris.py` |
| Quality assessment | 5 items, High/Medium/Low = 1/0.5/0, cut-off 3.0 of 5.0 | 9 items on the same scale, cut-off 50% with two mandatory items ([docs/06](../docs/06-quality-assessment.md)) |
| Reporting | PRISMA flow, VOSviewer keyword network | PRISMA 2020 flow from a counts file, bibliometric script, VOSviewer |

The changes are refinements learned from carrying out that review: a compulsory crop block in the search string, the same search fields in every database, and quality items that target the most common weaknesses of deep learning evaluation.
