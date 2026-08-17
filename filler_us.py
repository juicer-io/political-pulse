#!/usr/bin/env python3
"""Adaptive Wikipedia pageviews filler: US full congress, then finishes AU."""
import json, time, urllib.request, urllib.parse
UA = {"User-Agent": "juicer-politics-pulse/0.1 (research; juicer.io; contact pawel@juicer.io)"}
ROOT = __file__.rsplit('/', 1)[0]
def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25))
def fill(path, people_key=None, seed=None):
    try: d = json.load(open(path))
    except FileNotFoundError: d = {"generated_at": "2026-08-17", "people": json.load(open(seed))}
    delay = 4.0
    for p in d["people"]:
        if p.get("wiki_14d") is not None or p.get("wiki_error") == "no article": continue
        while True:
            time.sleep(delay)
            try:
                wv = get(f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{urllib.parse.quote(p['wiki'])}/daily/2026080300/2026081600")
                days = [(x["timestamp"][:8], x["views"]) for x in wv["items"]]
                p["wiki_daily"] = days; p["wiki_14d"] = sum(v for _, v in days)
                p["wiki_last7"] = sum(v for _, v in days[-7:]); p["wiki_prev7"] = sum(v for _, v in days[:-7][-7:])
                p.pop("wiki_error", None)
                delay = max(3.0, delay * 0.9)
                break
            except Exception as e:
                if "404" in str(e): p["wiki_error"] = "no article"; break
                delay = min(60, delay * 2); print(f"backoff {delay:.0f}s at {p['name']}", flush=True)
        json.dump(d, open(path, "w"), indent=1)
    done = sum(1 for p in d["people"] if p.get("wiki_14d") is not None)
    print(f"{path}: {done}/{len(d['people'])} filled", flush=True)
fill(ROOT + "/data/data_us_full.json", seed=ROOT + "/people_us_full.json")
fill(ROOT + "/data/data_au.json")
print("ALL DONE")
