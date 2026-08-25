#!/usr/bin/env bash
# Resolve a batch of vt.tiktok.com share URLs → product_id + title via the
# og_info embedded in the 301-redirect URL. This bypasses the SlardarWAF
# captcha that blocks the actual product detail pages.
#
# Usage:
#   ./resolve_vt_urls.sh urls.txt > products.tsv
#
# Input:  text file, one vt.tiktok.com URL per line
# Output: TSV with columns: short_code | product_id | decoded_title
#
# Notes:
#   - Honors HTTPS / MAX redirects / timeout
#   - UA set to common desktop (no bypass claim — TikTok is fine here because
#     we never trigger WAF; only the redirect server responds)
#   - For 14 URLs on a normal connection, takes ~15-30s
#   - Does NOT fetch the product detail page (that path hits captcha)

set -euo pipefail

UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <urls.txt>" >&2
  echo "  urls.txt: one vt.tiktok.com URL per line" >&2
  exit 1
fi

URL_FILE="$1"

if [[ ! -f "$URL_FILE" ]]; then
  echo "File not found: $URL_FILE" >&2
  exit 1
fi

echo "short_code|product_id|decoded_title"

while IFS= read -r url || [[ -n "$url" ]]; do
  # skip blanks + comments
  [[ -z "$url" || "$url" =~ ^# ]] && continue

  short_code=$(echo "$url" | sed -nE 's|.*/(ZS[^/]+)/?$|\1|p')
  if [[ -z "$short_code" ]]; then
    echo "PARSE_ERROR|||" >&2
    continue
  fi

  final_url=$(curl -sL -o /dev/null -w '%{url_effective}' \
    --max-redirs 5 --max-time 15 \
    -A "$UA" "$url" 2>/dev/null || echo "")

  if [[ -z "$final_url" ]]; then
    echo "$short_code|FAILED|||"
    continue
  fi

  # Extract product_id from /view/product/{ID} path
  product_id=$(echo "$final_url" | sed -nE 's|.*/view/product/([0-9]+).*|\1|p')
  if [[ -z "$product_id" ]]; then
    echo "$short_code|NO_PRODUCT_ID||"
    continue
  fi

  # Extract og_info title (URL-encoded JSON inside the final URL)
  og_info=$(echo "$final_url" | sed -nE 's|.*[?&]og_info=([^&]+).*|\1|p' | python3 -c '
import sys, urllib.parse, json
raw = sys.stdin.read().strip()
if not raw:
    print("")
    sys.exit(0)
try:
    # og_info is double-encoded in the URL — decode twice
    once = urllib.parse.unquote(raw)
    twice = urllib.parse.unquote_once(once) if once else ""
    # try parsing as JSON first
    for candidate in (once, twice):
        try:
            obj = json.loads(candidate)
            print(obj.get("title", ""))
            sys.exit(0)
        except Exception:
            continue
    # fallback: just return decoded string up to first &
    print(urllib.parse.unquote_plus(raw).split("&")[0])
except Exception:
    print("")
')

  # Replace tabs / pipes in title so TSV stays parseable
  safe_title=$(echo "$og_info" | tr '\t|' '  ')

  echo "$short_code|$product_id|$safe_title"
done < "$URL_FILE"
