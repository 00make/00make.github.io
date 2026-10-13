#!/usr/bin/env python3
"""Apply the visual-screening verdicts and ingest the surviving images into the
site, writing the proof manifest alongside.

Rules:
  - DROP files are never copied.
  - A hero image carrying any FLAG is demoted to proof: cards are the loudest
    placement on the site, so a blurry / unreadable / face-heavy shot does not
    belong there even though it may still sit in a gallery.
"""
import csv, os, shutil, collections

STAGE = os.environ.get("STAGE2_HOME", "/Users/max/.stage2")
REPO = "/Users/max/Documents/GitHub/00make.github.io"
HERO_DIR = os.path.join(REPO, "assets/img/journal")
PROOF_DIR = os.path.join(REPO, "assets/proof")

def load(path, col=None):
    if not os.path.exists(path):
        return []
    out = []
    for line in open(path):
        parts = line.rstrip("\n").split("\t")
        out.append(parts if col is None else (parts[col] if len(parts) > col else ""))
    return out

def main():
    rows = list(csv.DictReader(open(os.path.join(STAGE, "plan.tsv")), delimiter="\t"))
    drops = {l for l in load(os.path.join(STAGE, "drop.txt"), col=0) if l}
    for extra in ("005-2019-company_13419257287239864373-0.jpg",
                  "019-2019-award_13180450257479012437-0.jpg"):
        drops.add(extra)          # the two tokens the resolver left ambiguous
    flags = {p[0]: (p[1], p[2]) for p in load(os.path.join(STAGE, "flag.txt")) if p and p[0]}
    hero_alt = {}
    if os.path.exists(os.path.join(STAGE, "hero_alt.tsv")):
        for p in load(os.path.join(STAGE, "hero_alt.tsv")):
            if len(p) >= 2 and p[0]:
                hero_alt[p[0]] = p[1]

    kept, stats = [], collections.Counter()
    for r in rows:
        name = os.path.basename(r["dest"])
        if name in drops:
            stats["drop"] += 1
            continue
        bucket = r["bucket"]
        if bucket == "hero" and name in flags:
            bucket = "proof"
            stats["demoted"] += 1
        src = os.path.join(STAGE, "out", r["bucket"], name)
        if not os.path.isfile(src):
            stats["missing_src"] += 1
            continue
        dest_dir = HERO_DIR if bucket == "hero" else PROOF_DIR
        alt = hero_alt.get(name) or r["alt"]
        kept.append({
            "src": src, "asset": r["asset"],
            "new_path": os.path.relpath(os.path.join(dest_dir, name), REPO),
            "bucket": bucket, "post_id": r["post"], "file_index": r["idx"],
            "asset_type": r["atype"], "resume_value": r["title"],
            "alt": alt, "alt_source": "visual" if name in hero_alt else r["alt_src"],
            "flag": flags.get(name, ("", ""))[0],
        })
        stats["kept_" + bucket] += 1

    for d in (HERO_DIR, PROOF_DIR):
        os.makedirs(d, exist_ok=True)
    for k in kept:
        shutil.copy2(k["src"], os.path.join(REPO, k["new_path"]))

    man = os.path.join(PROOF_DIR, "MANIFEST.tsv")
    with open(man, "w") as f:
        f.write("new_path\tbucket\tpost_id\tfile_index\tasset_type\tresume_value\talt\talt_source\tflag\n")
        for k in kept:
            f.write("\t".join((k[c] or "").replace("\t", " ") for c in
                    ["new_path", "bucket", "post_id", "file_index", "asset_type",
                     "resume_value", "alt", "alt_source", "flag"]) + "\n")

    # asset index -> usable images, for the content pages and journal posts
    idx = collections.defaultdict(lambda: {"hero": [], "proof": []})
    for k in kept:
        idx[k["asset"]][k["bucket"]].append(k["new_path"])
    with open(os.path.join(STAGE, "by_asset.tsv"), "w") as f:
        f.write("asset\thero\tproof_n\tproof_paths\n")
        for a in sorted(idx, key=int):
            v = idx[a]
            f.write(f"{a}\t{len(v['hero'])}\t{len(v['proof'])}\t"
                    f"{','.join(v['hero'] + v['proof'])}\n")

    print("plan rows        :", len(rows))
    for k in sorted(stats):
        print(f"  {k:<16}: {stats[k]}")
    print("manifest         :", man)
    tb = sum(os.path.getsize(os.path.join(REPO, k['new_path'])) for k in kept)
    print("ingested bytes   : %.1f MB" % (tb / 1048576))
    print("hero w/ visual alt:", sum(1 for k in kept if k["alt_source"] == "visual"),
          "| generic:", sum(1 for k in kept if k["alt_source"] == "generic"))
    print("by year:", sorted(collections.Counter(k["new_path"].split("-")[1] for k in kept).items()))

main()
