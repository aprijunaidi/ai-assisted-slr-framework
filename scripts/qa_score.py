"""Quality-assessment scoring and inter-rater agreement.

Input: templates/quality_assessment.csv with one row per study per reviewer.
Item values: 1, 0.5, 0, or NA (not applicable).

Score = sum of applicable items; quality% = 100 * score / number of applicable items.
A study is included when quality% >= threshold AND every mandatory item >= 0.5.
If a row with reviewer == "consensus" exists for a study it is used for the decision;
otherwise the reviewers' item scores are averaged.

Usage:
    python scripts/qa_score.py templates/quality_assessment.csv --threshold 50 --mandatory QA1 QA6
    python scripts/qa_score.py templates/screening_log.csv --kappa reviewer1_ta reviewer2_ta
"""
import argparse
import csv
from collections import Counter, defaultdict


def parse(v):
    v = (v or "").strip().upper()
    if v in ("", "NA", "N/A"):
        return None
    x = float(v)
    if x not in (0.0, 0.5, 1.0):
        raise ValueError(f"QA score must be 1, 0.5, 0 or NA, got {v!r}")
    return x


def cohen_kappa(a, b):
    pairs = [(x, y) for x, y in zip(a, b) if x != "" and y != ""]
    n = len(pairs)
    if n == 0:
        return None, 0
    po = sum(x == y for x, y in pairs) / n
    ca, cb = Counter(x for x, _ in pairs), Counter(y for _, y in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return (1.0 if pe == 1 else (po - pe) / (1 - pe)), n


def kappa_mode(path, c1, c2):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    a = [r[c1].strip().lower() for r in rows]
    b = [r[c2].strip().lower() for r in rows]
    k, n = cohen_kappa(a, b)
    if k is None:
        print("No rows with decisions from both reviewers.")
    else:
        agree = sum(x == y for x, y in zip(a, b) if x and y)
        print(f"Pairs compared: {n}; raw agreement: {agree / n:.1%}; Cohen's kappa: {k:.3f}")


def qa_mode(path, threshold, mandatory, out):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    items = [c for c in rows[0].keys() if c.upper().startswith("QA")] if rows else []
    by_study = defaultdict(dict)
    for r in rows:
        by_study[r["study_id"]][r["reviewer"].strip().lower()] = {i: parse(r[i]) for i in items}

    results, item_kappa_data = [], defaultdict(lambda: ([], []))
    for sid, revs in by_study.items():
        named = [k for k in revs if k != "consensus"]
        if len(named) >= 2:
            r1, r2 = revs[named[0]], revs[named[1]]
            for i in items:
                item_kappa_data[i][0].append("" if r1[i] is None else str(r1[i]))
                item_kappa_data[i][1].append("" if r2[i] is None else str(r2[i]))
        if "consensus" in revs:
            scores, basis = revs["consensus"], "consensus"
        else:
            scores, basis = {}, "mean of " + ", ".join(named)
            for i in items:
                vals = [revs[k][i] for k in named if revs[k][i] is not None]
                scores[i] = sum(vals) / len(vals) if vals else None
        applicable = [v for v in scores.values() if v is not None]
        total = sum(applicable)
        pct = 100 * total / len(applicable) if applicable else 0.0
        failed = [m for m in mandatory if scores.get(m) is None or scores[m] < 0.5]
        decision = "include" if pct >= threshold and not failed else "exclude"
        reasons = []
        if pct < threshold:
            reasons.append(f"below {threshold:g}%")
        if failed:
            reasons.append("mandatory item(s) " + ",".join(failed) + " < 0.5")
        reason = "; ".join(reasons)
        band = "high" if pct >= 75 else ("moderate" if pct >= threshold else "low")
        results.append({"study_id": sid, "basis": basis, "score": round(total, 2),
                        "applicable_items": len(applicable), "quality_percent": round(pct, 1),
                        "band": band, "decision": decision, "reason": reason})

    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(results[0].keys()) if results else ["study_id"])
        w.writeheader()
        w.writerows(results)

    inc = sum(r["decision"] == "include" for r in results)
    print(f"Studies scored: {len(results)}; included: {inc}; excluded: {len(results) - inc}  -> {out}")
    if item_kappa_data:
        print("Agreement per item (first two reviewers):")
        for i in items:
            k, n = cohen_kappa(*item_kappa_data[i])
            print(f"  {i}: kappa = {'n/a' if k is None else f'{k:.3f}'} (n = {n})")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv_file")
    ap.add_argument("--threshold", type=float, default=50.0, help="minimum quality percent (default 50)")
    ap.add_argument("--mandatory", nargs="*", default=["QA1", "QA6"], help="items that must score >= 0.5")
    ap.add_argument("--out", default="qa_results.csv")
    ap.add_argument("--kappa", nargs=2, metavar=("COL1", "COL2"),
                    help="compute Cohen's kappa between two decision columns instead of QA scoring")
    args = ap.parse_args()
    if args.kappa:
        kappa_mode(args.csv_file, *args.kappa)
    else:
        qa_mode(args.csv_file, args.threshold, args.mandatory, args.out)


if __name__ == "__main__":
    main()
