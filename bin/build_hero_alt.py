#!/usr/bin/env python3
"""Normalise the agents' HERO_ALT lines into hero_alt.tsv (basename -> alt).

Agents wrote the alt either as a bare asset number ("HERO_ALT 180 | ...") or as
a full filename ("HERO_ALT 273-2025-robot_14647846008705061455-0.jpg | ...").
Each asset contributes at most one hero image, so the 3-digit asset prefix is a
safe join key against plan.tsv; anything that does not resolve to exactly one
hero row is reported instead of guessed.
"""
import csv, os, re, collections

STAGE = os.environ.get("STAGE2_HOME", "/Users/max/.stage2")

def main():
    rows = list(csv.DictReader(open(os.path.join(STAGE, "plan.tsv")), delimiter="\t"))
    by_asset = collections.defaultdict(list)
    by_name = {}
    for r in rows:
        name = os.path.basename(r["dest"])
        by_name[name] = r
        if r["bucket"] == "hero":
            by_asset[int(r["asset"])].append(name)

    out, bad = {}, []
    for src in ("hero_alt.txt", "hero_alt_batch03_05.txt"):
        p = os.path.join(STAGE, src)
        if not os.path.exists(p):
            continue
        for line in open(p):
            m = re.match(r"^HERO_ALT\s+(\S+)\s*\|\s*(.+)$", line.strip())
            if not m:
                continue
            tok, alt = m.groups()
            g = re.match(r"^(\d{3})(?:-|$)", tok)
            if not g:
                bad.append((src, tok, 0))
                continue
            key = g.group(1)
            # one hero image per asset, so the asset prefix is the join key;
            # the agent's trailing tile index is ignored on purpose.
            hits = by_asset.get(int(key), [])
            if len(hits) != 1:
                bad.append((src, tok, len(hits)))
                continue
            out[hits[0]] = alt
    with open(os.path.join(STAGE, "hero_alt.tsv"), "w") as f:
        for k in sorted(out):
            f.write(f"{k}\t{out[k]}\n")
    print(f"hero_alt.tsv: {len(out)} entries")
    for src, tok, n in bad:
        print(f"  ? {src}: {tok} -> {n} hero rows")

if __name__ == "__main__":
    main()
