"""Minimal RIS reader/writer used by the scripts in this folder (standard library only)."""
import re

TAG_RE = re.compile(r"^([A-Z][A-Z0-9])  - ?(.*)$")


def read_ris(path):
    """Return a list of records; each record is a list of (tag, value) pairs in file order."""
    records, current = [], []
    with open(path, encoding="utf-8-sig", errors="replace") as fh:
        for raw in fh:
            line = raw.rstrip("\r\n")
            m = TAG_RE.match(line)
            if not m:
                if current and line.strip():  # continuation line
                    tag, val = current[-1]
                    current[-1] = (tag, f"{val} {line.strip()}")
                continue
            tag, val = m.group(1), m.group(2).strip()
            if tag == "ER":
                if current:
                    records.append(current)
                current = []
            else:
                current.append((tag, val))
    if current:
        records.append(current)
    return records


def write_ris(records, path):
    with open(path, "w", encoding="utf-8") as fh:
        for rec in records:
            for tag, val in rec:
                fh.write(f"{tag}  - {val}\n")
            fh.write("ER  - \n\n")


def first(rec, *tags):
    for t in tags:
        for tag, val in rec:
            if tag == t and val:
                return val
    return ""


def all_values(rec, *tags):
    return [val for tag, val in rec if tag in tags and val]


def title(rec):
    return first(rec, "TI", "T1", "CT")


def year(rec):
    m = re.search(r"(19|20)\d{2}", first(rec, "PY", "Y1", "DA"))
    return int(m.group(0)) if m else None


def doi(rec):
    d = first(rec, "DO")
    if not d:
        for val in all_values(rec, "UR", "L3", "M3"):
            if "10." in val:
                d = val
                break
    m = re.search(r"10\.\d{4,9}/\S+", d)
    return m.group(0).rstrip(".,;").lower() if m else ""


def norm_title(t):
    t = t.lower()
    t = re.sub(r"<[^>]+>", " ", t)          # html tags from some exports
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()
