#!/usr/bin/env python3
"""Resolve the visual-screening findings (from contact-sheet agents) to concrete
image filenames, then emit drop/flag lists.

Findings tokens are messy by nature: full filenames, truncated
'130-company_13812' prefixes, brace shorthand '-0/-1/-4.jpg', or bare tile
positions '格9'. Resolution is scoped to the sheet's own file list, which makes
prefix + index unique in almost every case. Anything ambiguous is reported for
manual handling instead of being guessed.
"""
import os, re, sys, glob, collections

STAGE = os.environ.get("STAGE2_HOME", "/Users/max/.stage2")
PER = 30

def sheet_files():
    """sheet basename -> ordered filenames (row-major, as laid out by montage)."""
    m = {}
    for bf in sorted(glob.glob(os.path.join(STAGE, "batches/batch*.md"))):
        txt = open(bf).read()
        cur = None
        for line in txt.splitlines():
            s = line.strip()
            g = re.match(r"^## (sheets/[\w.]+\.jpg)", s)
            if g:
                cur = os.path.basename(g.group(1)); m[cur] = []; continue
            g = re.match(r"^第(\d+)格\s+(\S+\.jpg)", s)
            if g and cur:
                assert int(g.group(1)) == len(m[cur]) + 1, (cur, g.group(0))
                m[cur].append(g.group(2))
    return m

def expand(tok):
    """'a-0/-1/-4.jpg' -> ['a-0.jpg','a-1.jpg','a-4.jpg'];
       'a-5~-8.jpg'    -> ['a-5.jpg','a-6.jpg','a-7.jpg','a-8.jpg']"""
    ext = ".jpg" if tok.endswith(".jpg") else ""
    core = tok[: -len(ext)] if ext else tok
    m = re.match(r"^(.*?)-(\d+)((?:[~/]\d+)+)$", core)
    if not m:
        return [tok]
    stem, prim, spec = m.group(1), int(m.group(2)), m.group(3)
    rest = [int(x) for x in re.findall(r"[~/](\d+)", spec)]
    if "~" in spec:
        idxs = list(range(prim, rest[-1] + 1))
    else:
        idxs = [prim] + rest
    return [f"{stem}-{i}{ext}" for i in idxs]

def candidates(tok, files, global_files):
    """Filename candidates for a (possibly truncated) token.

    Scoped to the current sheet first; post_id+index is globally unique in our
    naming, so fall back to all sheets when the agent attributed a tile to the
    wrong sheet.
    """
    hits = _match(tok, files)
    if len(hits) == 1:
        return hits
    g = _match(tok, global_files)
    if len(g) == 1:
        return g
    return hits or g

def _match(tok, files):
    res = []
    for t in expand(tok):
        t_clean = t.replace(".jpg", "")
        exact = [f for f in files if f.replace(".jpg", "") == t_clean]
        if exact:
            res += exact; continue
        nums = [n for n in re.findall(r"\d+", t_clean) if len(n) >= 3]
        idx = re.search(r"-(\d+)$", t_clean)
        for f in files:
            fn = f.replace(".jpg", "")
            # every numeric run in the token must appear in the filename
            if not all(n in fn for n in nums):
                continue
            # leading asset id (NNN-) must match when present
            g = re.match(r"^(\d{3})-", t_clean)
            if g and not fn.startswith(g.group(1) + "-"):
                continue
            # trailing tile index (…-N) must match when present
            if idx and not fn.endswith("-" + idx.group(1)):
                continue
            # category token must match when present
            c = re.search(r"(robot|award|company|media|talk|qual|press|project|endorse)", t_clean)
            if c and f"-{c.group(1)}_" not in fn:
                continue
            res.append(f)
    return sorted(set(res))

def main(findings_path):
    sheets = sheet_files()
    glob_files = sorted({f for v in sheets.values() for f in v})
    drops, flags, unresolved = collections.OrderedDict(), collections.OrderedDict(), []
    cur_sheet = None
    for raw in open(findings_path):
        line = raw.strip()
        g = re.match(r"^表\s+([\w.]+\.jpg)", line)
        if g:
            cur_sheet = os.path.basename(g.group(1))
            if cur_sheet not in sheets:
                unresolved.append(("NO_SHEET", line, ""))
            continue
        m = re.match(r"^(DROP|FLAG)\s+(\S+)\s+(\S+)\s*(.*)$", line)
        if not m:
            continue
        kind, tok, code, why = m.groups()
        if cur_sheet not in sheets:
            unresolved.append((kind, line, "sheet 未识别")); continue
        files = sheets[cur_sheet]
        pm = re.match(r"^格(\d+)$", tok)
        hit = ([files[int(pm.group(1)) - 1]] if int(pm.group(1)) <= len(files)
               else []) if pm else candidates(tok, files, glob_files)
        if len(hit) == 1:
            (drops if kind == "DROP" else flags)[hit[0]] = (code, why, cur_sheet)
        else:
            unresolved.append((kind, line, f"命中 {len(hit)} 个: {hit[:3]}"))
    return drops, flags, unresolved, sheets

if __name__ == "__main__":
    drops, flags, unresolved, sheets = main(sys.argv[1])
    total = sum(len(v) for v in sheets.values())
    print(f"sheets mapped: {len(sheets)}  tiles covered: {total}")
    print(f"DROP resolved : {len(drops)}")
    print(f"FLAG resolved : {len(flags)}")
    print(f"UNRESOLVED    : {len(unresolved)}")
    for k, line, why in unresolved:
        print(f"  ? [{k}] {line}  -> {why}")
    with open(os.path.join(STAGE, "drop.txt"), "w") as f:
        for k in drops: f.write(k + "\n")
    with open(os.path.join(STAGE, "flag.txt"), "w") as f:
        for k, (c, w, s) in flags.items(): f.write(f"{k}\t{c}\t{w}\n")
    with open(os.path.join(STAGE, "drop_detail.tsv"), "w") as f:
        for k, (c, w, s) in drops.items(): f.write(f"{k}\t{c}\t{w}\t{s}\n")
    buckets = collections.Counter(
        ("hero" if os.path.exists(os.path.join(STAGE, "out/hero", k)) else
         "proof" if os.path.exists(os.path.join(STAGE, "out/proof", k)) else "missing")
        for k in drops)
    print("drop by bucket:", dict(buckets))
    print("drop by code:", collections.Counter(c for c, _, _ in drops.values()).most_common())
