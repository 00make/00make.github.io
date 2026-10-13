#!/usr/bin/env python3
"""Stage 2 selector: join resume_assets.json evidence -> on-disk Moments media,
apply the privacy blocklist, bucket into hero/proof, emit the transform plan."""
import json, os, re, sys, glob, collections

LIB = os.environ.get("RESUME_LIB", "/Users/max/Downloads/个人履历资产库")
MEDIA = os.path.join(LIB, "evidence/sns_self_export/media")
FRAMES = os.path.join(LIB, "evidence/frames")
OUT = os.environ.get("STAGE2_OUT", "/Users/max/.stage2")

# Whole-post ban: these Moments posts must never be published in any form.
BANNED_POSTS = {
    "13115959418939445327",  # 实习证明, exposes 学号
    "13199729329019031637",  # 微信转账记录
    "13765953714521837768",  # 私聊截图 (third-party name)
    "13222288603235618872",  # 群聊截图 (third-party names)
    "13375982735844380758",  # 私聊截图
    "14883698989262770803",  # 群聊截图
    "14676224291064648272",  # 股票/加密持仓录屏 + 已装应用列表
    "14640901784026485323",  # 礼堂满座未成年人学生
    "13053660164394389584",  # 营业执照
    "13582607130138120434",  # 营业执照
    "13870459481523097800",  # 发明专利证书, 发明人非本人
    "14942396303284441709",  # 短信签到提醒 (time + address)
    "13181905918145663063",  # 工行营业厅内
    "14966168407575302770",  # 新华社权威快报 (political)
}
# Per-file ban: the post stays usable, these indexes do not ship.
BANNED_FILES = {
    "14660503463249908311_0",  # 离职证明
    "14660503463249908311_5",  # 记账截图 单月收入
    "14660503463249908311_8",  # 社保增员表
    "14660503463249908311_7",  # 与他人合影的自拍, 未复核 -> 保守排除
}
# Redaction for alt text: never name these on the site.
ALT_DENY = ["王明玥", "王玥玥", "熊矿箭", "幺巧宇", "金成宇", "石予童", "颜昊清",
            "2017110005", "112,238", "112238", "91110108MA01JBX3"]

CAT_SLUG = {
    "机器人硬件": "robot", "媒体IP": "media", "竞赛荣誉": "award",
    "项目经历": "project", "公司商业": "company", "演讲布道": "talk",
    "知识产权": "ip", "媒体曝光": "press", "知产资质": "qual",
    "行业背书": "endorse",
}
Q90 = {"证书", "海报", "PPT", "截图", "奖杯"}


def redact(s):
    s = re.sub(r"\s+", " ", s or "").strip()
    for d in ALT_DENY:
        s = s.replace(d, "［已隐去］")
    s = re.sub(r"[|｜]", " · ", s)
    s = s.replace('"', "'").replace("\t", " ")
    return s[:150]


def main():
    assets = json.load(open(os.path.join(LIB, "resume_assets.json")))["assets"]
    disk = collections.defaultdict(list)
    for p in glob.glob(os.path.join(MEDIA, "*.jpg")):
        b = os.path.basename(p)
        m = re.match(r"^(\d+)_(\d+)\.jpg$", b)
        if m:
            disk[m.group(1)].append((int(m.group(2)), p))
    for k in disk:
        disk[k].sort()

    rows, dropped = [], collections.Counter()
    for i, x in enumerate(assets):
        e = x["evidence"]
        posts = ([str(e["post_id"])] if e.get("post_id") else []) + \
                [str(p) for p in (e.get("post_ids") or [])]
        seen, files, allowed_posts = set(), [], set()
        for p in posts:
            if p in seen:
                continue
            seen.add(p)
            if p in BANNED_POSTS:
                dropped["banned_post"] += len(disk.get(p, []))
                continue
            for idx, path in disk.get(p, []):
                key = "%s_%d" % (p, idx)
                if key in BANNED_FILES:
                    dropped["banned_file"] += 1
                    continue
                files.append((p, idx, path))
                allowed_posts.add(p)
        if not files:
            continue
        vf = e.get("visible_facts") or []
        atype = (e.get("asset_type") or "").strip()
        score = (2 if e.get("image_verified") else 0) + \
                (1 if x.get("star_details") else 0) + \
                (1 if atype in Q90 else 0) + \
                min(int(e.get("total_likes") or 0) / 100.0, 4)
        year = (x.get("start_date") or "0000")[:4]
        cat = CAT_SLUG.get(x["category"], "misc")
        n_posts = len(allowed_posts)
        for n, (pid, idx, path) in enumerate(files):
            # Positional fact->image matching is only credible inside a single-post
            # asset; merged multi-post assets misalign and get a generic caption.
            trust = n_posts == 1 and vf
            alt = redact(vf[n]) if trust and n < len(vf) else ""
            rows.append({
                "asset": i, "year": year, "cat": cat, "title": redact(x["title"]),
                "post": pid, "idx": idx, "src": os.path.relpath(path, LIB),
                "atype": atype, "q": 90 if atype in Q90 else 82,
                "score": round(score, 2), "alt": alt, "n_img": len(files),
                "alt_src": ("positional" if len(vf) == len(files) else "partial")
                           if trust else "generic",
            })

    # Hero bucket: top-ranked assets, 1 image each, capped at 150.
    by_asset = collections.defaultdict(list)
    for r in rows:
        by_asset[r["asset"]].append(r)
    ranked = sorted(by_asset.values(), key=lambda rs: -rs[0]["score"])
    hero_keys = set()
    for rs in ranked:
        if len(hero_keys) >= 150:
            break
        rs.sort(key=lambda r: (r["q"] != 90, r["idx"]))
        hero_keys.add((rs[0]["asset"], rs[0]["post"], rs[0]["idx"]))
    for r in rows:
        r["bucket"] = "hero" if (r["asset"], r["post"], r["idx"]) in hero_keys else "proof"
        stem = "%03d-%s-%s_%s-%d" % (r["asset"], r["year"], r["cat"], r["post"], r["idx"])
        r["dest"] = ("assets/img/journal/" if r["bucket"] == "hero" else "assets/proof/") + stem + ".jpg"

    os.makedirs(OUT, exist_ok=True)
    missing = [r for r in rows if not os.path.isfile(os.path.join(LIB, r["src"]))]
    rows = [r for r in rows if os.path.isfile(os.path.join(LIB, r["src"]))]
    with open(os.path.join(OUT, "plan.tsv"), "w") as f:
        f.write("\t".join(["asset", "year", "cat", "title", "post", "idx", "src",
                           "atype", "q", "bucket", "dest", "alt", "n_img", "alt_src"]) + "\n")
        for r in rows:
            f.write("\t".join(str(r[k]) for k in ["asset", "year", "cat", "title", "post",
                       "idx", "src", "atype", "q", "bucket", "dest", "alt", "n_img",
                       "alt_src"]) + "\n")
    print("missing on disk:", len(missing))

    print("planned images :", len(rows))
    print("hero :", sum(1 for r in rows if r["bucket"] == "hero"),
          "| proof :", sum(1 for r in rows if r["bucket"] == "proof"))
    print("assets with images :", len(by_asset))
    print("dropped:", dict(dropped))
    print("empty alt :", sum(1 for r in rows if not r["alt"]))
    print("alt_src :", collections.Counter(r["alt_src"] for r in rows).most_common())
    print("hero w/ alt:", sum(1 for r in rows if r["bucket"] == "hero" and r["alt"]))
    print("by cat :", collections.Counter(r["cat"] for r in rows).most_common())
    print("by atype:", collections.Counter(r["atype"] for r in rows).most_common())
    tb = sum(os.path.getsize(os.path.join(LIB, r["src"])) for r in rows)
    print("source bytes : %.1f MB" % (tb / 1048576))


main()
