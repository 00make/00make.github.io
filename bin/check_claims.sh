#!/usr/bin/env bash
# Content-compliance gate: scans published content for forbidden claims,
# forbidden role wording, wrong numbers, and privacy-blocked evidence.
#
# Every rule below traces to either
#   * views/resume_final.md 「已确认对外口径（本人 2026-10-13 定稿）」, or
#   * the owner's explicit privacy exclusions.
# Do not loosen a rule without the owner's say-so.
#
# Usage:
#   bin/check_claims.sh              # scan the published content tree
#   bin/check_claims.sh --quiet      # summary + exit status only
#
# Exit status: 0 = clean, 1 = violations found.
#
# Scope note: scans only what Jekyll actually publishes. README.md, docs/,
# AGENTS.md and the pages listed in _config.yml `exclude:` are skipped —
# wording in those files never reaches a visitor.
set -uo pipefail

cd "$(dirname "$0")/.." || exit 1

QUIET=0
[ "${1:-}" = "--quiet" ] && QUIET=1

# Content that gets published. _posts is listed even though it is currently
# empty, because the 开发者日志 stage fills it.
SCOPE=(_pages _projects _news _posts _data)

# Pages excluded from the build via _config.yml `exclude:`; not public.
EXCLUDE_FILES=(
  "_pages/about_einstein.md"
  "_pages/books.md"
  "_pages/dropdown.md"
  "_pages/plugins.md"
  "_pages/profiles.md"
  "_pages/publications.md"
  "_pages/repositories.md"
  "_pages/teaching.md"
)

# ---------------------------------------------------------------------------
# Rule table: <category>@@@<ERE regex>@@@<why / what to write instead>
#
# The delimiter is @@@ rather than "|" on purpose: ERE alternation uses "|",
# so a pattern like (年营收|营收) would be split mid-regex by `IFS='|' read`
# and silently match nothing. Keep patterns tight enough to avoid false
# positives, loose enough to catch spacing variants ("5项" vs "5 项").
# ---------------------------------------------------------------------------
RULES='FORBIDDEN_CLAIM@@@全球首款@@@口径禁用：TRI.ME「吹了么」只说「具身智能浴室理容机械臂领域创始人」
FORBIDDEN_CLAIM@@@全球第一@@@口径禁用：无佐证
FORBIDDEN_CLAIM@@@世界首创@@@口径禁用：无佐证
FORBIDDEN_CLAIM@@@首创@@@口径禁用：与「全球首款」同类主张。改用「打造…，本人为该领域创始人」
FORBIDDEN_CLAIM@@@事实标准@@@口径禁用：GitHub Star 数不支持该量级。改用「已开源并被开发者社区使用」
FORBIDDEN_CLAIM@@@行业基础设施@@@口径禁用：同上
FORBIDDEN_CLAIM@@@被产业界采用@@@口径禁用：同上
FORBIDDEN_CLAIM@@@行业标准@@@口径禁用：同上
FORBIDDEN_ROLE@@@探月.{0,30}发起人@@@口径禁用：官媒署名的发起人是社区创始人，公开报道未出现本人姓名。只说「探月具身智能社区 CTO、赛事主理人、决赛评委」
FORBIDDEN_ROLE@@@联合发起人@@@口径禁用：同上。awards.md / press.md / cv.yml 现有文案待改
FORBIDDEN_ROLE@@@组委会发起人@@@口径禁用：同上
FORBIDDEN_ROLE@@@发起人致辞@@@口径禁用：同上
FORBIDDEN_ROLE@@@作为发起人@@@口径禁用：裸「发起人」自称同样无公开佐证，改为「作为赛事模块主理人」
FORBIDDEN_ROLE@@@发起人之一@@@口径禁用：屋必安统一说「公司创始人」，不用「发起人之一 / 路演主讲」
FORBIDDEN_NUMBER@@@5[[:space:]]*项(国家)?发明专利@@@错误数字：本人发明专利为 1 项（申请中），且主题是扫描隧道显微镜减震体系，与医疗仿真无关
FORBIDDEN_NUMBER@@@48[[:space:]]*项.{0,6}软著@@@错误数字：软著为 8 项
FORBIDDEN_NUMBER@@@48[[:space:]]*项历史奖项@@@错误数字：应为「52 项荣誉证书、资质认证与注册商标」，且其中约 13 项非奖项
FORBIDDEN_NUMBER@@@4,?733@@@查无出处：全站旧用的 4,733 户在资产库 9 处佐证中零命中，正确口径为 4,784 户建档立卡贫困户
FORBIDDEN_NUMBER@@@631[[:space:]]*户@@@查无出处：与 4,733 同批的虚构伴生数字，正确口径为 985 户低保户危房改造
FORBIDDEN_NUMBER@@@298[[:space:]]*户@@@查无出处：同上
FORBIDDEN_NUMBER@@@(年营收|营业额)@@@不可验证：resume_final.md 全文无任何营收口径，只有奖金（8 万 / 10 万 / 累计逾 24 万）。删掉营收表述，改用「主导 5 款医疗仿真硬件产品」
FORBIDDEN_IP@@@外观专利@@@查无出处：资产库仅记软件著作权 8 份 + 发明专利 1 项（申请中），无外观专利
FORBIDDEN_NUMBER@@@34[[:space:]]*所(高)?校@@@查无出处：bucthole 记录只到「上线时间 + 多子域架构 + 校内热议」，无任何高校覆盖数
FORBIDDEN_NUMBER@@@(日活跃|DAU).{0,14}[0-9]@@@查无出处：资产库无 DAU / 注册用户量数据，树洞一律不提用户规模
FORBIDDEN_STACK@@@Kafka@@@虚构技术栈：树洞真实栈是 treehollow / React / WebSocket / reCAPTCHA / 多子域名，库内无 Kafka
FORBIDDEN_STACK@@@Go 微服务@@@虚构技术栈：同上，且网页版基于 P 大树洞开源 web 版 xmcp 二次构建
FORBIDDEN_CLAIM@@@全赛道(总)?冠军@@@夸大：定稿战绩为「1 项世界纪录 · 3 项冠军 · 4 项亚军」，该赛事并不存在「全赛道总冠军」这一头衔
FORBIDDEN_CLAIM@@@足球挑战赛(冠军|及|暨)@@@表述越界：库里「人形机器人足球赛」是 2025-05 清华站、其本人口径夺冠的独立条目，不是张江大赛的定稿成绩；张江定稿只记「应用场景挑战赛张江纪录第一名（¥10,000）」，两者不得合并成一句
FORBIDDEN_DATE@@@2025[^.]{0,4}(8|11)[^.]{0,4}月?.{0,20}人形机器人@@@日期错误：朋友圈 2025-05-29 定位张江科学会堂 + 媒体报道「29 日…在上海张江举行」，赛事为 2025-05
FORBIDDEN_NUMBER@@@18[[:space:]]*岁创立@@@推算性：需与身份证年龄对齐，改用「大学期间创立公司」
FORBIDDEN_NUMBER@@@19[[:space:]]*岁.{0,10}认定@@@推算性：同上
FORBIDDEN_NUMBER@@@七层技术栈均有已交付成果@@@需逐层对应到具体仓库/产品后才可使用
STALE_NAME@@@众绘@@@口径改名：统一为「北航虚拟现实国家重点研究院」，库内旧记为「北京众绘虚拟现实（国家重点研究院）」
STALE_ROLE@@@创新研发总监@@@口径改职：该段职务为「医疗仿真硬件负责人」，时间 2023-06 ~ 2025-02
FORBIDDEN_CLAIM@@@最大规模@@@不可验证的最高级，与「全球第一」同类：改用具体事实（首届 / 时间 / 地点 / 参赛规模），主观形容可留（最棒的场地、最大的舞台）
FORBIDDEN_NUMBER@@@观众[[:space:]]*[0-9]@@@不可验证：资产库无任何线上/线下观众规模佐证，一律不写观众人数（开发者日志 2025-05-30「观众10W+」、2025-12-21「22,000+ 位线上观众」已删）
FORBIDDEN_NUMBER@@@[0-9][0-9,.]*[[:space:]]*(W|w|万)?\+?[[:space:]]*(位|名)?[[:space:]]*(线上)?观众@@@不可验证：同上，覆盖「10W+ 观众」「22,000+ 位线上观众」等语序
FORBIDDEN_IP@@@[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}@@@隐私禁发：裸服务器 IP 一律不公开。自有域名可留；IP 早已易主，挂在自己的站上等于对现在的持有者做不实陈述
PRIVACY_STRING@@@[0-9]+[[:space:]]*位数@@@隐私禁发主题：个人收入金额不公开（「第一桶金（6位数）」已改为只留事件不留数字）
PRIVACY_POST@@@13115959418939445327@@@隐私禁发：实习证明，含学号
PRIVACY_POST@@@13199729329019031637@@@隐私禁发：微信转账记录
PRIVACY_POST@@@13765953714521837768@@@隐私禁发：私聊截图，含第三方姓名
PRIVACY_POST@@@13222288603235618872@@@隐私禁发：群聊截图，含第三方姓名
PRIVACY_POST@@@13375982735844380758@@@隐私禁发：私聊截图
PRIVACY_POST@@@14883698989262770803@@@隐私禁发：群聊截图
PRIVACY_POST@@@14676224291064648272@@@隐私禁发：股票/加密持仓录屏 + 已安装应用列表
PRIVACY_POST@@@14640901784026485323@@@隐私禁发：礼堂满座未成年人学生
PRIVACY_POST@@@13053660164394389584@@@隐私禁发：营业执照，含注册地址/信用代码/法人
PRIVACY_POST@@@13582607130138120434@@@隐私禁发：营业执照，同上
PRIVACY_POST@@@13870459481523097800@@@严重：该发明专利证书发明人非本人，发布会构成虚假专利署名
PRIVACY_FILE@@@14660503463249908311_0@@@隐私禁发：离职证明，且载明保密义务于离职后存续
PRIVACY_FILE@@@14660503463249908311_5@@@隐私禁发：记账截图，含单月收入具体金额
PRIVACY_FILE@@@14660503463249908311_8@@@隐私禁发：北京市社保增员表，含统一社会信用代码
PRIVACY_STRING@@@离职证明@@@隐私禁发主题
PRIVACY_STRING@@@社保增员@@@隐私禁发主题'

# ---------------------------------------------------------------------------
# Private rules — NOT committed.
#
# This repo is public (zhangzhenyao.com is served from 00make/00make.github.io,
# and a user-site repo has to be public for GitHub Pages). Two kinds of rule
# have to spell out a literal value in order to grep for it, and committing
# either kind would publish the very thing the rule exists to keep private:
#
#   1. personal identifiers — 学号, the monthly income figure, 统一社会信用代码;
#   2. FORBIDDEN_NAME rules for third parties whose name must never appear on
#      this site. Naming them here, in a public repo, would be the leak.
#
# They live in bin/check_claims.private.rules, which is gitignored. Format is
# identical to RULES above: category@@@regex@@@why
#
# The include is MANDATORY, not optional: if the file is missing the script
# exits 2 rather than reporting a false "clean". A privacy gate that silently
# degrades to a no-op is worse than no gate at all. (Consequence worth knowing:
# a fresh clone cannot run this gate until the private file is recreated.)
# ---------------------------------------------------------------------------
PRIVATE_RULES_FILE="bin/check_claims.private.rules"
if [ ! -f "$PRIVATE_RULES_FILE" ]; then
  echo "check_claims: ABORTED — missing $PRIVATE_RULES_FILE" >&2
  echo "That gitignored file holds the rules matching literal personal identifiers" >&2
  echo "(学号 / 单月收入 / 统一社会信用代码) plus the third-party name denylist." >&2
  echo "Without it the privacy gate cannot run, and reporting \"clean\" would be" >&2
  echo "meaningless. Restore it before trusting a pass." >&2
  exit 2
fi
RULES="$RULES
$(cat "$PRIVATE_RULES_FILE")"

report=$(mktemp)
trap 'rm -f "$report"' EXIT

total=0
rule_errors=0
rules_seen=0

while IFS= read -r line; do
  [ -z "$line" ] && continue

  # Split on the literal 3-char delimiter. `IFS='@@@' read` would NOT work here:
  # IFS treats each character separately, and more importantly the regex field
  # may itself contain "|" for ERE alternation.
  category="${line%%@@@*}"
  rest="${line#*@@@}"
  pattern="${rest%%@@@*}"
  why="${rest#*@@@}"

  # Guard 1 — the rule line must actually split into three fields. Without this,
  # a typo'd delimiter yields either pattern="" (matches every line, drowning the
  # report) or a truncated regex (matches nothing) — and both fail silently.
  if [ "$category" = "$line" ] || [ "$why" = "$rest" ]; then
    echo "RULE ERROR: malformed rule (want category@@@regex@@@why): $line" >&2
    rule_errors=$((rule_errors + 1))
    continue
  fi

  hits=$(grep -rnE --include='*.md' --include='*.yml' -- "$pattern" "${SCOPE[@]}" 2>/dev/null)
  rc=$?
  rules_seen=$((rules_seen + 1))
  # Guard 2 — grep exits 2 on a malformed regex. Never swallow that: an invalid
  # pattern would otherwise look identical to "no violations found".
  if [ "$rc" -gt 1 ]; then
    echo "RULE ERROR: invalid ERE /$pattern/ (grep exit $rc)" >&2
    rule_errors=$((rule_errors + 1))
    continue
  fi

  # Drop hits from pages that are excluded from the build.
  for f in "${EXCLUDE_FILES[@]}"; do
    hits=$(printf '%s\n' "$hits" | grep -v "^$f:")
  done
  hits=$(printf '%s\n' "$hits" | grep -v '^$' || true)
  [ -z "$hits" ] && continue

  n=$(printf '%s\n' "$hits" | wc -l | tr -d ' ')
  total=$((total + n))

  if [ "$QUIET" = "0" ]; then
    {
      echo "── $category  /$pattern/   [$n hit(s)]"
      echo "   why: $why"
      printf '%s\n' "$hits" | sed 's/^/   /' | cut -c1-200
      echo
    } >>"$report"
  fi
done <<<"$RULES"

[ "$QUIET" = "0" ] && cat "$report"

echo "────────────────────────────────────────"
echo "rules evaluated: $rules_seen   rule errors: $rule_errors"
if [ "$rule_errors" -gt 0 ]; then
  echo "check_claims: ABORTED — $rule_errors rule(s) failed to evaluate."
  echo "A green result is meaningless while any rule is broken; fix the rule table first."
  exit 2
fi
if [ "$total" -eq 0 ]; then
  echo "check_claims: clean — 0 violations across ${SCOPE[*]}"
  exit 0
fi
echo "check_claims: $total violation(s) found"
echo "Pre-existing hits in about.md / awards.md / press.md / cv.yml are exactly the"
echo "Stage 1 fact-correction worklist; across the campaign this count must only fall."
exit 1
