"""Basic bibliometric overview of the included studies from a RIS file.

Outputs (in --out folder):
    publications_per_year.png / .csv
    top_venues.png / .csv
    top_keywords.png / .csv

Usage:
    python scripts/bibliometrics.py included.ris --out results/ --top 15
For the keyword co-occurrence network, load the same RIS file into VOSviewer.
"""
import argparse
import csv
import os
import sys
from collections import Counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ris_utils import all_values, first, read_ris, year  # noqa: E402

BLUE = "#2F6FB5"


def save_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


def barh(path, items, title, xlabel):
    if not items:
        return
    labels, counts = zip(*items[::-1])
    fig, ax = plt.subplots(figsize=(8, 0.4 * len(items) + 1.2))
    ax.barh(range(len(items)), counts, color=BLUE)
    ax.set_yticks(range(len(items)))
    ax.set_yticklabels([lbl[:60] for lbl in labels], fontsize=9)
    ax.set_xlabel(xlabel)
    ax.set_title(title, fontweight="bold")
    for i, cnt in enumerate(counts):
        ax.text(cnt, i, f" {cnt}", va="center", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ris_file")
    ap.add_argument("--out", default="results")
    ap.add_argument("--top", type=int, default=15)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    recs = read_ris(args.ris_file)
    print(f"Records read: {len(recs)}")

    years = Counter(y for y in (year(r) for r in recs) if y)
    yrs = sorted(years)
    save_csv(os.path.join(args.out, "publications_per_year.csv"), ["year", "n"], [(y, years[y]) for y in yrs])
    if yrs:
        span = list(range(yrs[0], yrs[-1] + 1))
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(span, [years.get(y, 0) for y in span], color=BLUE)
        for y in span:
            ax.text(y, years.get(y, 0), str(years.get(y, 0)), ha="center", va="bottom", fontsize=9)
        ax.set_xticks(span)
        ax.set_xlabel("Publication year")
        ax.set_ylabel("Number of studies")
        ax.set_title("Included studies per year", fontweight="bold")
        ax.spines[["top", "right"]].set_visible(False)
        fig.tight_layout()
        fig.savefig(os.path.join(args.out, "publications_per_year.png"), dpi=300)
        plt.close(fig)

    venues = Counter(first(r, "T2", "JO", "JF", "J2").strip() for r in recs)
    venues.pop("", None)
    top_v = venues.most_common(args.top)
    save_csv(os.path.join(args.out, "top_venues.csv"), ["venue", "n"], top_v)
    barh(os.path.join(args.out, "top_venues.png"), top_v, "Top venues", "Number of studies")

    kw = Counter()
    for r in recs:
        terms = set()
        for val in all_values(r, "KW"):
            for t in val.replace(";", ",").split(","):
                t = t.strip().lower()
                if t:
                    terms.add(t)
        kw.update(terms)
    top_k = kw.most_common(args.top)
    save_csv(os.path.join(args.out, "top_keywords.csv"), ["keyword", "n_studies"], top_k)
    barh(os.path.join(args.out, "top_keywords.png"), top_k, "Most frequent keywords", "Number of studies")
    print(f"Outputs written to {args.out}/")


if __name__ == "__main__":
    main()
