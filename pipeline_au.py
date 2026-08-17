#!/usr/bin/env python3
"""Australia board data: Wikipedia pageviews + verified Bluesky for all 229 members."""
import json, time, urllib.request, urllib.parse
UA = {"User-Agent": "juicer-politics-pulse/0.1 (research; juicer.io)"}
ROOT = __file__.rsplit('/', 1)[0]
def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25))

people = json.load(open(ROOT + "/people_au.json"))
out = {"generated_at": "2026-08-17", "people": []}
for i, p in enumerate(people):
    try:
        wv = get(f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{urllib.parse.quote(p['wiki'])}/daily/2026080400/2026081700")
        days = [(x["timestamp"][:8], x["views"]) for x in wv["items"]]
        p["wiki_daily"] = days
        p["wiki_14d"] = sum(v for _, v in days)
        p["wiki_last7"] = sum(v for _, v in days[-7:])
        p["wiki_prev7"] = sum(v for _, v in days[:-7][-7:])
    except Exception:
        p["wiki_14d"] = None
    try:
        r = get("https://public.api.bsky.app/xrpc/app.bsky.actor.searchActors?limit=5&q=" + urllib.parse.quote(p["name"]))
        first, last = p["name"].split()[0].lower(), p["name"].split()[-1].lower()
        for a in r.get("actors", []):
            dn = (a.get("displayName") or "").lower()
            if a.get("verification", {}).get("verifiedStatus") == "valid" and first in dn and last in dn:
                p["bsky"] = a["handle"]
                prof = get("https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor=" + a["handle"])
                p["bsky_followers"] = prof.get("followersCount")
                break
    except Exception:
        pass
    out["people"].append(p)
    if i % 25 == 0: print(f"{i}/{len(people)}", flush=True)
    time.sleep(0.12)
json.dump(out, open(ROOT + "/data/data_au.json", "w"), indent=1)
top = sorted(out["people"], key=lambda x: -(x.get("wiki_14d") or 0))[:8]
print("TOP:", [(t["name"], t["party"], t.get("wiki_14d")) for t in top])
print("bsky verified:", sum(1 for x in out["people"] if x.get("bsky")))
clients = [x for x in out["people"] if x["name"] in ("Sarah Henderson", "Tim Wilson", "Ben Small", "Tom Venning")]
print("clients:", [(c["name"], c.get("wiki_14d"), c.get("bsky")) for c in clients])
