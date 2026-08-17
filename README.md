# Political Pulse

An open data attention tracker for politicians. Live example: https://juicer-political-pulse.netlify.app
(2026 US Senate midterms). Built by [Juicer](https://www.juicer.io), MIT licensed.

Track ANY set of politicians in ANY country: news coverage volume and tone (GDELT),
Wikipedia attention (Pageviews API) and verified Bluesky presence. No API keys needed.

## Quickstart (3 steps, Python 3.10+, no dependencies)

```bash
git clone <this repo> && cd political-pulse

# 1. Edit people.json: one entry per politician you want to track
#    (name, party, state, wiki article title, GDELT query, optional verified Bluesky handle)

# 2. Pull the data (a few minutes; GDELT is heavily rate limited, be patient)
python3 pipeline.py
python3 patch_gdelt.py   # backfills whatever GDELT throttled on the first pass

# 3. Generate the site
python3 build_site.py
```

The finished site is plain HTML in `site/`. Open `site/index.html` locally, or deploy it anywhere:
drag the folder into [Netlify Drop](https://app.netlify.com/drop), push to GitHub Pages, or any static host.

## Editing the roster (people.json)

```json
{
 "slug": "jon-ossoff",            // used in URLs
 "name": "Jon Ossoff",
 "party": "D",                    // D or R chip colors; extend build_site.py for other systems
 "state": "GA",
 "role": "Incumbent Senator",
 "race": "Georgia Senate",
 "wiki": "Jon_Ossoff",            // exact English Wikipedia article title
 "gdelt": "\"Jon Ossoff\"",      // GDELT query; add a disambiguating word for common names
 "bsky": "ossoff.bsky.social",   // ONLY verified accounts; null if none (parody accounts are everywhere)
 "bioguide": "O000174"            // US Congress photo id (unitedstates/images); null for non-members
}
```

## Ground rules baked in

- Identical queries, windows and math for every person regardless of party
- Verified Bluesky accounts only; absence is shown honestly as "not on Bluesky"
- Attention is not support: the site makes no election predictions and says so

## Data sources

| Source | What | Notes |
|---|---|---|
| GDELT DOC 2.0 | news article volume + tone, 28d | free, no key, ~1 request/45s to be safe |
| Wikimedia Pageviews | article views, 14d | free, no key |
| Bluesky public appview | followers, posts, engagement | free, no key, verified accounts only |

## Powered by Juicer

Want the actual posts, not just the numbers? [Juicer](https://www.juicer.io) aggregates a
politician's Instagram, Facebook, X, TikTok, YouTube, Reddit and Bluesky into one live feed
you can embed on any website. Senators, parliaments, city governments and campaigns already use it.
API: https://developers.juicer.io
