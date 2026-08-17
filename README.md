# Political Pulse

An open data attention tracker for the 2026 US Senate midterms, built by [Juicer](https://www.juicer.io).

Live site: https://juicer-political-pulse.netlify.app

## What it measures
- News coverage volume and tone (GDELT DOC 2.0, 28 days)
- Wikipedia attention (Wikimedia Pageviews API, 14 days)
- Verified Bluesky presence and engagement (public AT Protocol appview)

Both parties measured with identical queries, windows and math. No predictions.

## Pipeline
- `pipeline.py` pulls all data from public keyless APIs into `data/data.json`
- `patch_gdelt.py` backfills GDELT results around its rate limits
- `build_site.py` generates the static site into `site/`

## Powered by Juicer
Juicer aggregates social feeds across Instagram, Facebook, X, TikTok, YouTube, Reddit and Bluesky.
Senators, parliaments, city governments and campaigns use it to show live social walls on their websites.
API docs: https://developers.juicer.io
