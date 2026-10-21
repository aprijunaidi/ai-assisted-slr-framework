"""Draw a PRISMA 2020-style flow diagram from templates/prisma_counts.csv.

The script first checks that the counts are consistent, then draws the diagram.
Records found by citation searching (snowballing) are added at the full-text stage.

Usage:
    python scripts/prisma_flow.py templates/prisma_counts.csv --out figures/prisma_flow.png
"""
import argparse
import csv
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402


def load(path):
    vals, labels = {}, {}
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            v = r["value"].strip()
            if v == "":
                sys.exit(f"Missing value for '{r['key']}' in {path}. Fill in every count before drawing.")
            vals[r["key"]] = int(v)
            labels[r["key"]] = r["label"]
    return vals, labels


def compute(v):
    dbs = {k: n for k, n in v.items() if k.startswith("db_")}
    c = {"identified": sum(dbs.values())}
    c["screened"] = c["identified"] - v["duplicates_removed"] - v.get("excluded_automation", 0)
    c["sought"] = c["screened"] - v["records_excluded_ta"]
    c["assessed_db"] = c["sought"] - v["reports_not_retrieved"]
    ec = {k: n for k, n in v.items() if k.startswith("excluded_EC")}
    c["excluded_ft"] = sum(ec.values())
    c["assessed"] = c["assessed_db"] + v.get("other_sources", 0)
    c["eligible"] = c["assessed"] - c["excluded_ft"]
    c["included_calc"] = c["eligible"] - v.get("excluded_QA", 0)
    for k in ("screened", "sought", "assessed_db", "eligible", "included_calc"):
        if c[k] < 0:
            sys.exit(f"Inconsistent counts: '{k}' becomes negative ({c[k]}).")
    if c["included_calc"] != v["included"]:
        sys.exit(f"Counts do not add up: the flow gives {c['included_calc']} included studies, "
                 f"but 'included' = {v['included']}. Check the screening log.")
    return dbs, ec, c


def box(ax, x, y, w, h, text, fc="#FFFFFF", ec="#37474F", bold=False, size=9.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc, ec=ec, lw=1.4))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size,
            fontweight="bold" if bold else "normal", wrap=True)


def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color="#37474F", lw=1.4))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("counts_csv")
    ap.add_argument("--out", default="prisma_flow.png")
    args = ap.parse_args()
    v, labels = load(args.counts_csv)
    dbs, ec, c = compute(v)

    fig, ax = plt.subplots(figsize=(11, 12))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 12.5)
    ax.axis("off")
    stages = [("Identification", 9.4, 2.9, "#DCE9F7"), ("Screening", 3.0, 6.3, "#FFF1D6"),
              ("Included", 0.3, 2.6, "#DFF2E1")]
    for name, y0, h, col in stages:
        ax.add_patch(FancyBboxPatch((0.1, y0), 0.6, h, boxstyle="round,pad=0.02,rounding_size=0.1",
                                    fc=col, ec="none"))
        ax.text(0.4, y0 + h / 2, name, rotation=90, ha="center", va="center", fontsize=11, fontweight="bold")

    db_lines = "\n".join(f"{labels[k]} (n = {n})" for k, n in dbs.items())
    box(ax, 1.0, 9.6, 4.6, 2.5, f"Records identified from databases (n = {c['identified']})\n\n{db_lines}", "#EEF5FC")
    box(ax, 6.3, 10.2, 4.4, 1.4,
        f"Records removed before screening:\nDuplicates (n = {v['duplicates_removed']})\n"
        f"Removed by automation tools (n = {v.get('excluded_automation', 0)})", "#F7F7F7")
    arrow(ax, 5.6, 10.9, 6.3, 10.9)

    box(ax, 1.0, 7.9, 4.6, 0.9, f"Records screened (title/abstract)\n(n = {c['screened']})")
    box(ax, 6.3, 7.9, 4.4, 0.9, f"Records excluded (n = {v['records_excluded_ta']})", "#FDECEC", "#C62828")
    arrow(ax, 3.3, 9.6, 3.3, 8.8)
    arrow(ax, 5.6, 8.35, 6.3, 8.35)

    box(ax, 1.0, 6.5, 4.6, 0.9, f"Reports sought for retrieval\n(n = {c['sought']})")
    box(ax, 6.3, 6.5, 4.4, 0.9, f"Reports not retrieved (n = {v['reports_not_retrieved']})", "#FDECEC", "#C62828")
    arrow(ax, 3.3, 7.9, 3.3, 7.4)
    arrow(ax, 5.6, 6.95, 6.3, 6.95)

    other = v.get("other_sources", 0)
    box(ax, 1.0, 4.9, 4.6, 1.1,
        f"Reports assessed for eligibility\n(n = {c['assessed']}"
        + (f"; incl. {other} from citation searching)" if other else ")"))
    ec_lines = "\n".join(f"{labels[k]} (n = {n})" for k, n in ec.items())
    box(ax, 6.3, 4.2, 4.4, 2.0, f"Reports excluded (n = {c['excluded_ft']}):\n{ec_lines}", "#FDECEC", "#C62828", size=9)
    arrow(ax, 3.3, 6.5, 3.3, 6.0)
    arrow(ax, 5.6, 5.45, 6.3, 5.45)

    box(ax, 1.0, 3.2, 4.6, 0.9, f"Reports assessed for quality\n(n = {c['eligible']})")
    box(ax, 6.3, 3.2, 4.4, 0.9, f"Below quality threshold (n = {v.get('excluded_QA', 0)})", "#FDECEC", "#C62828")
    arrow(ax, 3.3, 4.9, 3.3, 4.1)
    arrow(ax, 5.6, 3.65, 6.3, 3.65)

    box(ax, 1.0, 1.0, 4.6, 1.1, f"Studies included in review\n(n = {v['included']})", "#DFF2E1", "#2E7D32", bold=True, size=11)
    arrow(ax, 3.3, 3.2, 3.3, 2.1)

    fig.savefig(args.out, dpi=300, bbox_inches="tight")
    if args.out.lower().endswith(".png"):
        fig.savefig(args.out[:-4] + ".pdf", bbox_inches="tight")
    print(f"Counts are consistent. Diagram saved to {args.out}")


if __name__ == "__main__":
    main()
