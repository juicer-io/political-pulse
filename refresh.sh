#!/usr/bin/env bash
# Full Political Pulse refresh: attention, followers, posts, rebuild, deploy.
# Run every 14 days (see .github/workflows/refresh.yml or run manually).
set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
$PY filler_us.py || true          # wikipedia attention, US then AU (rate-limit tolerant)
$PY fetch_x_followers.py          # X followers via Juicer API
$PY fetch_posts_us.py             # senate walls (add --house when extended)
$PY build_site.py
if [ -n "${NETLIFY_SITE_ID:-}" ]; then
  npx --yes netlify-cli deploy --prod --dir site --site "$NETLIFY_SITE_ID"
else
  SITE=$(grep -o '[a-f0-9-]\{36\}' .netlify-site-id)
  netlify deploy --prod --dir site --site "$SITE"
fi
