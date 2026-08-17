#!/usr/bin/env python3
"""X follower counts for the full US + AU rosters via the Juicer Data API.

Reads JUICER_API_KEY from ~/juicer/.env.api. Batches 5 handles per call,
keeps exact matches only, saves incrementally to data/x_followers.json
(the site generator flips the X column to numbers when this file has data)."""
import json, time, urllib.request, urllib.parse
from pathlib import Path
ROOT = Path(__file__).resolve().parent
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in open(Path.home() / "juicer/.env.api")
           if l.startswith("JUICER_API_KEY="))
handles = set()
for f in ("social_us.json", "social_au.json"):
    try:
        handles |= {v["twitter"] for v in json.load(open(ROOT / "data" / f)).values() if v.get("twitter")}
    except FileNotFoundError:
        pass
handles = sorted(handles)
PATH = ROOT / "data/x_followers.json"
out = json.load(open(PATH)) if PATH.exists() else {"as_of": None, "source": "Juicer Data API", "followers": {}}
todo = [h for h in handles if h not in out["followers"]]
print(f"{len(todo)} handles, ~{(len(todo)+4)//5} calls")
for i in range(0, len(todo), 5):
    batch = todo[i:i+5]
    url = ("https://api.juicer.io/v1/data/profiles?platforms=Twitter&term=" +
           urllib.parse.quote(",".join(batch)))
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {KEY}"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=60))
        for t in r.get("data", []):
            prof = (t.get("profiles") or [{}])[0]
            fc = prof.get("metrics", {}).get("follower_count")
            if t.get("exact_match") and fc is not None:
                out["followers"][t["term"]] = fc
            else:
                out["followers"][t["term"]] = None  # mark tried, no exact profile
        out["as_of"] = time.strftime("%Y-%m-%d")
        json.dump(out, open(PATH, "w"), indent=1)
    except Exception as e:
        print(f"batch {i}: {str(e)[:60]} (will retry on next run)", flush=True)
    if i % 50 == 0:
        got = sum(1 for v in out['followers'].values() if v)
        print(f"{i+len(batch)}/{len(todo)} processed, {got} with counts", flush=True)
    time.sleep(1.5)
got = sum(1 for v in out["followers"].values() if v)
print(f"DONE: {got} follower counts of {len(handles)} handles")
