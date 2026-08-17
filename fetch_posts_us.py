#!/usr/bin/env python3
"""Recent posts for members' social walls: X via Juicer Data API, Bluesky via
public appview. Senate pilot scope (pass --house to extend later).
Writes data/posts_us.json {slug: [{platform, text, likes, comments, shares,
date, url}]}, up to 10 newest per member across both platforms."""
import json, sys, time, urllib.request, urllib.parse
from pathlib import Path
ROOT = Path(__file__).resolve().parent
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in open(Path.home() / "juicer/.env.api")
           if l.startswith("JUICER_API_KEY="))
UA = {"User-Agent": "juicer-politics-pulse/0.1 (research; juicer.io)"}
def get(url, auth=False):
    h = dict(UA)
    if auth: h["Authorization"] = f"Bearer {KEY}"
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=60))

people = json.load(open(ROOT / "people_us_full.json"))
social = json.load(open(ROOT / "data/social_us.json"))
bsky = json.load(open(ROOT / "data/bsky_us.json"))
scope = [p for p in people if p["chamber"] == "Senate" or "--house" in sys.argv]
PATH = ROOT / "data/posts_us.json"
out = json.load(open(PATH)) if PATH.exists() else {}
calls = 0
for p in scope:
    if p["slug"] in out: continue
    posts = []
    tw = social.get(p["bioguide"], {}).get("twitter")
    if tw:
        try:
            r = get("https://api.juicer.io/v1/data/posts?platforms=Twitter&term=" + urllib.parse.quote(tw), auth=True)
            calls += 1
            for it in (r.get("data") or [])[:10]:
                posts.append({"platform": "X", "text": (it.get("message") or "")[:300],
                              "likes": it.get("like_count"), "comments": it.get("comment_count"),
                              "shares": it.get("share_count"), "date": (it.get("post_created_at") or "")[:10],
                              "url": it.get("url") or it.get("external_url") or f"https://x.com/{tw}"})
        except Exception as e:
            print(f"X fail {p['name']}: {str(e)[:40]}", flush=True)
    bh = (bsky.get(p["slug"]) or {}).get("handle") if isinstance(bsky.get(p["slug"]), dict) else None
    if bh:
        try:
            r = get(f"https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor={bh}&limit=10&filter=posts_no_replies")
            for f in r.get("feed", []):
                po = f["post"]
                if po["author"]["handle"] != bh: continue
                rkey = po["uri"].rsplit("/", 1)[-1]
                posts.append({"platform": "Bluesky", "text": po["record"].get("text", "")[:300],
                              "likes": po.get("likeCount"), "comments": po.get("replyCount"),
                              "shares": po.get("repostCount"), "date": po["record"].get("createdAt", "")[:10],
                              "url": f"https://bsky.app/profile/{bh}/post/{rkey}"})
        except Exception as e:
            print(f"bsky fail {p['name']}: {str(e)[:40]}", flush=True)
    posts.sort(key=lambda x: x["date"], reverse=True)
    out[p["slug"]] = posts[:10]
    json.dump(out, open(PATH, "w"), indent=1)
    time.sleep(1.2)
walls = sum(1 for v in out.values() if v)
print(f"DONE: {walls} members with posts, {calls} Juicer API calls this run")
