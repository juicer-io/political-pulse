#!/usr/bin/env python3
"""X walls via a real Juicer feed (workaround for D-1236).
Adds X sources for wall-less members to feed 457678, then harvests posts
per member from the feed. Run with --add to (re)create sources; plain run
just harvests. Merges into data/posts_us.json."""
import html, json, re, sys, time, urllib.request, urllib.parse
from pathlib import Path
ROOT = Path(__file__).resolve().parent
FEED = 457678
COHORT = 120
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in open(Path.home() / "juicer/.env.api")
           if l.startswith("JUICER_API_KEY="))
def req(method, path, body=None):
    r = urllib.request.Request("https://api.juicer.io" + path, method=method,
                               headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
                               data=json.dumps(body).encode() if body else None)
    return json.load(urllib.request.urlopen(r, timeout=60))

people = json.load(open(ROOT / "people_us_full.json"))
social = json.load(open(ROOT / "data/social_us.json"))
posts_db = json.load(open(ROOT / "data/posts_us.json"))
wallless = [p for p in people if not posts_db.get(p["slug"])]
wallless.sort(key=lambda x: -(x.get("wiki_14d") or 0))
cohort = [(p, social.get(p["bioguide"], {}).get("twitter")) for p in wallless]
cohort = [(p, tw) for p, tw in cohort if tw][:COHORT]
handle2slug = {tw.lower(): p["slug"] for p, tw in cohort}

MAP_PATH = ROOT / "data/x_sources.json"
srcmap = json.load(open(MAP_PATH)) if MAP_PATH.exists() else {}
if "--add" in sys.argv:
    for p, tw in cohort:
        if tw in srcmap: continue
        for attempt in range(3):
            try:
                r = req("POST", f"/v1/feeds/{FEED}/sources",
                        {"platform": "Twitter", "term": tw, "term_type": "username"})
                srcmap[tw] = r["data"]["id"]
                json.dump(srcmap, open(MAP_PATH, "w"), indent=1)
                break
            except Exception as e:
                if attempt == 2: print(f"source fail {tw}: {str(e)[:50]}", flush=True)
                time.sleep(4)
        time.sleep(1.0)
    print(f"sources registered: {len(srcmap)}", flush=True)

# harvest: page through feed posts, bucket by poster handle
by_handle = {}
page = 1
while page <= 40:
    d = req("GET", f"/v1/feeds/{FEED}/posts?per=100&page={page}")
    batch = d.get("data") or []
    if not batch: break
    for po in batch:
        h = (po.get("poster") or {}).get("name", "").lower()
        if h not in handle2slug: continue
        text = html.unescape(re.sub(r"<[^>]+>", "", po.get("message") or ""))
        by_handle.setdefault(h, []).append({
            "platform": "X", "text": text[:300],
            "likes": po.get("like_count"), "comments": po.get("comment_count"),
            "shares": po.get("share_count"),
            "date": (po.get("external_created_at") or "")[:10],
            "url": po.get("url") or f"https://x.com/{h}"})
    page += 1
merged = 0
for h, plist in by_handle.items():
    plist.sort(key=lambda x: x["date"], reverse=True)
    slug = handle2slug[h]
    if not posts_db.get(slug):
        posts_db[slug] = plist[:10]
        merged += 1
json.dump(posts_db, open(ROOT / "data/posts_us.json", "w"), indent=1)
print(f"harvested walls for {merged} members ({len(by_handle)} handles had posts)")
