#!/usr/bin/env python3
"""Generate the 开发者日志 (_posts) timeline from the personal asset library.

Read-only on the source library; writes only into _posts/.

Design rules (these are load-bearing — see AGENTS.md and the site plan):

* ALLOWLIST, not denylist. Only `date`, `text`, `venue`/`city` and the
  positionally-matched kept image for that post are ever emitted. Fields such as
  `comments`, `likes`, `n_likes`, `ocr_text` and every `url`/`proxy` field are
  dropped on the floor: they contain third-party names and WeChat CDN links.
* Two private inputs gate publication and are never committed:
    bin/journal_denylist.private.txt   whole-post ids to exclude
    bin/check_claims.private.rules     FORBIDDEN_NAME / PRIVACY_STRING rules
  If either is missing the script exits 2 rather than publishing "clean" output.
* Generic redaction runs before the sieve: phone numbers, emails, long digit
  runs (ids), WeChat sticker codes, and support.weixin.qq.com links.
* Filenames are pure ASCII because `permalink: /blog/:year/:title/` would put
  CJK in URLs; the post id keeps them unique and stable.
* Two-stage pipeline. This script only ever produces **drafts**: a truncated
  first-sentence title, the raw Moments text as one blob, and `polished: false`.
  A separate editorial pass rewrites each draft into blog prose (real title,
  paragraphing, first-person voice, third-party notices moved into `>` quotes),
  derives `description:` from the post's own first sentence, and stamps
  `polished: true`. Re-running this script skips any post already marked
  `polished: true` unless `--force` is given — and `--force` therefore throws
  away that editorial work. After any regeneration, re-run the editorial pass
  and then `bash bin/check_claims.sh` and `bash bin/check_internal_links.sh`:
  neither gate is wired into CI (check_claims.sh needs a gitignored rules file),
  so they only protect you if you run them.

Usage:
    python3 bin/build_journal_posts.py --dry-run     # stats + samples only
    python3 bin/build_journal_posts.py --write       # emit _posts/*.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from collections import Counter, defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.expanduser("~/Downloads/个人履历资产库")
SRC = os.path.join(LIB, "raw", "sns_self_enriched.json")
MANIFEST = os.path.join(REPO, "assets", "proof", "MANIFEST.tsv")
DENY = os.path.join(REPO, "bin", "journal_denylist.private.txt")
RULES = os.path.join(REPO, "bin", "check_claims.private.rules")
POSTS = os.path.join(REPO, "_posts")

HARD_CEILING = dt.date(2026, 10, 13)  # no `future:` key in _config.yml

# --- topic vocabulary (public, non-sensitive) --------------------------------
ERAS = [
    (2018, 2019, "校园创客与硬件启蒙"),
    (2020, 2022, "创业、公益与工程训练"),
    (2023, 2024, "医疗硬件与工业现场"),
    (2025, 2026, "具身智能真机闭环"),
]

# keyword -> tag. First match wins, so order from specific to generic.
TAGS = [
    ("机器狗", ("机器狗", "四足", "quadruped", "宇树", "dmcan", "robodog")),
    ("机械臂", ("机械臂", "manipulat", "so-10", "so100", "so101", "双臂", "夹爪", "灵巧手")),
    ("具身智能", ("具身", "embodied", "vla", "world model", "wall-oss")),
    ("大模型", ("大模型", "llm", "gpt", "chatgpt", "gemini", "qwen", "cursor", "agent", "智能体", "rag")),
    ("黑客松", ("黑客松", "hackathon", "马拉松", "巅峰赛", "hacker house")),
    ("竞赛荣誉", ("一等奖", "二等奖", "三等奖", "冠军", "金奖", "获奖", "答辩", "挑战杯", "竞赛")),
    ("演讲布道", ("演讲", "分享", "直播", " AMA", "沙龙", "大会", "培训", "宣讲", "speaker")),
    ("开源生态", ("开源", "github", "gitlab", "wiki", "知识库", "社区", "sdk", "中间件")),
    ("硬件设计", ("pcb", "3d打印", "光固化", "舵机", "电机", "焊接", "示波器", "结构", "模具", "smt", "打样")),
    ("视觉与传感", ("视觉", "相机", "摄像头", "slam", "雷达", "点云", "深度", "标定", "imu", "uwb")),
    ("VR与交互", ("vr", "ar", "头显", "遥操作", "交互", "unity", "ue4", "unreal")),
    ("公益与社会服务", ("公益", "扶贫", "危房", "养老", "助残", "志愿", "勤工助学", "乡村")),
    ("创业经营", ("公司", "客户", "订单", "交付", "量产", "供应商", "注册", "商标", "软著", "团队")),
    ("校园生活", ("宿舍", "食堂", "社团", "课程", "考试", "毕设", "实验室日常", "同学")),
]

# Generic, category-level text sieve. Deliberately broad: anything that smells
# like hiring, payroll, tax, benefits, medical leave, personal finance, ID
# numbers, credentials or private chat never becomes a public log entry.
SIEVE = re.compile(
    "|".join(
        [
            "招聘", "急招", "求职", "简历", "内推", "岗位", "薪资", "年薪", "月薪", "工资",
            "实习证明", "离职", "辞职", "入职", "社保", "公积金", "发票", "报税", "纳税", "税",
            "减资", "转账", "红包", "回款", "咨询费", "报价", "成本价", "营收", "营业额", "流水",
            "持仓", "股票", "基金", "币", "收益", "奖金", "补助", "报销",
            "学号", "身份证", "护照", "营业执照", "统一社会信用代码", "开户", "银行卡",
            "私聊", "私信我", "加我", "微信号", "电话我", "1[3-9][0-9]{9}",
            "挂科", "补考", "处分", "投诉", "纠纷", "殴打", "报警", "起诉",
            "发烧", "生病", "住院", "躺了一周", "无语了", "心态崩", "抑郁",
            "看病", "血检", "尿检", "挂号", "肚子疼",
            "女朋友", "相亲", "表白",
            # Buying / selling / hiring classifieds are not engineering logs.
            "兼职", "报酬", "日薪", "包差旅", "转让", "下单有优惠", "招一名", "欢迎自荐",
            # Named private individuals: a public log thanks organisations, not
            # people who never agreed to appear on this site.
            "教授", "博士生", "博士生导师", "日电（记者", "新华社",
            # Credentials. A 2018 ops tutorial quoted a live root server IP and
            # password verbatim; nothing that looks like a login block survives.
            r"(?i:(?:password|passwd|pwd|secret|token))\s*[:：=]",
            r"(?i:username)\s*[:：]",
            r"(?i:IP\s*Address)",
            # Classified-ad style solicitations: personal handles or named
            # third-party contacts, which are not what this log is for.
            r"微信[:：]?\s*[A-Za-z][A-Za-z0-9_\-]{4,}",
            r"有意者?请联系", "有意向请联系", "招募合伙人",
            r"欢迎联系[\u4e00-\u9fa5]{2,4}",
            # Claim discipline: bin/check_claims.sh rejects these strings
            # site-wide, so a quoted vendor blurb or an old self-description
            # must not smuggle them back in through an archived log entry.
            "首创", "全球第一", "事实标准", "行业标准", "行业基础设施", "被产业界采用",
            "发起人", "全赛道", "营收", "营业额", "外观专利", "Kafka", "Go 微服务",
            "4,?733", "631\\s*户", "298\\s*户", "48\\s*项", "34\\s*所高校",
        ]
    )
)

STICKER = re.compile(r"\[[^\[\]]{1,8}\]")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
PHONE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
LONG_DIGITS = re.compile(r"(?<!\d)\d{9,}(?!\d)")
WEIXIN_LINK = re.compile(r"https?://[^\s]*support\.weixin\.qq\.com[^\s]*")
# Internal ops links (shared forms, doc shares) are not citations and can let a
# reader post into someone's workflow; drop them entirely.
FORM_LINK = re.compile(
    r"https?://[^\s]*(?:feishu\.cn|docs\.qq\.com|shimo\.im|wjx\.cn|jiandaoyun\.com|notion\.site)[^\s]*", re.I
)
# App "share" links carry the sharer's account id in the query string
# (e.g. coolapk ?shareUid=…). Keep scheme+host+path only.
URL_QUERY = re.compile(r"(https?://[^\s/?#]+/[^\s?#]*)[?#][^\s]*")
WS = re.compile(r"[ \t\u2005]+")
BIDI = re.compile("[\u202a-\u202e\u2066-\u2069]")
# Bidi / zero-width / C0-C1 control characters survive from Moments text that was
# copied out of other apps. They scramble title rendering in a browser, so they
# never reach a post file.
CONTROL = re.compile(
    "[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f-\u009f"
    "\u200b-\u200f\u202a-\u202e\u2060-\u2069\ufeff]"
)
EMOJI_ONLY = re.compile(r"^[\W_]+$", re.UNICODE)

ERA_BY_YEAR = {}
for lo, hi, name in ERAS:
    for y in range(lo, hi + 1):
        ERA_BY_YEAR[y] = name


def load_private() -> tuple[set[str], list[str], list[str]]:
    for path in (DENY, RULES):
        if not os.path.exists(path):
            sys.exit(f"FATAL: missing private gate file {path} — refusing to generate.")
    ids = set()
    with open(DENY, encoding="utf-8") as fh:
        for line in fh:
            line = line.split("#", 1)[0].strip()
            if line:
                ids.add(line)
    names, secrets = [], []
    with open(RULES, encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("@@@")
            if len(parts) < 3:
                continue
            kind, value = parts[0], parts[1]
            if kind == "FORBIDDEN_NAME":
                names.append(value)
            elif kind == "PRIVACY_STRING":
                secrets.append(value)
    if not ids or not names:
        sys.exit("FATAL: private gate files look truncated — refusing to generate.")
    return ids, names, secrets


def load_images() -> dict[str, list[str]]:
    """post_id -> kept image site paths, hero first then proof order."""
    by_post: dict[str, list[str]] = defaultdict(list)
    with open(MANIFEST, encoding="utf-8") as fh:
        header = fh.readline()
        assert header.startswith("new_path"), "unexpected MANIFEST header"
        for line in fh:
            cols = line.rstrip("\n").split("\t")
            if len(cols) < 4 or cols[1] not in ("hero", "proof"):
                continue
            path, bucket, post_id = cols[0], cols[1], cols[2]
            by_post[post_id].append((0 if bucket == "hero" else 1, path))
    return {k: [p for _, p in sorted(v, key=lambda t: (t[0], t[1]))] for k, v in by_post.items()}


def clean(text: str) -> str:
    text = CONTROL.sub("", text)
    text = WEIXIN_LINK.sub("", text)
    text = FORM_LINK.sub("", text)
    text = URL_QUERY.sub(r"\1", text)
    text = STICKER.sub("", text)
    text = EMAIL.sub("", text)
    text = PHONE.sub("", text)
    text = LONG_DIGITS.sub("", text)
    text = text.replace("\r", "\n")
    text = WS.sub(" ", text)
    lines = [ln.strip() for ln in text.split("\n")]
    return "\n".join(ln for ln in lines if ln).strip()


def tag_for(text: str) -> list[str]:
    low = text.lower()
    hits = [tag for tag, kws in TAGS if any(k in low for k in kws)]
    return hits[:3] or ["开发者日志"]


def make_title(text: str) -> str:
    first = re.split(r"[。！？!?；;\n]", text.strip())[0]
    first = re.sub(r"^[#✨🔥🚀\s]+", "", first).strip()
    if len(first) < 6:
        first = text.strip().split("\n")[0]
    return (first[:38] + "…") if len(first) > 38 else first


def eligible(item: dict, deny: set[str], names: list[str], secrets: list[str], min_len: int) -> tuple[bool, str]:
    pid = str(item.get("id") or "")
    if not pid or pid in deny:
        return False, "denylisted"
    date_s = item.get("date") or ""
    try:
        d = dt.date.fromisoformat(date_s)
    except ValueError:
        return False, "no-date"
    if d > HARD_CEILING:
        return False, "future"
    body = clean(str(item.get("text") or ""))
    # Text that travelled through an RTL isolate comes back character-reversed
    # ("你北们理工…" for "们北理工你…"). Removing the control marks does not restore
    # the order, and publishing scrambled Chinese is worse than publishing less.
    if BIDI.search(str(item.get("text") or "")):
        return False, "bidi"
    if len(body) < min_len or EMOJI_ONLY.match(body):
        return False, "too-short"
    if SIEVE.search(body):
        return False, "sieve"
    for n in names:
        if n in body:
            return False, "forbidden-name"
    for s in secrets:
        if re.search(s, body):
            return False, "privacy-string"
    return True, "ok"


def render(item: dict, body: str, images: list[str], era: str, tags: list[str]) -> str:
    """Emit the *unpolished* draft of one log entry.

    This is stage 1 of a two-stage pipeline. The draft keeps the original wording
    verbatim (after privacy filtering) and is deliberately rough: run-on sentences,
    a truncated title, Moments-style "P1/P2" photo references. Stage 2 is a manual
    editorial pass that rewrites each draft into blog prose and then stamps
    `polished: true` into the front matter — which makes this generator skip the
    file on every later run, so re-filtering never clobbers edited copy.
    """
    d = item["date"]
    stamp = f'{d} {(item.get("datetime") or d + " 00:00").split(" ")[1]}:00'
    venue = clean(str(item.get("venue") or item.get("city") or ""))[:40]
    fm = [
        "---",
        "layout: post",
        f"title: {make_title(body)}",
        f"date: {stamp}",
        f"tags: {' '.join(tags)}",
        f"categories: {era}",
        "author: 张振尧",
    ]
    if images:
        fm.append(f"thumbnail: {images[0]}")
    fm.append("related_posts: true")
    fm.append("polished: false")
    fm.append("---")
    fm.append("")
    if venue:
        fm.append(f"_地点：{venue}_")
        fm.append("")
    for line in body.split("\n"):
        fm.append(line)
    if images:
        fm.append("")
        fm.append('<div class="row g-2 my-3">')
        for path in images[:4]:
            fm.append(
                '  <div class="col-6 col-md-3">'
                f'<a href="/{path}" target="_blank" rel="noopener noreferrer">'
                f'<img src="/{path}" class="img-fluid rounded border" loading="lazy" alt="{d} 现场记录"></a></div>'
            )
        fm.append("</div>")
    fm.append("")
    return "\n".join(fm)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument(
        "--force",
        action="store_true",
        help="overwrite posts even when they are already marked `polished: true`",
    )
    args = ap.parse_args()

    deny, names, secrets = load_private()
    images = load_images()
    items = json.load(open(SRC, encoding="utf-8"))

    stats: Counter[str] = Counter()
    chosen = []
    seen_dates: set[str] = set()
    for item in sorted(items, key=lambda x: x.get("date") or ""):
        pid = str(item.get("id") or "")
        imgs = [p for p in images.get(pid, []) if not p.startswith("dropped")]
        # A dated photo plus a one-line caption is still a valid log entry, so
        # image-bearing posts get a lower text floor than text-only ones.
        ok, why = eligible(item, deny, names, secrets, 16 if imgs else 30)
        stats[why] += 1
        if not ok:
            continue
        d = item["date"]
        key = d
        body = clean(str(item["text"]))
        if len(body) < 60 and not imgs:
            stats["thin"] += 1
            continue
        if key in seen_dates and len(chosen) > 220:
            stats["dup-date"] += 1
            continue
        era = ERA_BY_YEAR.get(int(d[:4]), "开发者日志")
        tags = tag_for(body)
        chosen.append((d, pid, render(item, body, imgs, era, tags)))
        seen_dates.add(key)
        stats["chosen"] += 1

    if args.limit:
        chosen = chosen[: args.limit]

    tag_counts: Counter[str] = Counter()
    era_counts: Counter[str] = Counter()
    with_img = 0
    for _, _, text in chosen:
        head = text.split("---\n")[1]
        for line in head.splitlines():
            if line.startswith("tags:"):
                tag_counts.update(line.split(":", 1)[1].split())
            elif line.startswith("categories:"):
                era_counts[line.split(":", 1)[1].strip()] += 1
        if "\nthumbnail:" in head:
            with_img += 1

    print("stats:", dict(stats))
    print("posts:", len(chosen), "with image:", with_img)
    print("eras:", dict(era_counts))
    print("top tags:", tag_counts.most_common(20))
    print("config snippet:")
    print("  display_tags:", [t for t, _ in tag_counts.most_common(12)])
    print("  display_categories:", [e for e, _ in era_counts.most_common()])

    if args.dry_run or not args.write:
        for d, pid, text in chosen[-2:]:
            print("=" * 70, "\n", text[:900])
        if not args.write:
            print("(dry run — nothing written)")
        return 0

    os.makedirs(POSTS, exist_ok=True)
    written = kept = 0
    for d, pid, text in chosen:
        path = os.path.join(POSTS, f"{d}-log-{pid}.md")
        # Never overwrite a post that has already been through the editorial pass.
        if not args.force and os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                if "polished: true" in fh.read():
                    kept += 1
                    continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        written += 1
    print("written:", written, "kept (already polished):", kept)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
