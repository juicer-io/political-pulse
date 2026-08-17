#!/usr/bin/env python3
import json, time, urllib.request, urllib.parse
UA = {"User-Agent": "juicer-politics-pulse/0.1 (research; juicer.io)"}
PATH = __file__.rsplit('/', 1)[0] + "/data/data.json"
def get(url):
    req = urllib.request.Request(url, headers=UA)
    return json.loads(urllib.request.urlopen(req, timeout=30).read().decode())

for round_ in range(12):
    d = json.load(open(PATH))
    missing = [(p, m) for p in d["people"] for m, k in
               [("timelinevolraw", "news_articles_28d"), ("timelinetone", "news_tone_avg")] if p.get(k) is None]
    if not missing:
        print("all filled"); break
    for p, mode in missing:
        time.sleep(45)
        try:
            r = get(f"https://api.gdeltproject.org/api/v2/doc/doc?query={urllib.parse.quote(p['gdelt'])}&mode={mode}&timespan=4w&format=json")
            data = r["timeline"][0]["data"]
            if mode == "timelinevolraw":
                p["news_articles_28d"] = sum(x["value"] for x in data)
                p["news_last7"] = sum(x["value"] for x in data[-7:])
                p["news_prev7"] = sum(x["value"] for x in data[-14:-7])
            else:
                p["news_tone_avg"] = round(sum(x["value"] for x in data) / max(len(data), 1), 2)
            json.dump(d, open(PATH, "w"), indent=1)
            print(f"filled {p['name']} {mode}", flush=True)
        except Exception as e:
            print(f"retry-later {p['name']} {mode}: {str(e)[:40]}", flush=True)
print("filler done")
