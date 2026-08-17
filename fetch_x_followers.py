#!/usr/bin/env python3
"""Fetches live X follower counts for the whole roster via the official X API.

Needs X_BEARER_TOKEN in the environment (create an app at developer.x.com;
Basic tier covers this easily, Free tier works in daily portions).
Whole Congress = 6 batched requests (100 usernames per request).
Writes data/x_followers.json; resumable, honors 429s.
"""
import json, os, time, urllib.request, urllib.parse
ROOT = __file__.rsplit('/', 1)[0]
TOKEN = os.environ.get("X_BEARER_TOKEN")
if not TOKEN:
    raise SystemExit("X_BEARER_TOKEN not set. Create an app at developer.x.com, then: "
                     "X_BEARER_TOKEN=... python3 fetch_x_followers.py")
social = json.load(open(ROOT + "/data/social_us.json"))
handles = sorted({v["twitter"] for v in social.values() if v.get("twitter")})
PATH = ROOT + "/data/x_followers.json"
try: out = json.load(open(PATH))
except FileNotFoundError: out = {"as_of": None, "followers": {}}
todo = [h for h in handles if h not in out["followers"]]
print(f"{len(todo)} handles to fetch in {(len(todo)+99)//100} requests")
for i in range(0, len(todo), 100):
    batch = todo[i:i+100]
    url = ("https://api.twitter.com/2/users/by?user.fields=public_metrics&usernames=" +
           urllib.parse.quote(",".join(batch)))
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOKEN}"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=30))
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print("rate limited; run again later (progress is saved)"); break
        raise
    for u in r.get("data", []):
        out["followers"][u["username"]] = u["public_metrics"]["followers_count"]
    out["as_of"] = time.strftime("%Y-%m-%d")
    json.dump(out, open(PATH, "w"), indent=1)
    print(f"saved {len(out['followers'])} counts")
    time.sleep(2)
print("done; as of", out["as_of"])
