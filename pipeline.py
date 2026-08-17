#!/usr/bin/env python3
"""Political Pulse data pipeline. Public keyless sources only:
GDELT (news volume + tone), Wikipedia pageviews (attention),
Bluesky appview (verified accounts only). Emits data/data.json."""
import json, time, urllib.request, urllib.parse
from datetime import date, timedelta

UA = {"User-Agent": "juicer-politics-pulse/0.1 (research; juicer.io)"}
def get(url):
    req = urllib.request.Request(url, headers=UA)
    return json.load(urllib.request.urlopen(req, timeout=25))

PEOPLE = json.load(open(__file__.rsplit('/', 1)[0] + "/people.json"))

end = date(2026, 8, 16); start = end - timedelta(days=13)
out = {"generated_at": "2026-08-17", "window": {"news_days": 28, "wiki_days": 14}, "people": []}

for p in PEOPLE:
    rec = dict(p)
    q = urllib.parse.quote(p["gdelt"])
    try:
        vol = get(f"https://api.gdeltproject.org/api/v2/doc/doc?query={q}&mode=timelinevolraw&timespan=4w&format=json")
        series = vol["timeline"][0]["data"]
        rec["news_articles_28d"] = sum(x["value"] for x in series)
        rec["news_last7"] = sum(x["value"] for x in series[-7:])
        rec["news_prev7"] = sum(x["value"] for x in series[-14:-7])
    except Exception as e:
        rec["news_error"] = str(e)[:60]
    time.sleep(6)
    try:
        tone = get(f"https://api.gdeltproject.org/api/v2/doc/doc?query={q}&mode=timelinetone&timespan=4w&format=json")
        tdata = tone["timeline"][0]["data"]
        rec["news_tone_avg"] = round(sum(x["value"] for x in tdata) / max(len(tdata), 1), 2)
    except Exception as e:
        rec["tone_error"] = str(e)[:60]
    time.sleep(6)
    try:
        wv = get(f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{urllib.parse.quote(p['wiki'])}/daily/{start:%Y%m%d}00/{end:%Y%m%d}00")
        days = [(i["timestamp"][:8], i["views"]) for i in wv["items"]]
        rec["wiki_daily"] = days
        rec["wiki_14d"] = sum(v for _, v in days)
        rec["wiki_last7"] = sum(v for _, v in days[-7:])
        rec["wiki_prev7"] = sum(v for _, v in days[:-7][-7:])
    except Exception as e:
        rec["wiki_error"] = str(e)[:60]
    if p["bsky"]:
        try:
            prof = get(f"https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor={p['bsky']}")
            rec["bsky_followers"] = prof.get("followersCount")
            feed = get(f"https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor={p['bsky']}&limit=30&filter=posts_no_replies")
            posts = [f["post"] for f in feed.get("feed", []) if f["post"]["author"]["handle"] == p["bsky"]]
            if posts:
                rec["bsky_avg_likes"] = round(sum(x.get("likeCount", 0) for x in posts) / len(posts))
                rec["bsky_avg_reposts"] = round(sum(x.get("repostCount", 0) for x in posts) / len(posts))
                top = sorted(posts, key=lambda x: -x.get("likeCount", 0))[:3]
                rec["bsky_top_posts"] = [
                    {"text": t["record"].get("text", "")[:280], "likes": t.get("likeCount", 0),
                     "reposts": t.get("repostCount", 0), "date": t["record"].get("createdAt", "")[:10]} for t in top]
        except Exception as e:
            rec["bsky_error"] = str(e)[:60]
    out["people"].append(rec)
    print(f"done: {p['name']}  news28d={rec.get('news_articles_28d')} tone={rec.get('news_tone_avg')} wiki14d={rec.get('wiki_14d')} bskyF={rec.get('bsky_followers')}")

with open(__file__.rsplit('/', 1)[0] + "/data/data.json", "w") as f:
    json.dump(out, f, indent=1)
print("written data/data.json")
