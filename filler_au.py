#!/usr/bin/env python3
import json, time, urllib.request, urllib.parse
UA = {"User-Agent": "juicer-politics-pulse/0.1 (research; juicer.io; contact pawel@juicer.io)"}
PATH = __file__.rsplit('/', 1)[0] + "/data/data_au.json"
def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25))
for rnd in range(6):
    d = json.load(open(PATH))
    missing = [p for p in d["people"] if p.get("wiki_14d") is None]
    if not missing:
        print("all filled"); break
    print(f"round {rnd}: {len(missing)} missing", flush=True)
    for p in missing:
        time.sleep(10)
        try:
            wv = get(f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{urllib.parse.quote(p['wiki'])}/daily/2026080300/2026081600")
            days = [(x["timestamp"][:8], x["views"]) for x in wv["items"]]
            p["wiki_daily"] = days; p["wiki_14d"] = sum(v for _, v in days)
            p["wiki_last7"] = sum(v for _, v in days[-7:]); p["wiki_prev7"] = sum(v for _, v in days[:-7][-7:])
            p.pop("wiki_error", None)
            json.dump(d, open(PATH, "w"), indent=1)
        except Exception as e:
            if "404" in str(e):
                p["wiki_error"] = "no article"; json.dump(d, open(PATH, "w"), indent=1)
    time.sleep(120)
print("done")
