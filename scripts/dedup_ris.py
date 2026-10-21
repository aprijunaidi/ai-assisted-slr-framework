"""Merge RIS exports from several databases and remove duplicates.

Duplicates are matched by DOI first, then by normalised title + year.
The first occurrence is kept (so list the database you trust most first).

Usage:
    python scripts/dedup_ris.py exports/wos.ris exports/scopus.ris exports/ieee.ris \
        --out merged_dedup.ris --log dedup_log.csv
"""
import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ris_utils import doi, norm_title, read_ris, title, write_ris, year  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ris_files", nargs="+")
    ap.add_argument("--out", default="merged_dedup.ris")
    ap.add_argument("--log", default="dedup_log.csv")
    args = ap.parse_args()

    kept, seen_doi, seen_title, log_rows = [], {}, {}, []
    per_source = {}
    for path in args.ris_files:
        recs = read_ris(path)
        per_source[os.path.basename(path)] = len(recs)
        for i, rec in enumerate(recs):
            d, t, y = doi(rec), norm_title(title(rec)), year(rec)
            key_t = f"{t}|{y}" if t else ""
            match = None
            if d and d in seen_doi:
                match, how = seen_doi[d], "doi"
            elif key_t and key_t in seen_title:
                match, how = seen_title[key_t], "title+year"
            if match:
                log_rows.append({"source": os.path.basename(path), "record": i + 1,
                                 "title": title(rec)[:200], "doi": d,
                                 "matched_on": how, "duplicate_of": match})
                continue
            ident = f"{os.path.basename(path)}#{i + 1}"
            kept.append(rec)
            if d:
                seen_doi[d] = ident
            if key_t:
                seen_title[key_t] = ident

    write_ris(kept, args.out)
    with open(args.log, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["source", "record", "title", "doi", "matched_on", "duplicate_of"])
        w.writeheader()
        w.writerows(log_rows)

    total = sum(per_source.values())
    for src, n in per_source.items():
        print(f"{src:40s} {n:6d} records")
    print(f"{'Total identified':40s} {total:6d}")
    print(f"{'Duplicates removed':40s} {len(log_rows):6d}")
    print(f"{'Unique records written':40s} {len(kept):6d}  -> {args.out}")


if __name__ == "__main__":
    main()
