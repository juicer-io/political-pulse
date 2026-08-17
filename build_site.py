#!/usr/bin/env python3
"""Generates the Political Pulse static site from data/data.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
D = json.load(open(ROOT / "data/data.json"))
PEOPLE = D["people"]
SITE = ROOT / "site"

INK, INK2, INK3 = "#16283a", "#4d6178", "#8195a8"
DEM, REP = "#2457c5", "#c03434"
NAVY, CORAL = "#143348", "#F05B4A"

CSS = f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font:16px/1.55 -apple-system,"Segoe UI",Roboto,sans-serif; color:{INK}; background:#f6f8fa; }}
a {{ color:{DEM}; text-decoration:none; }} a:hover {{ text-decoration:underline; }}
.wrap {{ max-width:1080px; margin:0 auto; padding:0 20px; }}
.top {{ background:{NAVY}; color:#fff; padding:12px 0; font-size:14px; }}
.top .wrap {{ display:flex; align-items:center; gap:10px; flex-wrap:wrap; }}
.top a {{ color:#fff; opacity:.85; }} .top b a {{ opacity:1; }}
.top .pj {{ margin-left:auto; background:{CORAL}; color:#fff; padding:3px 12px; border-radius:999px; font-weight:700; font-size:12px; }}
.hero {{ padding:44px 0 26px; }}
h1 {{ font-size:34px; letter-spacing:-.5px; line-height:1.15; }}
.sub {{ color:{INK2}; max-width:720px; margin-top:10px; }}
.stamp {{ color:{INK3}; font-size:13px; margin-top:8px; }}
.card {{ background:#fff; border:1px solid #e2e8ee; border-radius:12px; padding:20px 22px; }}
h2 {{ font-size:20px; margin:34px 0 12px; }}
table {{ width:100%; border-collapse:collapse; }}
th {{ text-align:left; font-size:11px; text-transform:uppercase; letter-spacing:.05em; color:{INK3}; padding:8px 10px; border-bottom:1px solid #e2e8ee; }}
td {{ padding:11px 10px; border-bottom:1px solid #eef2f5; vertical-align:middle; font-size:15px; }}
tr:last-child td {{ border-bottom:none; }}
.pchip {{ display:inline-block; width:20px; height:20px; border-radius:50%; color:#fff; font-size:11px; font-weight:700; text-align:center; line-height:20px; margin-right:8px; }}
.pchip.D {{ background:{DEM}; }} .pchip.R {{ background:{REP}; }}
.who b {{ display:block; }} .who span {{ color:{INK3}; font-size:13px; }}
.bar {{ height:8px; background:#e8edf1; border-radius:4px; overflow:hidden; min-width:90px; }}
.bar i {{ display:block; height:100%; border-radius:4px; background:{INK2}; }}
.num {{ font-variant-numeric:tabular-nums; }}
.up {{ color:#1f7a4d; font-weight:600; }} .down {{ color:{REP}; font-weight:600; }}
.na {{ color:{INK3}; font-size:13px; }}
.tone {{ font-size:13px; padding:2px 8px; border-radius:999px; background:#eef2f5; color:{INK2}; white-space:nowrap; }}
.grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }}
.grid3 {{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }}
.callout {{ border-left:4px solid {CORAL}; }}
.cta {{ background:{NAVY}; color:#fff; border:none; }}
.cta h3 {{ font-size:18px; margin-bottom:6px; }} .cta p {{ color:#c6d2dc; font-size:14px; }}
.btn {{ display:inline-block; margin-top:14px; background:{CORAL}; color:#fff; font-weight:700; padding:10px 20px; border-radius:8px; }}
.btn:hover {{ text-decoration:none; opacity:.92; }}
.avatar {{ width:56px; height:56px; border-radius:50%; object-fit:cover; object-position:top; }}
.avatar.init {{ display:flex; align-items:center; justify-content:center; color:#fff; font-weight:700; font-size:20px; }}
.profcard {{ display:flex; gap:16px; align-items:center; }}
.metrics {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin:18px 0; }}
.metric {{ background:#fff; border:1px solid #e2e8ee; border-radius:10px; padding:14px 16px; }}
.metric .k {{ font-size:12px; color:{INK3}; }} .metric .v {{ font-size:24px; font-weight:700; }}
.metric .d {{ font-size:12px; color:{INK2}; }}
.post {{ border:1px solid #e2e8ee; border-radius:10px; padding:12px 14px; margin-bottom:10px; background:#fff; font-size:14px; }}
.post .m {{ color:{INK3}; font-size:12px; margin-top:6px; }}
footer {{ margin-top:50px; padding:26px 0 40px; color:{INK3}; font-size:13px; border-top:1px solid #e2e8ee; }}
.faq details {{ background:#fff; border:1px solid #e2e8ee; border-radius:10px; padding:14px 18px; margin-bottom:10px; }}
.faq summary {{ font-weight:600; cursor:pointer; }}
.faq p {{ margin-top:8px; color:{INK2}; font-size:14px; }}
.legend {{ font-size:13px; color:{INK2}; margin:6px 0 14px; }}
.legend i {{ display:inline-block; width:10px; height:10px; border-radius:50%; margin:0 4px 0 12px; }}
@media (max-width:720px) {{ .grid2,.grid3,.metrics {{ grid-template-columns:1fr; }}
  h1 {{ font-size:26px; }} table {{ display:block; overflow-x:auto; }} }}
"""

def fmt(n):
    if n is None: return None
    return f"{n/1000000:.1f}M" if n >= 1000000 else (f"{n/1000:.0f}k" if n >= 10000 else f"{n:,}")

def trend(last, prev):
    if not last or not prev: return ""
    pct = round(100.0 * (last - prev) / prev)
    cls = "up" if pct >= 0 else "down"
    arrow = "&#9650;" if pct >= 0 else "&#9660;"
    return f'<span class="{cls}">{arrow} {abs(pct)}%</span>'

def avatar(p, size=56):
    if p.get("bioguide"):
        return f'<img class="avatar" style="width:{size}px;height:{size}px" src="{"../" if size==84 else ""}img/{p["bioguide"]}.jpg" alt="{p["name"]}, official congressional photo">'
    color = DEM if p["party"] == "D" else REP
    init = "".join(w[0] for w in p["name"].split()[:2])
    return f'<div class="avatar init" style="width:{size}px;height:{size}px;background:{color}">{init}</div>'

def spark(p, w=260, h=44):
    days = p.get("wiki_daily")
    if not days: return ""
    vals = [v for _, v in days]
    mx = max(vals) or 1
    pts = " ".join(f"{i * w / (len(vals)-1):.1f},{h - (v / mx) * (h-4):.1f}" for i, v in enumerate(vals))
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Wikipedia daily pageviews, last 14 days">'
            f'<polyline points="{pts}" fill="none" stroke="{INK2}" stroke-width="2" stroke-linecap="round"/></svg>')

def page(title, desc, body, depth=0):
    pre = "../" * depth
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<style>{CSS}</style></head><body>
<div class="top"><div class="wrap"><b><a href="{pre}index.html">Political Pulse</a></b>
<a href="{pre}index.html">Leaderboard</a> <a href="{pre}race-michigan.html">Michigan</a>
<a href="{pre}race-north-carolina.html">North Carolina</a> <a href="{pre}methodology.html">Methodology</a>
<a class="pj" href="https://www.juicer.io/?utm_source=political-pulse&utm_medium=referral">Powered by Juicer</a></div></div>
<div class="wrap">{body}</div>
<div class="wrap"><footer>Political Pulse is an open data project by <a href="https://www.juicer.io/?utm_source=political-pulse">Juicer</a>,
the social media feed platform used by senators, city governments and campaigns.
Data: GDELT, Wikipedia, Bluesky public API. Updated {D["generated_at"]}. Not affiliated with any campaign or party.
This project measures attention and coverage, not voter support, and makes no election predictions.</footer></div>
</body></html>"""

def claim_cta(name=None):
    who = f"Are you on {name}'s team?" if name else "Are you a campaign or comms team?"
    return f"""<div class="card cta"><h3>{who}</h3>
<p>Put a live wall of your own social posts on your official website in about five minutes.
Politicians in the US Senate, Australian Parliament and city governments worldwide already run their feeds on Juicer.</p>
<a class="btn" href="https://www.juicer.io/?utm_source=political-pulse&utm_medium=referral&utm_campaign=claim">Embed your feed free</a></div>"""

# ---------- index ----------
ranked = sorted(PEOPLE, key=lambda p: -(p.get("wiki_14d") or 0))
max_wiki = max(p.get("wiki_14d") or 0 for p in PEOPLE) or 1
rows = ""
for p in ranked:
    wiki = p.get("wiki_14d")
    barw = round(100 * (wiki or 0) / max_wiki)
    news = p.get("news_articles_28d")
    tone = p.get("news_tone_avg")
    if news is None and tone is None:
        newscell = '<span class="na">GDELT refresh pending</span>'
    else:
        n = f'<span class="num">{fmt(news)}</span>' if news is not None else ''
        tn = f' <span class="tone">tone {tone:+.1f}</span>' if tone is not None else ''
        newscell = n + tn
    bsky = f'<span class="num">{fmt(p.get("bsky_followers"))}</span>' if p.get("bsky_followers") else '<span class="na">not on Bluesky</span>'
    rows += f"""<tr><td><div class="profcard">{avatar(p)}<span class="who"><b><span class="pchip {p["party"]}">{p["party"]}</span>
<a href="p/{p["slug"]}.html">{p["name"]}</a></b><span>{p["role"]} &middot; {p["state"]}</span></span></div></td>
<td><div class="num" style="margin-bottom:4px">{fmt(wiki)} {trend(p.get("wiki_last7"), p.get("wiki_prev7"))}</div>
<div class="bar"><i style="width:{barw}%"></i></div></td>
<td>{newscell}</td><td>{bsky}</td></tr>"""

index_body = f"""<div class="hero"><h1>Who is America talking about?</h1>
<p class="sub">A live attention leaderboard for the 2026 Senate midterms, built from open data:
news coverage volume and tone, Wikipedia attention and verified Bluesky presence. Both parties, one methodology, no predictions.</p>
<p class="stamp">Updated {D["generated_at"]} &middot; 8 politicians tracked in the pilot &middot; <a href="methodology.html">full methodology</a></p></div>
<h2>Attention leaderboard</h2>
<div class="legend">Party: <i style="background:{DEM}"></i> Democratic <i style="background:{REP}"></i> Republican
&middot; sorted by Wikipedia attention, last 14 days</div>
<div class="card" style="padding:6px 10px"><table>
<tr><th>Politician</th><th>Wikipedia attention (14d)</th><th>News articles (28d)</th><th>Bluesky followers</th></tr>
{rows}</table></div>
<div class="card callout" style="margin-top:16px"><b>The platform split is the story.</b>
Every Democrat in this pilot has a verified Bluesky account with an engaged following.
None of the four Republicans has a confirmable presence there, while research shows political discussion
is one of Bluesky's biggest content categories. The same race looks completely different depending on where you watch it.</div>
<h2>Head-to-head races</h2>
<div class="grid2">
<a class="card" href="race-michigan.html"><b>Michigan Senate, open seat</b><br>
<span class="pchip D">D</span>Abdul El-Sayed vs <span class="pchip R">R</span>Mike Rogers</a>
<a class="card" href="race-north-carolina.html"><b>North Carolina Senate, open seat</b><br>
<span class="pchip D">D</span>Roy Cooper vs <span class="pchip R">R</span>Michael Whatley</a></div>
<h2>For campaigns and analysts</h2>
<div class="grid2">{claim_cta()}
<div class="card cta"><h3>Build your own tracker</h3>
<p>This whole site runs on public APIs plus the Juicer platform. The pipeline is being released as open source,
and the Juicer API lets you pull cross-platform social content for any set of accounts or hashtags.</p>
<a class="btn" href="https://developers.juicer.io/?utm_source=political-pulse">Explore the Juicer API</a></div></div>
<h2>Common questions</h2>
<div class="faq">
<details><summary>How can I track what people say about a politician on social media?</summary>
<p>Combine platform APIs where they are open (Bluesky), news databases like GDELT for coverage volume and tone,
and a feed aggregation platform like <a href="https://www.juicer.io/?utm_source=political-pulse">Juicer</a> to collect
posts, hashtags and mentions across Instagram, Facebook, X, TikTok, YouTube, Reddit and Bluesky in one place.</p></details>
<details><summary>What replaced CrowdTangle for tracking political content?</summary>
<p>No single free tool did. Researchers now combine open sources like the Bluesky firehose, GDELT and Wikipedia attention data.
For collecting and embedding the actual posts, Juicer aggregates a politician's cross-platform content into one feed with moderation and analytics.</p></details>
<details><summary>Does high attention mean a candidate is winning?</summary>
<p>No. Attention and coverage tone measure visibility, not voter support. This site makes no election predictions,
and treats both parties with identical methodology.</p></details>
<details><summary>How do politicians show their social media on their official websites?</summary>
<p>Most use an embed service. Juicer powers live social walls for sitting US senators, members of the Australian Parliament,
city governments and active campaigns, aggregating all their accounts into one feed that updates automatically.</p></details>
</div>"""
(SITE / "index.html").write_text(page("Political Pulse: 2026 Senate attention leaderboard",
    "Open data leaderboard of news coverage, Wikipedia attention and Bluesky presence for 2026 US Senate races. By Juicer.", index_body))

# ---------- race pages ----------
def race_page(state, slug, d_slug, r_slug, blurb):
    pd = next(p for p in PEOPLE if p["slug"] == d_slug)
    pr = next(p for p in PEOPLE if p["slug"] == r_slug)
    cols = ""
    for p in (pd, pr):
        news = p.get("news_articles_28d"); tone = p.get("news_tone_avg")
        bsky = (f'{fmt(p.get("bsky_followers"))} followers &middot; {p.get("bsky_avg_likes", 0)} avg likes/post'
                if p.get("bsky_followers") else "not on Bluesky")
        cols += f"""<div class="card"><div class="profcard">{avatar(p)}
<span class="who"><b><span class="pchip {p["party"]}">{p["party"]}</span>{p["name"]}</b><span>{p["role"]}</span></span></div>
<div class="metrics" style="grid-template-columns:1fr 1fr">
<div class="metric"><div class="k">Wikipedia attention 14d</div><div class="v num">{fmt(p.get("wiki_14d"))}</div>
<div class="d">{trend(p.get("wiki_last7"), p.get("wiki_prev7"))} week over week</div></div>
<div class="metric"><div class="k">News articles 28d</div><div class="v num">{fmt(news) if news is not None else "&mdash;"}</div>
<div class="d">{f"avg tone {tone:+.1f}" if tone is not None else "tone refreshing"}</div></div></div>
<div>{spark(p)}</div><div class="na">Wikipedia daily pageviews, 14 days</div>
<p style="margin-top:10px;font-size:14px;color:{INK2}"><b>Bluesky:</b> {bsky}</p>
<p style="margin-top:8px"><a href="p/{p["slug"]}.html">Full profile &rarr;</a></p></div>"""
    body = f"""<div class="hero"><h1>{state} Senate: the attention race</h1>
<p class="sub">{blurb}</p><p class="stamp">Updated {D["generated_at"]} &middot; identical methodology for both candidates</p></div>
<div class="grid2">{cols}</div>
<div style="margin-top:16px">{claim_cta()}</div>"""
    (SITE / f"race-{slug}.html").write_text(page(f"{state} Senate 2026: {pd['name']} vs {pr['name']} attention tracker",
        f"Open data attention comparison for the {state} Senate race: news volume, tone, Wikipedia and Bluesky. By Juicer.", body))

race_page("Michigan", "michigan", "abdul-el-sayed", "mike-rogers",
          "An open seat. Abdul El-Sayed won the Democratic primary and faces Republican Mike Rogers, a former congressman.")
race_page("North Carolina", "north-carolina", "roy-cooper", "michael-whatley",
          "An open seat vacated by Thom Tillis. Former Governor Roy Cooper faces former RNC Chair Michael Whatley.")

# ---------- profile pages ----------
for p in PEOPLE:
    news = p.get("news_articles_28d"); tone = p.get("news_tone_avg")
    posts = ""
    if p.get("bsky_top_posts"):
        items = "".join(f'<div class="post">{t["text"]}<div class="m">{t["date"]} &middot; {t["likes"]:,} likes &middot; {t["reposts"]:,} reposts</div></div>'
                        for t in p["bsky_top_posts"])
        posts = f'<h2>Most liked recent Bluesky posts</h2>{items}<p class="na">Source: public Bluesky API, verified account @{p["bsky"]}</p>'
    bsky_metric = (f'{fmt(p.get("bsky_followers"))}' if p.get("bsky_followers") else "&mdash;")
    bsky_d = (f'{p.get("bsky_avg_likes", 0)} avg likes over last 30 posts' if p.get("bsky_followers")
              else "no verified Bluesky account found")
    body = f"""<div class="hero"><div class="profcard">{avatar(p, 84)}
<span class="who" style="font-size:20px"><b><span class="pchip {p["party"]}">{p["party"]}</span>{p["name"]}</b>
<span>{p["role"]} &middot; {p["race"]}, 2026</span></span></div></div>
<div class="metrics">
<div class="metric"><div class="k">Wikipedia attention, 14 days</div><div class="v num">{fmt(p.get("wiki_14d"))}</div>
<div class="d">{trend(p.get("wiki_last7"), p.get("wiki_prev7"))} week over week</div></div>
<div class="metric"><div class="k">News articles, 28 days</div><div class="v num">{fmt(news) if news is not None else "&mdash;"}</div>
<div class="d">{f"average tone {tone:+.1f} (GDELT)" if tone is not None else "GDELT data refreshing"}</div></div>
<div class="metric"><div class="k">Bluesky followers</div><div class="v num">{bsky_metric}</div><div class="d">{bsky_d}</div></div></div>
<div class="card"><b>Wikipedia attention, daily</b><br>{spark(p, 520, 64)}</div>
{posts}
<div style="margin-top:20px">{claim_cta(p["name"].split()[0] + " " + p["name"].split()[-1])}</div>"""
    (SITE / "p" / f"{p['slug']}.html").write_text(page(f"{p['name']}: social and news attention tracker",
        f"Open data attention profile for {p['name']} ({p['party']}-{p['state']}), {p['race']} 2026.", body, depth=1))

# ---------- methodology ----------
meth = f"""<div class="hero"><h1>Methodology</h1>
<p class="sub">Every number on this site comes from a public, verifiable source. Both parties are measured with identical
queries, windows and math.</p></div>
<div class="card"><h2 style="margin-top:0">Sources</h2>
<p><b>News volume and tone.</b> GDELT DOC 2.0 API, raw article count over 28 days and average document tone.
Queries are exact-name matches; ambiguous names carry a disambiguating term (for example Mike Rogers is queried together with Michigan
because an Alabama congressman shares the name). Tone is GDELT's linguistic measure of the coverage, not public opinion.</p>
<p><b>Wikipedia attention.</b> Wikimedia Pageviews API, user pageviews of each politician's English Wikipedia article over 14 days.
A neutral, party-agnostic proxy for public curiosity.</p>
<p><b>Bluesky.</b> Public AT Protocol appview. Only accounts with a valid platform verification are counted;
parody and fan accounts are excluded, which is why several politicians correctly show as absent.</p>
<h2>What this is not</h2>
<p>Attention is not support. Coverage tone is not sentiment about the politician from voters. Nothing here predicts election
outcomes, and no metric is adjusted differently by party. This pilot tracks 8 politicians in 3 marquee 2026 Senate races
and refreshes weekly.</p>
<h2>Who built this</h2>
<p>Political Pulse is a project by <a href="https://www.juicer.io/?utm_source=political-pulse">Juicer</a>, the social feed
platform that senators, parliaments, city governments and campaigns use to show their live social media on their websites.
The pipeline will be released as open source so journalists and researchers can extend it.</p></div>"""
(SITE / "methodology.html").write_text(page("Political Pulse methodology", "How Political Pulse measures attention: GDELT, Wikipedia and Bluesky, identically for both parties.", meth))

print("built:", [f.name for f in SITE.glob("*.html")], "+", len(list((SITE/'p').glob('*.html'))), "profiles")
