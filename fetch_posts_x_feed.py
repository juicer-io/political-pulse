#!/usr/bin/env python3
"""X-only post walls via a real Juicer feed (id 457678).

The account's source limit allows ~75 concurrent sources and the feed posts
endpoint serves a small recent-sync window, so this works in ROTATING BATCHES:
delete the previous batch's sources, add the next ~55 members, harvest the
window over several passes, repeat until every member with an X handle has a
wall. Walls merge into data/posts_us.json (X posts only, newest 10).

Run plain for a single harvest pass of whatever is in the feed.
Run with --rotate to work through all wall-less members (long; background it).
"""
import html
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FEED = 457678
BATCH = 55
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


people = json.load(open(ROOT / "people_us_full.json"))
social = json.load(open(ROOT / "data/social_us.json"))
POSTS_PATH = ROOT / "data/posts_us.json"
slug_by_handle = {}
for p in people:
    tw = social.get(p["bioguide"], {}).get("twitter")
    if tw:
        slug_by_handle[tw.lower()] = p["slug"]


def harvest():
    """One pass over the feed's visible post window; merge X posts per member."""
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
    while True:
        posts_db = json.load(open(POSTS_PATH))
        wallless = [p for p in people if not posts_db.get(p["slug"])
                    and social.get(p["bioguide"], {}).get("twitter")]
        wallless.sort(key=lambda x: -(x.get("wiki_14d") or 0))
        if not wallless:
            print("all members with X handles have walls", flush=True)
            break
        batch = [(p, social[p["bioguide"]]["twitter"]) for p in wallless[:BATCH]]
        print(f"rotating: {len(wallless)} wall-less remain, next batch {len(batch)}", flush=True)
        for s in current_sources():
            try:
                req("DELETE", f"/v1/feeds/{FEED}/sources/{s['id']}")
            except Exception:
                pass
            time.sleep(0.4)
        added = 0
        for p, tw in batch:
            for attempt in range(3):
                try:
                    req("POST", f"/v1/feeds/{FEED}/sources",
                        {"platform": "Twitter", "term": tw, "term_type": "username"})
                    added += 1
                    break
                except Exception as e:
                    if attempt == 2:
                        print(f"add fail {tw}: {str(e)[:40]}", flush=True)
                    time.sleep(4)
            time.sleep(1.0)
        print(f"batch added: {added}", flush=True)
        recovered_total = 0
        for i in range(HARVEST_PASSES):
            time.sleep(40)
            recovered_total += harvest()
            print(f"  pass {i+1}: {recovered_total} new walls this batch", flush=True)
        if recovered_total == 0:
            print("batch yielded nothing; stopping to avoid a spin loop", flush=True)
            break
    # cost control: empty the feed so no sources sync between 14-day refreshes
    for s in current_sources():
        try:
            req("DELETE", f"/v1/feeds/{FEED}/sources/{s['id']}")
        except Exception:
            pass
        time.sleep(0.4)
    print("feed emptied: zero sources syncing until next refresh", flush=True)


if __name__ == "__main__":
    if "--rotate" in sys.argv:
        rotate()
    else:
        print(f"harvested, {harvest()} new walls")
