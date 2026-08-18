#!/usr/bin/env python3
"""Re-adds sources for pilot members still without walls (fresh sync puts
their posts in the feed's recent window), then runs repeated harvests."""
import json, subprocess, time, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parent
FEED = 457678
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in open(Path.home() / "juicer/.env.api")
           if l.startswith("JUICER_API_KEY="))
def req(method, path, body=None):
    r = urllib.request.Request("https://api.juicer.io" + path, method=method,
                               headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
                               data=json.dumps(body).encode() if body else None)
    return json.load(urllib.request.urlopen(r, timeout=60))

people = json.load(open(ROOT / "people_us_full.json"))
social = json.load(open(ROOT / "data/social_us.json"))
srcmap = json.load(open(ROOT / "data/x_sources.json"))
posts_db = json.load(open(ROOT / "data/posts_us.json"))
slug_by_handle = {}
for p in people:
    tw = social.get(p["bioguide"], {}).get("twitter")
    if tw: slug_by_handle[tw] = p["slug"]
stragglers = [h for h in srcmap if not posts_db.get(slug_by_handle.get(h, ""))]
# ensure the manually-created RepMaxMiller source pair is covered via its dataset handle
print("stragglers:", len(stragglers), stragglers[:8], flush=True)
for h in stragglers:
    try:
        req("DELETE", f"/v1/feeds/{FEED}/sources/{srcmap[h]}")
    except Exception:
        pass
    for attempt in range(3):
        try:
            r = req("POST", f"/v1/feeds/{FEED}/sources", {"platform": "Twitter", "term": h, "term_type": "username"})
            srcmap[h] = r["data"]["id"]
            json.dump(srcmap, open(ROOT / "data/x_sources.json", "w"), indent=1)
            break
        except Exception as e:
            if attempt == 2: print(f"re-add fail {h}: {str(e)[:40]}", flush=True)
            time.sleep(4)
    time.sleep(1.5)
print("re-added; harvesting over 6 passes", flush=True)
for i in range(6):
    time.sleep(45)
    subprocess.run(["python3", str(ROOT / "fetch_posts_x_feed.py")], capture_output=True)
    posts_db = json.load(open(ROOT / "data/posts_us.json"))
    left = [h for h in stragglers if not posts_db.get(slug_by_handle.get(h, ""))]
    print(f"pass {i+1}: {len(stragglers) - len(left)}/{len(stragglers)} recovered", flush=True)
    if not left: break
print("done")
