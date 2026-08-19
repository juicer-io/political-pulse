#!/usr/bin/env python3
"""Australian Parliament X walls via a dedicated Juicer feed, same rotation
pattern as the US script. Handles come from Wikidata (data/social_au.json).
Writes data/posts_au.json. Ends by emptying the feed (cost rule)."""
import html, json, re, sys, time, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BATCH = 50
HARVEST_PASSES = 6
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in open(Path.home() / "juicer/.env.api")
           if l.startswith("JUICER_API_KEY="))

def req(method, path, body=None, retries=3):
    last = None
    for attempt in range(retries):
        try:
            r = urllib.request.Request("https://api.juicer.io" + path, method=method,
                                       headers={"Authorization": f"Bearer {KEY}",
                                                "Content-Type": "application/json"},
                                       data=json.dumps(body).encode() if body else None)
            return json.load(urllib.request.urlopen(r, timeout=60))
        except Exception as e:
            last = e
            time.sleep(5 * (attempt + 1))
    raise last

FEED_FILE = ROOT / ".feed_au_id"
if FEED_FILE.exists():
    FEED = int(FEED_FILE.read_text().strip())
else:
    FEED = req("POST", "/v1/feeds", {"name": "political-pulse-x-au"})["data"]["id"]
    FEED_FILE.write_text(str(FEED))
print("AU feed:", FEED, flush=True)

people = json.load(open(ROOT / "people_au.json"))
social = json.load(open(ROOT / "data/social_au.json"))
POSTS_PATH = ROOT / "data/posts_au.json"
if not POSTS_PATH.exists():
    POSTS_PATH.write_text("{}")
slug_by_handle = {}
for p in people:
    tw = social.get(p["slug"], {}).get("twitter")
    if tw:
        slug_by_handle[tw.lower()] = p["slug"]

def harvest():
    posts_db = json.load(open(POSTS_PATH))
    by_handle = {}
    page = 1
    while page <= 40:
        d = req("GET", f"/v1/feeds/{FEED}/posts?per=100&page={page}")
        batch = d.get("data") or []
        if not batch:
            break
        for po in batch:
            h = (po.get("poster") or {}).get("name", "").lower()
            if h not in slug_by_handle:
                continue
            text = html.unescape(re.sub(r"<[^>]+>", "", po.get("message") or ""))
            by_handle.setdefault(h, []).append({
                "platform": "X", "text": text[:300],
                "likes": po.get("like_count"), "comments": po.get("comment_count"),
                "shares": po.get("share_count"),
                "date": (po.get("external_created_at") or "")[:10],
                "url": po.get("url") or f"https://x.com/{h}"})
        page += 1
    fresh = 0
    for h, plist in by_handle.items():
        plist.sort(key=lambda x: x["date"], reverse=True)
        slug = slug_by_handle[h]
        if not posts_db.get(slug):
            fresh += 1
        posts_db[slug] = plist[:10]
    json.dump(posts_db, open(POSTS_PATH, "w"), indent=1)
    return fresh

def current_sources():
    out, page = [], 1
    while page <= 5:
        d = req("GET", f"/v1/feeds/{FEED}/sources?per=100&page={page}")
        b = d.get("data") or []
        if not b:
            break
        out += b
        page += 1
    return out

def rotate():
    posts_db0 = json.load(open(POSTS_PATH))
    queue = [p for p in people if social.get(p["slug"], {}).get("twitter")]
    queue.sort(key=lambda p: (bool(posts_db0.get(p["slug"])), -(p.get("wiki_14d") or 0)))
    done = set()
    while True:
        remaining = [p for p in queue if p["slug"] not in done]
        if not remaining:
            print("AU cycle complete", flush=True)
            break
        batch = [(p, social[p["slug"]]["twitter"]) for p in remaining[:BATCH]]
        done.update(p["slug"] for p, _ in batch)
        print(f"AU rotating: {len(remaining)} to process, batch {len(batch)}", flush=True)
        for s in current_sources():
            try: req("DELETE", f"/v1/feeds/{FEED}/sources/{s['id']}")
            except Exception: pass
            time.sleep(0.4)
        added = 0
        for p, tw in batch:
            try:
                req("POST", f"/v1/feeds/{FEED}/sources",
                    {"platform": "Twitter", "term": tw, "term_type": "username"}, retries=2)
                added += 1
            except Exception as e:
                print(f"add fail {tw}: {str(e)[:40]}", flush=True)
            time.sleep(1.0)
        print(f"AU batch added: {added}", flush=True)
        for i in range(HARVEST_PASSES):
            time.sleep(40)
            print(f"  AU pass {i+1}: +{harvest()}", flush=True)
    for s in current_sources():
        try: req("DELETE", f"/v1/feeds/{FEED}/sources/{s['id']}")
        except Exception: pass
        time.sleep(0.4)
    print("AU feed emptied", flush=True)

if __name__ == "__main__":
    if "--rotate" in sys.argv:
        rotate()
    else:
        print("harvested:", harvest())
