#!/usr/bin/env bash
# Offline internal-link and asset resolver for the built site.
#
# This is the local equivalent of what .github/workflows/broken-links-site.yml
# does with `lychee --offline`, except that workflow only runs AFTER a deploy —
# so it reports breakage on the live site rather than preventing it. Run this
# before pushing.
#
# Usage:
#   bin/check_internal_links.sh                 # copy _site out of the docker container
#   bin/check_internal_links.sh /path/to/_site  # check an existing build directory
#
# Exit status: 0 = no broken internal references, 1 = broken references found.
#
# Notes:
#   * Percent-encoded CJK asset paths are decoded before the existence check.
#     A naive checker reports `/assets/img/awards/%E8%8B%B1...jpg` as broken
#     even though the raw-CJK file is on disk and GitHub Pages serves it fine.
#   * Only site-internal refs (leading "/") are checked. External URLs are
#     lychee's job, and checking them here would make this script network-
#     dependent and slow.
set -uo pipefail

cd "$(dirname "$0")/.." || exit 1

SITE="${1:-}"
TMP_COPIED=0

if [ -z "$SITE" ]; then
  SITE="$(mktemp -d)/_site"
  TMP_COPIED=1
  echo "Copying _site out of the jekyll container..."
  if ! docker compose cp jekyll:/tmp/_site "$SITE" >/dev/null 2>&1; then
    echo "error: could not copy _site from container. Is it running? Try:" >&2
    echo "  docker compose up -d" >&2
    exit 2
  fi
fi

if [ ! -d "$SITE" ]; then
  echo "error: $SITE is not a directory" >&2
  exit 2
fi

cleanup() { [ "$TMP_COPIED" = "1" ] && rm -rf "$(dirname "$SITE")"; }
trap cleanup EXIT

echo "Checking $SITE ($(find "$SITE" -name '*.html' | wc -l | tr -d ' ') html pages, $(du -sh "$SITE" | cut -f1))"
echo

SITE="$SITE" python3 - <<'PY'
import html
import os
import re
import sys
import urllib.parse

site = os.environ["SITE"]
ref_pat = re.compile(r'(?:href|src)="(/[^"]*)"')

# url -> set of pages that reference it
refs = {}
for root, _dirs, files in os.walk(site):
    for fn in files:
        if not fn.endswith(".html"):
            continue
        path = os.path.join(root, fn)
        try:
            txt = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        for m in ref_pat.findall(txt):
            refs.setdefault(html.unescape(m), set()).add(os.path.relpath(path, site))


def resolves(url):
    """True if the URL maps to a file, a directory with index.html, or <path>.html."""
    path = url.split("#")[0].split("?")[0]
    if not path:  # bare "/" or "/#anchor" -> site root
        path = "/"
    decoded = urllib.parse.unquote(path)
    target = os.path.join(site, decoded.lstrip("/"))
    if os.path.isfile(target):
        return True
    if os.path.isdir(target) and os.path.isfile(os.path.join(target, "index.html")):
        return True
    if os.path.isfile(target.rstrip("/") + "/index.html"):
        return True
    if os.path.isfile(target + ".html"):
        return True
    return False


broken = {u: pages for u, pages in refs.items() if not resolves(u)}
print(f"unique internal refs: {len(refs)}")
print(f"broken:               {len(broken)}")

if broken:
    print()
    for url in sorted(broken):
        print(f"  BROKEN  {url}")
        for page in sorted(broken[url])[:5]:
            print(f"            <- /{page}")
        if len(broken[url]) > 5:
            print(f"            <- ...and {len(broken[url]) - 5} more")
    sys.exit(1)

print("\nAll internal references resolve.")
PY
status=$?

exit $status
