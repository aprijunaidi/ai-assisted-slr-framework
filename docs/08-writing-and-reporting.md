# Stage 5 · Writing, language refinement and reporting

**Goal:** a manuscript that reports the review transparently enough for someone else to repeat it, written in clear academic English, with honest disclosure of how AI tools were used.

## 8.1 Suggested structure of an SLR article

1. **Introduction** – why the problem matters (yield loss, field conditions), what existing reviews cover, what this review adds, the RO and RQs.
2. **Review methodology** – protocol (and registration, e.g. on OSF), databases, full search strings (table), eligibility criteria (table), screening procedure, quality assessment (table and threshold), data extraction, synthesis method.
3. **Overview of included studies** – PRISMA 2020 flow diagram, publications per year, venues, keyword network.
4. **Results by RQ** – one section per RQ, organised by theme, with comparison tables.
5. **Discussion** – cross-cutting findings, disagreements and their likely causes, open challenges and a research agenda.
6. **Threats to validity** – database coverage, language and date limits, single or double screening, subjectivity of QA, publication bias.
7. **Conclusions** – one answer per RQ.

Check the draft against the **PRISMA 2020 checklist** (Page et al., 2021) and submit the completed checklist as a supplementary file.

## 8.2 Citations

Citations come from Zotero only (Zotero Connector + the Word/LibreOffice plugin, or Better BibTeX for LaTeX). Every reference in the paper must exist in the Zotero library with a verified DOI. Never paste a reference suggested by a chatbot without finding the paper itself.

## 8.3 Language refinement

| Tool | Use | Note |
|---|---|---|
| [InstaText](https://instatext.io) | Improving clarity, grammar and flow of text you wrote | Read every suggestion; reject changes that alter technical meaning |
| [StealthWriter](https://stealthwriter.ai) | Rewording sentences of your own draft | Use only to rephrase your own writing. Do not use it to hide AI involvement: journals and universities require AI use to be disclosed, and text altered to evade detection can be treated as misconduct |

Two checks before submission:

- **Similarity with your own earlier work.** Text reused from your thesis or a previous review (even your own) is flagged by similarity checks and can lead to desk rejection. Rewrite from the underlying facts rather than swapping synonyms, and cite the earlier paper.
- **Technical accuracy after rewriting.** Paraphrasing tools sometimes change numbers, metric names or the strength of a claim. Re-check every number against the extraction table.

The output of this stage is the **final draft article**: the language-refined manuscript, checked against the extraction table, that the authors read once more in full before submission.

## 8.4 Disclosure of AI use

Most publishers now require a statement on generative AI use (Elsevier: a separate declaration; Springer Nature: description in the Methods when use goes beyond copy editing; IEEE: disclosure in the acknowledgements). Keep the prompt log from [Stage 1](01-ideation-and-prompting.md) so you can describe:

- which tools were used (name and version or access date);
- for which tasks (e.g. brainstorming search terms, structuring research questions, language editing);
- that all outputs were checked by the authors and that the authors take responsibility for the content.

AI tools cannot be listed as authors.

## 8.5 Reproducibility package

Publish, as supplementary material or in a repository like this one:

- the protocol (RO, RQs, criteria, QA checklist), ideally registered before screening;
- the search log with full strings, dates and hit counts;
- the screening log with exclusion reasons;
- the quality-assessment scores;
- the data-extraction table;
- the scripts used for figures.
