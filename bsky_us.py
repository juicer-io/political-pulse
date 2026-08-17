#!/usr/bin/env python3
"""Verified-only Bluesky resolution for the full US congress roster."""
import json, time, urllib.request, urllib.parse
UA = {"User-Agent": "juicer-politics-pulse/0.1 (research; juicer.io)"}
ROOT = __file__.rsplit('/', 1)[0]
def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20))
PATH = ROOT + "/data/bsky_us.json"
try: found = json.load(open(PATH))
except FileNotFoundError: found = {}
people = json.load(open(ROOT + "/people_us_full.json"))
for i, p in enumerate(people):
    if p["slug"] in found: continue
    try:
        r = get("https://public.api.bsky.app/xrpc/app.bsky.actor.searchActors?limit=5&q=" + urllib.parse.quote(p["name"]))
        first, last = p["name"].split()[0].lower(), p["name"].split()[-1].lower()
        hit = None
        for a in r.get("actors", []):
            dn = (a.get("displayName") or "").lower()
            if a.get("verification", {}).get("verifiedStatus") == "valid" and first in dn and last in dn:
                prof = get("https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor=" + a["handle"])
                hit = {"handle": a["handle"], "followers": prof.get("followersCount")}
                break
        found[p["slug"]] = hit
    except Exception:
        pass
    if i % 50 == 0:
        json.dump(found, open(PATH, "w")); print(f"{i}/536 verified so far: {sum(1 for v in found.values() if v)}", flush=True)
    time.sleep(0.25)
json.dump(found, open(PATH, "w"))
print("done. verified accounts:", sum(1 for v in found.values() if v))
