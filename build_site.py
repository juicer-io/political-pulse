#!/usr/bin/env python3
"""Political Pulse site generator.
index.html      = full US Congress leaderboard (interactive, all sitting members)
race-*.html     = 2026 spotlight races (marquee data incl. news volume/tone)
australia.html  = full Australian Parliament board
p/us-*.html     = one profile per member of Congress
p/au-*.html     = one profile per Australian MP/senator
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
(SITE / "p").mkdir(parents=True, exist_ok=True)
(SITE / "img").mkdir(exist_ok=True)

MARQUEE = json.load(open(ROOT / "data/data.json"))
US = json.load(open(ROOT / "data/data_us_full.json")) if (ROOT / "data/data_us_full.json").exists() else {"people": []}
AU = json.load(open(ROOT / "data/data_au.json")) if (ROOT / "data/data_au.json").exists() else None
BSKY = json.load(open(ROOT / "data/bsky_us.json")) if (ROOT / "data/bsky_us.json").exists() else {}
POSTS = json.load(open(ROOT / "data/posts_us.json")) if (ROOT / "data/posts_us.json").exists() else {}
SOCIAL = json.load(open(ROOT / "data/social_us.json")) if (ROOT / "data/social_us.json").exists() else {}
XF = json.load(open(ROOT / "data/x_followers.json")) if (ROOT / "data/x_followers.json").exists() else {"followers": {}}
SOCIAL_AU = json.load(open(ROOT / "data/social_au.json")) if (ROOT / "data/social_au.json").exists() else {}
BSKY_AU = json.load(open(ROOT / "data/bsky_au.json")) if (ROOT / "data/bsky_au.json").exists() else {}
POSTS_AU = json.load(open(ROOT / "data/posts_au.json")) if (ROOT / "data/posts_au.json").exists() else {}
GEN = "2026-08-17"

INK, INK2, INK3 = "#16283a", "#4d6178", "#8195a8"
DEM, REP, IND = "#2457c5", "#c03434", "#5a6b78"
NAVY, CORAL = "#143348", "#F05B4A"
PARTY_COLOR = {"D": DEM, "R": REP, "I": IND}

# merge marquee extras (news, bsky posts) into the full-roster records by bioguide
by_bg = {p.get("bioguide"): p for p in MARQUEE["people"] if p.get("bioguide")}
for p in US["people"]:
    m = by_bg.get(p.get("bioguide"))
    if m:
        for k in ("news_articles_28d", "news_tone_avg", "bsky_top_posts"):
            if m.get(k) is not None:
                p[k] = m[k]
    b = BSKY.get(p["slug"])
    if b:
        p["bsky"] = b["handle"]
        p["bsky_followers"] = b["followers"]

CSS = f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font:16px/1.55 -apple-system,"Segoe UI",Roboto,sans-serif; color:{INK}; background:#f6f8fa; }}
a {{ color:{DEM}; text-decoration:none; }} a:hover {{ text-decoration:underline; }}
.wrap {{ max-width:1120px; margin:0 auto; padding:0 20px; }}
.top {{ background:{NAVY}; color:#fff; padding:12px 0; font-size:14px; }}
.top .wrap {{ display:flex; align-items:center; gap:12px; flex-wrap:wrap; }}
.top a {{ color:#fff; opacity:.85; }} .top b a {{ opacity:1; }}
.top .pj {{ margin-left:auto; background:{CORAL}; color:#fff; padding:3px 12px; border-radius:999px; font-weight:700; font-size:12px; }}
.hero {{ padding:38px 0 20px; }}
h1 {{ font-family:'Montserrat',sans-serif; font-weight:800; font-size:34px; letter-spacing:-1px; line-height:1.12; }}
.sub {{ color:{INK2}; max-width:760px; margin-top:10px; }}
.stamp {{ color:{INK3}; font-size:13px; margin-top:8px; }}
.card {{ background:#fff; border:1px solid #e2e8ee; border-radius:14px; padding:20px 22px;
  box-shadow:0 1px 2px rgba(16,39,56,.05), 0 10px 24px rgba(16,39,56,.06); }}
h2 {{ font-family:'Montserrat',sans-serif; font-weight:700; font-size:20px; letter-spacing:-.3px; margin:30px 0 12px; }}
table {{ width:100%; border-collapse:collapse; }}
th {{ text-align:left; font-size:11px; text-transform:uppercase; letter-spacing:.05em; color:{INK3};
     padding:8px 10px; border-bottom:1px solid #e2e8ee; white-space:nowrap; }}
th.sort {{ cursor:pointer; }} th.sort:hover {{ color:{INK}; }}
td {{ padding:9px 10px; border-bottom:1px solid #eef2f5; vertical-align:middle; font-size:14px; }}
.pchip {{ display:inline-block; width:18px; height:18px; border-radius:50%; color:#fff; font-size:10px;
  font-weight:700; text-align:center; line-height:18px; margin-right:7px; flex:none; }}
.who {{ display:flex; align-items:center; gap:10px; }}
.who .nm b {{ display:block; font-size:14px; }} .who .nm span {{ color:{INK3}; font-size:12px; }}
.bar {{ height:7px; background:#e8edf1; border-radius:4px; overflow:hidden; min-width:70px; max-width:130px; }}
.bar i {{ display:block; height:100%; border-radius:4px; background:{INK2}; }}
.num {{ font-variant-numeric:tabular-nums; }}
.up {{ color:#1f7a4d; font-weight:600; font-size:12px; }} .down {{ color:{REP}; font-weight:600; font-size:12px; }}
.na {{ color:{INK3}; font-size:12px; }}
.grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }}
.cta {{ background:{NAVY}; color:#fff; border:none; }}
.cta h3 {{ font-size:18px; margin-bottom:6px; }} .cta p {{ color:#c6d2dc; font-size:14px; }}
.btn {{ display:inline-block; margin-top:14px; background:{CORAL}; color:#fff; font-weight:700; padding:10px 20px; border-radius:8px; }}
.btn:hover {{ text-decoration:none; opacity:.92; }}
.btnlink {{ display:inline-block; border:1px solid #dde4ea; border-radius:8px; padding:6px 12px; font-size:13px;
  background:#fff; color:{INK2}; font-weight:600; }}
.btnlink:hover {{ text-decoration:none; border-color:{INK3}; }}
.avatar {{ width:40px; height:40px; border-radius:50%; object-fit:cover; object-position:top; flex:none; background:#e8edf1; }}
.avatar.lg {{ width:84px; height:84px; }}
.avatar.init {{ display:flex; align-items:center; justify-content:center; color:#fff; font-weight:700; }}
.toolbar {{ display:flex; gap:10px; flex-wrap:wrap; margin:14px 0; }}
.toolbar input, .toolbar select {{ padding:9px 12px; border:1px solid #dde4ea; border-radius:8px; font-size:14px;
  background:#fff; color:{INK}; }}
.toolbar input {{ flex:1; min-width:180px; }}
.count {{ color:{INK3}; font-size:13px; align-self:center; }}
.metrics {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin:18px 0; }}
.metric {{ background:#fff; border:1px solid #e2e8ee; border-radius:12px; padding:14px 16px;
  box-shadow:0 1px 2px rgba(16,39,56,.06), 0 8px 20px rgba(16,39,56,.07); }}
.metric .k {{ font-size:12px; color:{INK3}; }} .metric .v {{ font-size:24px; font-weight:700; }}
.metric .d {{ font-size:12px; color:{INK2}; }}
.post {{ border:1px solid #e2e8ee; border-radius:10px; padding:12px 14px; margin-bottom:10px; background:#fff; font-size:14px; }}
.wall {{ display:flex; gap:16px; overflow-x:auto; scroll-snap-type:x mandatory; padding:6px 2px 16px; }}
.wall {{ perspective:1200px; }}
.wcard {{ flex:0 0 320px; scroll-snap-align:start; border-radius:18px; font-size:14px;
  display:flex; flex-direction:column; overflow:hidden; border:1px solid rgba(226,232,238,.9);
  background:linear-gradient(178deg, #ffffff 0%, #fbfcfe 70%, #f4f7fa 100%);
  box-shadow:0 1px 2px rgba(16,39,56,.10), 0 6px 14px rgba(16,39,56,.10), 0 18px 34px rgba(16,39,56,.10);
  transition:transform .22s cubic-bezier(.2,.8,.3,1.1), box-shadow .22s ease; }}
.wcard:hover {{ transform:translateY(-8px) rotateX(2.5deg) scale(1.025); text-decoration:none;
  box-shadow:0 2px 4px rgba(16,39,56,.12), 0 14px 28px rgba(16,39,56,.16), 0 34px 64px rgba(16,39,56,.22); }}
.wcard .ph {{ display:flex; align-items:center; gap:10px; padding:14px 16px 10px; }}
.wcard .ph img {{ width:38px; height:38px; border-radius:50%; object-fit:cover; object-position:top; }}
.wcard .ph .pn b {{ display:block; font-size:13.5px; color:{INK}; }}
.wcard .ph .pn span {{ font-size:12px; color:{INK3}; }}
.wcard .xmark {{ margin-left:auto; width:22px; height:22px; border-radius:6px; background:#0f1419; color:#fff;
  font-weight:800; font-size:12px; display:flex; align-items:center; justify-content:center; flex:none; }}
.wcard .txt {{ padding:0 16px; margin:2px 0 12px; flex:1; overflow-wrap:break-word; color:{INK}; line-height:1.5; }}
.wcard .eng {{ display:flex; gap:16px; padding:10px 16px 13px; border-top:1px solid #eef2f5;
  color:{INK3}; font-size:12.5px; font-variant-numeric:tabular-nums; }}
.wcard .eng span {{ display:flex; align-items:center; gap:5px; }}
.wcard .eng svg {{ width:14px; height:14px; fill:none; stroke:{INK3}; stroke-width:1.8; }}
.wcard .wdate {{ margin-left:auto; }}
.pjbadge {{ display:inline-block; font-family:'Montserrat',sans-serif; font-size:15px; font-weight:800;
  color:#fff; background:{CORAL}; padding:5px 16px; border-radius:999px; margin-left:10px; vertical-align:middle;
  box-shadow:0 3px 10px rgba(240,91,74,.35); transition:transform .15s ease, box-shadow .15s ease; }}
.pjbadge:hover {{ transform:translateY(-2px); box-shadow:0 6px 16px rgba(240,91,74,.45); text-decoration:none; color:#fff; }}
.mini {{ width:225px; background:linear-gradient(178deg,#fff 0%,#f7fafc 100%); border:1px solid #e9eef3;
  border-radius:12px; padding:10px 12px; cursor:pointer; text-align:left;
  box-shadow:0 1px 2px rgba(16,39,56,.09), 0 6px 14px rgba(16,39,56,.10);
  transition:transform .18s ease, box-shadow .18s ease; }}
.mini:hover {{ transform:translateY(-3px); box-shadow:0 3px 6px rgba(16,39,56,.12), 0 14px 28px rgba(16,39,56,.18); }}
.mini .mhead {{ display:flex; gap:9px; align-items:flex-start; }}
.mini .mavatar {{ width:28px; height:28px; border-radius:50%; object-fit:cover; object-position:top; flex:none;
  border:1.5px solid #fff; box-shadow:0 1px 4px rgba(16,39,56,.25); }}
.mini .mtxt {{ font-size:12px; line-height:1.45; color:{INK}; display:-webkit-box; -webkit-line-clamp:3;
  -webkit-box-orient:vertical; overflow:hidden; min-height:3.9em; flex:1; }}
.mini.msync .mtxt {{ color:{INK3}; font-style:italic; min-height:auto; }}
.mini .mrow {{ display:flex; align-items:center; gap:8px; margin-top:7px; font-size:11px; color:{INK3}; }}
.mini .mx {{ background:#0f1419; color:#fff; font-weight:800; font-size:9px; border-radius:4px; padding:1px 5px; }}
.marrow {{ margin-left:auto; width:24px; height:24px; border-radius:50%; border:1px solid #dde4ea; background:#fff;
  cursor:pointer; font-size:14px; line-height:1; color:{INK2}; flex:none; }}
.marrow:hover {{ border-color:{CORAL}; color:{CORAL}; }}
.wchip {{ display:inline-block; background:#e8f3ec; color:#1f7a4d; font-size:10px; font-weight:700;
  border-radius:999px; padding:1px 7px; margin-left:6px; vertical-align:middle; }}
.post .m {{ color:{INK3}; font-size:12px; margin-top:6px; }}
footer {{ margin-top:50px; padding:26px 0 40px; color:{INK3}; font-size:13px; border-top:1px solid #e2e8ee; }}
.faq details {{ background:#fff; border:1px solid #e2e8ee; border-radius:10px; padding:14px 18px; margin-bottom:10px; }}
.faq summary {{ font-weight:600; cursor:pointer; }} .faq p {{ margin-top:8px; color:{INK2}; font-size:14px; }}
.legend {{ font-size:13px; color:{INK2}; margin:6px 0 10px; }}
.legend i {{ display:inline-block; width:10px; height:10px; border-radius:50%; margin:0 4px 0 12px; }}
@media (max-width:720px) {{ .grid2,.metrics {{ grid-template-columns:1fr; }} h1 {{ font-size:25px; }}
  .tblwrap {{ overflow-x:auto; }} }}
"""


def fmt(n):
    if n is None:
        return None
    return f"{n/1000000:.1f}M" if n >= 1000000 else (f"{n/1000:.0f}k" if n >= 10000 else f"{n:,}")


def trend(last, prev):
    if not last or not prev:
        return ""
    pct = round(100.0 * (last - prev) / prev)
    cls = "up" if pct >= 0 else "down"
    return f'<span class="{cls}">{"&#9650;" if pct >= 0 else "&#9660;"} {abs(pct)}%</span>'


def avatar(p, lg=False, color=None):
    cls = "avatar lg" if lg else "avatar"
    color = color or PARTY_COLOR.get(p.get("party"), IND)
    init = "".join(w[0] for w in p["name"].split()[:2])
    if p.get("bioguide"):
        url = f"https://unitedstates.github.io/images/congress/225x275/{p['bioguide']}.jpg"
        return (f'<img class="{cls}" loading="lazy" src="{url}" alt="{p["name"]}" '
                f'onerror="this.style.display=\'none\'">')
    return f'<div class="{cls} init" style="background:{color}">{init}</div>'


def spark(p, w=520, h=64):
    days = p.get("wiki_daily")
    if not days:
        return ""
    vals = [v for _, v in days]
    mx = max(vals) or 1
    pts = " ".join(f"{i * w / (len(vals)-1):.1f},{h - (v / mx) * (h-4):.1f}" for i, v in enumerate(vals))
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="max-width:100%" role="img" '
            f'aria-label="Wikipedia daily pageviews"><polyline points="{pts}" fill="none" stroke="{INK2}" '
            f'stroke-width="2" stroke-linecap="round"/></svg>')


def page(title, desc, body, depth=0, extra_head=""):
    pre = "../" * depth
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&display=swap" rel="stylesheet"><style>{CSS}</style>{extra_head}
<script>document.addEventListener("click", function(e) {{
  var a = e.target.closest("a");
  if (a && a.host && a.host !== location.host) {{ a.target = "_blank"; a.rel = "noopener"; }}
}});</script></head><body>
<div class="top"><div class="wrap"><b><a href="{pre}index.html">Political Pulse</a></b>
<a href="{pre}index.html">US Congress</a> <a href="{pre}australia.html">Australia</a>
<a href="{pre}methodology.html">Methodology</a>
<a class="pj" href="https://www.juicer.io/?utm_source=political-pulse&utm_medium=referral">Powered by Juicer</a></div></div>
<div class="wrap">{body}</div>
<div class="wrap"><footer>Political Pulse is an open data project by <a href="https://www.juicer.io/?utm_source=political-pulse">Juicer</a>,
the social feed platform used by senators, parliaments, city governments and campaigns.
Data: Wikipedia, Bluesky public API, GDELT. Photos: unitedstates/images (public domain). Updated {GEN}.
Not affiliated with any campaign or party. Attention is not support; this site makes no election predictions.</footer></div>
</body></html>"""


def claim_cta(name=None):
    who = f"Are you on {name}'s team?" if name else "Are you a campaign or comms team?"
    return f"""<div class="card cta"><h3>{who}</h3>
<p>Put a live wall of your own social posts on your official website in about five minutes.
Politicians in the US Senate, Australian Parliament and city governments worldwide already run their feeds on Juicer.</p>
<a class="btn" href="https://www.juicer.io/?utm_source=political-pulse&utm_medium=referral&utm_campaign=claim">Embed your feed free</a></div>"""


# ================= index: full congress board =================
filled = sum(1 for p in US["people"] if p.get("wiki_14d") is not None)
pending = len(US["people"]) - filled
verified = sum(1 for p in US["people"] if p.get("bsky_followers"))

board = [{"slug": p["slug"], "n": p["name"], "pa": p["party"], "st": p.get("state"),
          "ch": p["chamber"], "bg": p.get("bioguide"),
          "w": p.get("wiki_14d"), "wl": p.get("wiki_last7"), "wp": p.get("wiki_prev7"),
          "bf": p.get("bsky_followers"), "bh": p.get("bsky"),
          "wl2": bool(POSTS.get(p["slug"])),
          "mp": [{"t": (x.get("text") or "")[:110], "l": x.get("likes"), "d": x.get("date")}
                 for x in (POSTS.get(p["slug"]) or [])[:3]],
          "tw": SOCIAL.get(p.get("bioguide"), {}).get("twitter"),
          "tf": XF["followers"].get(SOCIAL.get(p.get("bioguide"), {}).get("twitter") or "")} for p in US["people"]]
states = sorted({p["state"] for p in US["people"] if p.get("state")})
pend_note = f" &middot; attention data still filling for {pending} members" if pending else ""
XH = "X followers &#8597;" if XF["followers"] else "X account"

board_js = f"""
<script>
const DATA = {json.dumps(board).replace("</", "<\\/")};
const PC = {{"D": "{DEM}", "R": "{REP}", "I": "{IND}"}};
const fmtn = n => n == null ? null : (n >= 1e6 ? (n/1e6).toFixed(1)+"M" : n >= 1e4 ? Math.round(n/1e3)+"k" : n.toLocaleString());
let sortKey = "w";
function render() {{
  const q = document.getElementById("q").value.toLowerCase();
  const ch = document.getElementById("ch").value, pa = document.getElementById("pa").value, st = document.getElementById("st").value;
  let rows = DATA.filter(p => (!q || p.n.toLowerCase().includes(q) || (p.st || "").toLowerCase() === q)
      && (!ch || p.ch === ch) && (!pa || p.pa === pa) && (!st || p.st === st));
  rows.sort((a, b) => (b[sortKey] ?? -1) - (a[sortKey] ?? -1));
  const mx = Math.max(...DATA.map(p => p.w || 0), 1);
  document.getElementById("count").textContent = rows.length + " of " + DATA.length + " members";
  document.getElementById("tbody").innerHTML = rows.map((p, i) => {{
    const img = p.bg ? `<img class="avatar" loading="lazy" src="https://unitedstates.github.io/images/congress/225x275/${{p.bg}}.jpg" onerror="this.style.display='none'" alt="">` : "";
    const tr = (p.wl && p.wp) ? (() => {{ const pc = Math.round(100 * (p.wl - p.wp) / p.wp);
      return `<span class="${{pc >= 0 ? "up" : "down"}}">${{pc >= 0 ? "&#9650;" : "&#9660;"}} ${{Math.abs(pc)}}%</span>`; }})() : "";
    const att = p.w != null ? `<div class="num">${{fmtn(p.w)}} ${{tr}}</div>
      <div class="bar"><i style="width:${{Math.round(100 * (p.w || 0) / mx)}}%"></i></div>` : `<span class="na">data filling</span>`;
    return `<tr><td><span class="na num">${{i + 1}}</span></td>
      <td><div class="who">${{img}}<span class="pchip" style="background:${{PC[p.pa]}}">${{p.pa}}</span>
      <span class="nm"><b><a href="p/${{p.slug}}.html">${{p.n}}</a>${{p.wl2 ? ' <span class="wchip">posts</span>' : ''}}</b><span>${{p.ch}} &middot; ${{p.st}}</span></span></div></td>
      <td>${{att}}</td>
      <td>${{p.tw ? (p.tf != null
        ? `<a class="num" href="https://x.com/${{p.tw}}" rel="nofollow noopener">${{fmtn(p.tf)}} &#8599;</a>`
        : `<a href="https://x.com/${{p.tw}}" rel="nofollow noopener">@${{p.tw}}</a>`) : `<span class="na">none listed</span>`}}</td>
      <td>${{p.bf != null ? `<a class="num" href="https://bsky.app/profile/${{p.bh}}" rel="nofollow noopener">${{fmtn(p.bf)}} &#8599;</a>` : `<span class="na">not verified</span>`}}</td>
      <td>${{(() => {{
        const av = p.bg ? `<img class="mavatar" loading="lazy" src="https://unitedstates.github.io/images/congress/225x275/${{p.bg}}.jpg" onerror="this.style.display='none'" alt="">` : "";
        if (p.mp && p.mp.length) return `<div class="mini" data-slug="${{p.slug}}" data-i="0" onclick="location.href='p/${{p.slug}}.html'">
          <div class="mhead">${{av}}<div class="mtxt">${{esc(p.mp[0].t)}}</div></div>
          <div class="mrow"><span class="mx">&#120143;</span><span class="ml">&#9825; ${{fmtn(p.mp[0].l) ?? 0}}</span><span class="md">${{p.mp[0].d || ""}}</span>
          ${{p.mp.length > 1 ? `<button class="marrow" onclick="event.stopPropagation();nextMini(this)">&#8250;</button>` : ""}}</div></div>`;
        const msg = p.tw ? "posts syncing, coming in the next refresh" : "no official X account listed";
        return `<div class="mini msync" onclick="location.href='p/${{p.slug}}.html'">
          <div class="mhead">${{av}}<div class="mtxt">${{msg}}</div></div></div>`;
      }})()}}</td></tr>`;
  }}).join("");
}}
function setSort(k) {{ sortKey = k; render(); }}
const esc = s => (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;");
function nextMini(btn) {{
  const card = btn.closest(".mini");
  const rec = DATA.find(x => x.slug === card.dataset.slug);
  if (!rec || !rec.mp.length) return;
  const i = (parseInt(card.dataset.i || "0") + 1) % rec.mp.length;
  card.dataset.i = i;
  card.querySelector(".mtxt").textContent = rec.mp[i].t;
  card.querySelector(".ml").innerHTML = "&#9825; " + (fmtn(rec.mp[i].l) ?? 0);
  card.querySelector(".md").textContent = rec.mp[i].d || "";
}}
window.addEventListener("DOMContentLoaded", render);
</script>"""

index_body = f"""<div class="hero"><h1>Every member of Congress, ranked by attention</h1>
<p class="sub">All {len(US["people"])} sitting members of the US Senate and House on one open leaderboard:
Wikipedia attention, week-over-week movement and verified Bluesky reach. Both parties, every state, one methodology, no predictions.</p>
<p class="stamp">Updated {GEN}{pend_note} &middot; {verified} members have verified Bluesky accounts &middot; <a href="methodology.html">methodology</a></p></div>
<div class="toolbar">
<input id="q" type="search" placeholder="Search name or state code&hellip;" oninput="render()">
<select id="ch" onchange="render()"><option value="">Both chambers</option><option>Senate</option><option>House</option></select>
<select id="pa" onchange="render()"><option value="">All parties</option><option value="D">Democratic</option><option value="R">Republican</option><option value="I">Independent</option></select>
<select id="st" onchange="render()"><option value="">All states</option>{"".join(f"<option>{s}</option>" for s in states)}</select>
<span class="count" id="count"></span></div>
<div class="legend">Party: <i style="background:{DEM}"></i> Democratic <i style="background:{REP}"></i> Republican
<i style="background:{IND}"></i> Independent</div>
<div class="card tblwrap" style="padding:6px 10px"><table>
<tr><th>#</th><th>Member</th><th class="sort" onclick="setSort('w')">Wikipedia attention 14d &#8597;</th>
<th class="sort" onclick="setSort('tf')" title="Follower counts activate once X API access is configured">{XH}</th>
<th class="sort" onclick="setSort('bf')">Bluesky followers &#8597;</th>
<th>Latest post <span style="color:{CORAL};text-transform:none">powered by Juicer</span></th></tr>
<tbody id="tbody"></tbody></table></div>
<h2>2026 spotlight races</h2>
<p class="sub" style="margin-bottom:12px">The two open-seat Senate battles of this November's midterms, tracked candidate
versus candidate with news coverage volume and tone on top of the attention metrics.</p>
<div class="grid2">
<a class="card" href="race-michigan.html"><b>Michigan Senate, open seat</b><br>Abdul El-Sayed (D) vs Mike Rogers (R), with news volume and tone</a>
<a class="card" href="race-north-carolina.html"><b>North Carolina Senate, open seat</b><br>Roy Cooper (D) vs Michael Whatley (R), with news volume and tone</a></div>
<h2>For campaigns and analysts</h2>
<div class="grid2">{claim_cta()}
<div class="card cta"><h3>Build your own tracker</h3>
<p>This site runs on public APIs plus the Juicer platform, and the pipeline is being released as open source.
The Juicer API pulls cross-platform social content for any set of accounts or hashtags.</p>
<a class="btn" href="https://developers.juicer.io/?utm_source=political-pulse">Explore the Juicer API</a></div></div>
<h2>Common questions</h2>
<div class="faq">
<details><summary>How can I track what people say about a politician on social media?</summary>
<p>Combine platform APIs where they are open (Bluesky), news databases like GDELT for coverage volume and tone,
and a feed aggregation platform like <a href="https://www.juicer.io/?utm_source=political-pulse">Juicer</a> to collect
posts, hashtags and mentions across Instagram, Facebook, X, TikTok, YouTube, Reddit and Bluesky in one place.</p></details>
<details><summary>What replaced CrowdTangle for tracking political content?</summary>
<p>No single free tool did. Researchers now combine open sources like the Bluesky firehose, GDELT and Wikipedia attention data.
For collecting and embedding the actual posts, Juicer aggregates a politician's cross-platform content into one feed.</p></details>
<details><summary>How many members of Congress are on Bluesky?</summary>
<p>As of August 2026, {verified} of {len(US["people"])} sitting members have a platform-verified Bluesky account
according to the public Bluesky API. This board shows the count per member and updates weekly.</p></details>
<details><summary>Does high attention mean a politician is winning?</summary>
<p>No. Attention measures visibility, not voter support. This site makes no election predictions and treats
both parties with identical methodology.</p></details>
<details><summary>How do politicians show their social media on their official websites?</summary>
<p>Most use an embed service. Juicer powers live social walls for sitting US senators, members of the Australian Parliament,
city governments and active campaigns.</p></details></div>"""
(SITE / "index.html").write_text(page(
    "Political Pulse: every member of Congress ranked by attention",
    f"Open leaderboard of all {len(US['people'])} members of the US Congress: Wikipedia attention, Bluesky reach, 2026 race trackers. By Juicer.",
    index_body, extra_head=board_js))

# ================= race pages (marquee data) =================
MQ = {p["slug"]: p for p in MARQUEE["people"]}


def race_page(state, slug, d_slug, r_slug, blurb):
    cols = ""
    for key in (d_slug, r_slug):
        p = MQ[key]
        news = p.get("news_articles_28d")
        tone = p.get("news_tone_avg")
        bsky = (f'{fmt(p.get("bsky_followers"))} followers &middot; {p.get("bsky_avg_likes", 0)} avg likes/post'
                if p.get("bsky_followers") else "not on Bluesky")
        cols += f"""<div class="card"><div class="who">{avatar(p, lg=True)}
<span class="nm"><b style="font-size:17px"><span class="pchip" style="background:{PARTY_COLOR[p["party"]]}">{p["party"]}</span>{p["name"]}</b>
<span>{p["role"]}</span></span></div>
<div class="metrics" style="grid-template-columns:1fr 1fr">
<div class="metric"><div class="k">Wikipedia attention 14d</div><div class="v num">{fmt(p.get("wiki_14d"))}</div>
<div class="d">{trend(p.get("wiki_last7"), p.get("wiki_prev7"))} week over week</div></div>
<div class="metric"><div class="k">News articles 28d</div><div class="v num">{fmt(news) if news is not None else "&mdash;"}</div>
<div class="d">{f"avg tone {tone:+.1f} (GDELT)" if tone is not None else ""}</div></div></div>
<div>{spark(p, 460, 56)}</div><div class="na">Wikipedia daily pageviews, 14 days</div>
<p style="margin-top:10px;font-size:14px;color:{INK2}"><b>Bluesky:</b> {bsky}</p></div>"""
    body = f"""<div class="hero"><h1>{state} Senate: the attention race</h1>
<p class="sub">{blurb}</p><p class="stamp">Updated {GEN} &middot; identical methodology for both candidates</p></div>
<div class="grid2">{cols}</div><div style="margin-top:16px">{claim_cta()}</div>"""
    (SITE / f"race-{slug}.html").write_text(page(f"{state} Senate 2026 attention tracker",
        f"Open data attention comparison for the {state} Senate race. By Juicer.", body))


race_page("Michigan", "michigan", "abdul-el-sayed", "mike-rogers",
          "An open seat. Abdul El-Sayed won the Democratic primary and faces Republican Mike Rogers, a former congressman.")
race_page("North Carolina", "north-carolina", "roy-cooper", "michael-whatley",
          "An open seat vacated by Thom Tillis. Former Governor Roy Cooper faces former RNC Chair Michael Whatley.")

# ================= US profiles =================
ranked_us = sorted(US["people"], key=lambda x: -(x.get("wiki_14d") or 0))
for p in US["people"]:
    w = p.get("wiki_14d")
    news = p.get("news_articles_28d")
    tone = p.get("news_tone_avg")
    if news is not None:
        extra_metric = (f'<div class="metric"><div class="k">News articles, 28 days</div><div class="v num">{fmt(news)}</div>'
                        f'<div class="d">{f"average tone {tone:+.1f} (GDELT)" if tone is not None else ""}</div></div>')
    else:
        extra_metric = (f'<div class="metric"><div class="k">Bluesky followers</div>'
                        f'<div class="v num">{fmt(p.get("bsky_followers")) or "&mdash;"}</div>'
                        f'<div class="d">{"verified account @" + p["bsky"] if p.get("bsky") else "no verified account found"}</div></div>')
    soc = SOCIAL.get(p.get("bioguide"), {})
    links = []
    if soc.get("twitter"): links.append(f'<a class="btnlink" href="https://x.com/{soc["twitter"]}" rel="nofollow noopener">X @{soc["twitter"]}</a>')
    if soc.get("instagram"): links.append(f'<a class="btnlink" href="https://www.instagram.com/{soc["instagram"]}/" rel="nofollow noopener">Instagram</a>')
    if soc.get("facebook"): links.append(f'<a class="btnlink" href="https://www.facebook.com/{soc["facebook"]}" rel="nofollow noopener">Facebook</a>')
    if soc.get("youtube"): links.append(f'<a class="btnlink" href="https://www.youtube.com/{soc["youtube"]}" rel="nofollow noopener">YouTube</a>')
    if p.get("bsky"): links.append(f'<a class="btnlink" href="https://bsky.app/profile/{p["bsky"]}" rel="nofollow noopener">Bluesky</a>')
    socials = ""
    if links:
        socials = (f'<div class="card" style="margin-top:16px"><b>Official accounts</b>'
                   f'<div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap">{"".join(links)}</div>'
                   f'<p class="na" style="margin-top:10px">One person, {len(links)} platforms. Juicer merges all of them into a single live feed for a website.</p></div>')
    posts = ""
    wall_posts = POSTS.get(p["slug"]) or []
    if wall_posts:
        cards = ""
        HEART = '<svg viewBox="0 0 24 24"><path d="M12 21s-7.5-4.8-10-9.3C.6 8.4 2.5 5 6 5c2.2 0 3.6 1.2 6 3.7C14.4 6.2 15.8 5 18 5c3.5 0 5.4 3.4 4 6.7C19.5 16.2 12 21 12 21z"/></svg>'
        REPLY = '<svg viewBox="0 0 24 24"><path d="M21 12a8 8 0 0 1-8 8H5l-2 2V12a8 8 0 0 1 8-8h2a8 8 0 0 1 8 8z"/></svg>'
        SHARE = '<svg viewBox="0 0 24 24"><path d="M17 2l4 4-4 4M21 6H9a5 5 0 0 0-5 5M7 22l-4-4 4-4M3 18h12a5 5 0 0 0 5-5"/></svg>'
        member_photo = (f"https://unitedstates.github.io/images/congress/225x275/{p['bioguide']}.jpg"
                        if p.get("bioguide") else "")
        member_handle = soc.get("twitter", "")
        for wpost in wall_posts:
            def _n(v): return f"{v:,}" if v is not None else "0"
            cards += (f'<a class="wcard" href="{wpost["url"]}">'
                      f'<span class="ph">{f"<img src=\"{member_photo}\" alt=\"\" onerror=\"this.style.display=chr(39)none{chr(39)}\">" if member_photo else ""}'
                      f'<span class="pn"><b>{p["name"]}</b><span>@{member_handle}</span></span>'
                      f'<span class="xmark">&#120143;</span></span>'
                      f'<span class="txt">{(wpost["text"] or "").replace("<", "&lt;")[:240]}</span>'
                      f'<span class="eng"><span>{HEART} {_n(wpost.get("likes"))}</span>'
                      f'<span>{REPLY} {_n(wpost.get("comments"))}</span>'
                      f'<span>{SHARE} {_n(wpost.get("shares"))}</span>'
                      f'<span class="wdate">{wpost["date"]}</span></span></a>')
        badge = '<a class="pjbadge" href="https://www.juicer.io/api?utm_source=political-pulse&utm_medium=referral&utm_campaign=wall-badge">powered by Juicer</a>'
        src_line = "their official X account, ingested by a live Juicer feed"
        handles_list = []
        if soc.get("twitter"): handles_list.append(("X", "@" + soc["twitter"]))
        if p.get("bsky"): handles_list.append(("Bluesky", p["bsky"]))
        if soc.get("instagram"): handles_list.append(("Instagram", "@" + soc["instagram"]))
        chips = "".join(f'<code style="background:rgba(255,255,255,.12);border-radius:6px;padding:3px 8px;margin-right:8px;font-size:13px">{plat}: {h}</code>'
                        for plat, h in handles_list)
        signup = (f"https://www.juicer.io/sign-up?utm_source=political-pulse&utm_medium=referral"
                  f"&utm_campaign=wall-embed&utm_content={p['slug']}")
        embed_cta = f"""<div class="card cta" style="margin-top:16px"><h3>Get this wall on your website</h3>
<p>This exact feed, live and auto-updating, embeddable on any site. Create a free Juicer account,
add {p["name"].split()[-1]}'s official accounts as sources and paste one line of embed code. About five minutes.</p>
<p style="margin-top:10px">{chips}</p>
<a class="btn" href="{signup}">Create your free Juicer account</a></div>"""
        posts = (f'<h2>Latest posts {badge}</h2><div class="wall">{cards}</div>'
                 f'<p class="na">Newest posts from {src_line}. Swipe to browse.</p>' + embed_cta)
    else:
        posts = ('<div class="card" style="margin-top:16px"><b>Post wall syncing</b>'
                 '<p class="na" style="margin-top:6px">This member&#39;s X posts are being ingested and will '
                 'appear here in a coming refresh. Their official accounts are linked above, and follower '
                 'numbers on the leaderboard stay current.</p></div>')
    seat = f"{p['chamber']} &middot; {p.get('state')}" + (f"-{p['district']}" if p.get("district") not in (None, 0, "0") else "")
    body = f"""<div class="hero"><div class="who">{avatar(p, lg=True)}
<span class="nm" style="font-size:20px"><b><span class="pchip" style="background:{PARTY_COLOR[p["party"]]}">{p["party"]}</span>{p["name"]}</b>
<span>United States Congress &middot; {seat}</span></span></div></div>
<div class="metrics">
<div class="metric"><div class="k">Wikipedia attention, 14 days</div><div class="v num">{fmt(w) if w is not None else "&mdash;"}</div>
<div class="d">{trend(p.get("wiki_last7"), p.get("wiki_prev7"))} week over week</div></div>
<div class="metric"><div class="k">Rank in Congress</div><div class="v num">#{ranked_us.index(p) + 1}</div>
<div class="d">of {len(US["people"])} members by attention</div></div>
{extra_metric}</div>
{f'<div class="card"><b>Wikipedia attention, daily</b><br>{spark(p)}</div>' if p.get("wiki_daily") else ''}
{socials}
{posts}
<div style="margin-top:20px">{claim_cta(p["name"])}</div>"""
    (SITE / "p" / f"{p['slug']}.html").write_text(page(f"{p['name']}: attention tracker",
        f"Public attention profile for {p['name']} ({p['party']}-{p.get('state')}), US Congress.", body, depth=1))

# ================= Australia =================
if AU:
    AUP = AU["people"]
    AU_COLORS = {"ALP": "#c03434", "LIB": "#2457c5", "NAT": "#8a6d00", "GRN": "#1f7a4d", "PHON": "#b45309",
                 "LNP": "#2457c5", "CLP": "#2457c5", "IND": "#5a6b78", "JLN": "#5a6b78", "KAP": "#5a6b78",
                 "CA": "#5a6b78", "OTH": "#5a6b78"}
    AU_NAMES = {"ALP": "Labor", "LIB": "Liberal", "NAT": "Nationals", "GRN": "Greens", "PHON": "One Nation",
                "LNP": "Liberal National", "CLP": "Country Liberal", "IND": "Independent",
                "JLN": "Lambie Network", "KAP": "Katter", "CA": "Centre Alliance", "OTH": "Other"}
    filled_au = sum(1 for x in AUP if x.get("wiki_14d") is not None)
    ranked_au = sorted(AUP, key=lambda x: -(x.get("wiki_14d") or 0))
    board_au = []
    for x in AUP:
        soc = SOCIAL_AU.get(x["slug"], {})
        tw = soc.get("twitter")
        ba = BSKY_AU.get(x["slug"])
        board_au.append({"slug": x["slug"], "n": x["name"], "pa": x["party"], "ch": x["chamber"],
                         "w": x.get("wiki_14d"), "wl": x.get("wiki_last7"), "wp": x.get("wiki_prev7"),
                         "tw": tw, "tf": XF["followers"].get(tw) if tw else None,
                         "bh": ba["handle"] if ba else None,
                         "bf": ba.get("followers") if ba else None,
                         "mp": [{"t": (w.get("text") or "")[:110], "l": w.get("likes"), "d": w.get("date")}
                                for w in (POSTS_AU.get(x["slug"]) or [])[:3]]})
    au_parties = sorted({x["party"] for x in AUP})
    au_js = f"""
<script>
const DATA = {json.dumps(board_au)};
const PC = {json.dumps(AU_COLORS)};
const PN = {json.dumps(AU_NAMES)};
const fmtn = n => n == null ? null : (n >= 1e6 ? (n/1e6).toFixed(1)+"M" : n >= 1e4 ? Math.round(n/1e3)+"k" : n.toLocaleString());
let sortKey = "w";
function render() {{
  const q = document.getElementById("q").value.toLowerCase();
  const ch = document.getElementById("ch").value, pa = document.getElementById("pa").value;
  let rows = DATA.filter(p => (!q || p.n.toLowerCase().includes(q)) && (!ch || p.ch === ch) && (!pa || p.pa === pa));
  rows.sort((a, b) => (b[sortKey] ?? -1) - (a[sortKey] ?? -1));
  const mx = Math.max(...DATA.map(p => p.w || 0), 1);
  document.getElementById("count").textContent = rows.length + " of " + DATA.length + " members";
  document.getElementById("tbody").innerHTML = rows.map((p, i) => {{
    const tr = (p.wl && p.wp) ? (() => {{ const pc = Math.round(100 * (p.wl - p.wp) / p.wp);
      return `<span class="${{pc >= 0 ? "up" : "down"}}">${{pc >= 0 ? "&#9650;" : "&#9660;"}} ${{Math.abs(pc)}}%</span>`; }})() : "";
    const att = p.w != null ? `<div class="num">${{fmtn(p.w)}} ${{tr}}</div>
      <div class="bar"><i style="width:${{Math.round(100 * (p.w || 0) / mx)}}%"></i></div>` : `<span class="na">no article</span>`;
    const x = p.tw ? (p.tf != null
      ? `<a class="num" href="https://x.com/${{p.tw}}">${{fmtn(p.tf)}} &#8599;</a>`
      : `<a href="https://x.com/${{p.tw}}">@${{p.tw}}</a>`) : `<span class="na">none listed</span>`;
    const bs = p.bf != null ? `<a class="num" href="https://bsky.app/profile/${{p.bh}}">${{fmtn(p.bf)}} &#8599;</a>` : `<span class="na">none listed</span>`;
    const mav = `<div class="mavatar" style="background:${{PC[p.pa] || "#5a6b78"}};color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:11px">${{p.n.split(" ").map(w=>w[0]).slice(0,2).join("")}}</div>`;
    let mini;
    if (p.mp && p.mp.length) {{
      mini = `<div class="mini" data-slug="${{p.slug}}" data-i="0" onclick="location.href='p/${{p.slug}}.html'">
        <div class="mhead">${{mav}}<div class="mtxt">${{esc(p.mp[0].t)}}</div></div>
        <div class="mrow"><span class="mx">&#120143;</span><span class="ml">&#9825; ${{fmtn(p.mp[0].l) ?? 0}}</span><span class="md">${{p.mp[0].d || ""}}</span>
        ${{p.mp.length > 1 ? `<button class="marrow" onclick="event.stopPropagation();nextMini(this)">&#8250;</button>` : ""}}</div></div>`;
    }} else {{
      const msg = p.tw ? "posts syncing, coming soon" : "no official X account listed";
      mini = `<div class="mini msync" onclick="location.href='p/${{p.slug}}.html'"><div class="mhead">${{mav}}<div class="mtxt">${{msg}}</div></div></div>`;
    }}
    return `<tr><td><span class="na num">${{i + 1}}</span></td>
      <td><div class="who"><span class="pchip" style="background:${{PC[p.pa] || "#5a6b78"}}">${{p.pa[0]}}</span>
      <span class="nm"><b><a href="p/${{p.slug}}.html">${{p.n}}</a></b><span>${{PN[p.pa] || p.pa}} &middot; ${{p.ch}}</span></span></div></td>
      <td>${{att}}</td><td>${{x}}</td><td>${{bs}}</td><td>${{mini}}</td></tr>`;
  }}).join("");
}}
function setSort(k) {{ sortKey = k; render(); }}
const esc = s => (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;");
function nextMini(btn) {{
  const card = btn.closest(".mini");
  const rec = DATA.find(x => x.slug === card.dataset.slug);
  if (!rec || !rec.mp.length) return;
  const i = (parseInt(card.dataset.i || "0") + 1) % rec.mp.length;
  card.dataset.i = i;
  card.querySelector(".mtxt").textContent = rec.mp[i].t;
  card.querySelector(".ml").innerHTML = "&#9825; " + (fmtn(rec.mp[i].l) ?? 0);
  card.querySelector(".md").textContent = rec.mp[i].d || "";
}}
window.addEventListener("DOMContentLoaded", render);
</script>"""
    legend_au = " ".join(f'<i style="background:{AU_COLORS[k]}"></i> {AU_NAMES[k]}' for k in ("ALP", "LIB", "NAT", "GRN", "PHON", "IND"))
    pend_au = f" &middot; attention data still filling for {len(AUP) - filled_au} members" if filled_au < len(AUP) - 1 else ""
    au_body = f"""<div class="hero"><h1>Australia: the full Parliament board</h1>
<p class="sub">Every current member of the 48th Parliament of Australia, both chambers, ranked by public attention.
One list, every party, identical methodology. No selections, no exclusions.</p>
<p class="stamp">Updated {GEN} &middot; {len(AUP)} members tracked{pend_au} &middot; <a href="methodology.html">methodology</a></p></div>
<div class="toolbar">
<input id="q" type="search" placeholder="Search name&hellip;" oninput="render()">
<select id="ch" onchange="render()"><option value="">Both chambers</option><option>Senate</option><option>House</option></select>
<select id="pa" onchange="render()"><option value="">All parties</option>{"".join(f'<option value="{k}">{AU_NAMES.get(k, k)}</option>' for k in au_parties)}</select>
<span class="count" id="count"></span></div>
<div class="legend">Party: {legend_au}</div>
<div class="card tblwrap" style="padding:6px 10px"><table>
<tr><th>#</th><th>Member</th><th class="sort" onclick="setSort('w')">Wikipedia attention 14d &#8597;</th>
<th class="sort" onclick="setSort('tf')">X followers &#8597;</th><th class="sort" onclick="setSort('bf')">Bluesky followers &#8597;</th>
<th>Latest post <span style="color:{CORAL};text-transform:none">powered by Juicer</span></th></tr>
<tbody id="tbody"></tbody></table></div>
<div style="margin-top:16px">{claim_cta()}</div>"""
    (SITE / "australia.html").write_text(page("Australian Parliament attention board",
        "Every member of the 48th Parliament of Australia ranked by public attention. Open data, by Juicer.", au_body,
        extra_head=au_js))
    def au_wall(x, color):
        wall_posts = POSTS_AU.get(x["slug"]) or []
        tw_h = SOCIAL_AU.get(x["slug"], {}).get("twitter", "")
        init = "".join(n[0] for n in x["name"].split()[:2])
        if not wall_posts:
            msg = ("posts syncing, coming in a refresh" if tw_h else "no official X account listed on Wikidata")
            return (f'<div class="card" style="margin-top:16px"><b>Post wall</b>'
                    f'<p class="na" style="margin-top:6px">{msg}</p></div>')
        HEART = '<svg viewBox="0 0 24 24"><path d="M12 21s-7.5-4.8-10-9.3C.6 8.4 2.5 5 6 5c2.2 0 3.6 1.2 6 3.7C14.4 6.2 15.8 5 18 5c3.5 0 5.4 3.4 4 6.7C19.5 16.2 12 21 12 21z"/></svg>'
        REPLY = '<svg viewBox="0 0 24 24"><path d="M21 12a8 8 0 0 1-8 8H5l-2 2V12a8 8 0 0 1 8-8h2a8 8 0 0 1 8 8z"/></svg>'
        SHARE = '<svg viewBox="0 0 24 24"><path d="M17 2l4 4-4 4M21 6H9a5 5 0 0 0-5 5M7 22l-4-4 4-4M3 18h12a5 5 0 0 0 5-5"/></svg>'
        cards = ""
        for wpost in wall_posts:
            def _n(v): return f"{v:,}" if v is not None else "0"
            cards += (f'<a class="wcard" href="{wpost["url"]}">'
                      f'<span class="ph"><span class="avatar init" style="width:38px;height:38px;background:{color};font-size:14px">{init}</span>'
                      f'<span class="pn"><b>{x["name"]}</b><span>@{tw_h}</span></span>'
                      f'<span class="xmark">&#120143;</span></span>'
                      f'<span class="txt">{(wpost["text"] or "").replace("<", "&lt;")[:240]}</span>'
                      f'<span class="eng"><span>{HEART} {_n(wpost.get("likes"))}</span>'
                      f'<span>{REPLY} {_n(wpost.get("comments"))}</span>'
                      f'<span>{SHARE} {_n(wpost.get("shares"))}</span>'
                      f'<span class="wdate">{wpost["date"]}</span></span></a>')
        badge = '<a class="pjbadge" href="https://www.juicer.io/api?utm_source=political-pulse&utm_medium=referral&utm_campaign=wall-badge">powered by Juicer</a>'
        return (f'<h2>Latest posts {badge}</h2><div class="wall">{cards}</div>'
                f'<p class="na">Newest posts from their official X account, ingested by a live Juicer feed.</p>')

    for x in AUP:
        w = x.get("wiki_14d")
        color = AU_COLORS.get(x["party"], IND)
        init = "".join(n[0] for n in x["name"].split()[:2])
        body = f"""<div class="hero"><div class="who"><div class="avatar lg init" style="background:{color}">{init}</div>
<span class="nm" style="font-size:20px"><b><span class="pchip" style="background:{color}">{x["party"][:1]}</span>{x["name"]}</b>
<span>{AU_NAMES.get(x["party"], x["party"])} &middot; Australian {x["chamber"]}</span></span></div></div>
<div class="metrics" style="grid-template-columns:1fr 1fr">
<div class="metric"><div class="k">Wikipedia attention, 14 days</div><div class="v num">{fmt(w) if w is not None else "&mdash;"}</div>
<div class="d">{trend(x.get("wiki_last7"), x.get("wiki_prev7"))} week over week</div></div>
<div class="metric"><div class="k">Rank in Parliament</div><div class="v num">#{ranked_au.index(x) + 1}</div>
<div class="d">of {len(AUP)} members by attention</div></div></div>
{f'<div class="card"><b>Wikipedia attention, daily</b><br>{spark(x)}</div>' if x.get("wiki_daily") else ''}
{au_wall(x, color)}
<div style="margin-top:20px">{claim_cta(x["name"])}</div>"""
        (SITE / "p" / f"{x['slug']}.html").write_text(page(f"{x['name']}: attention tracker",
            f"Public attention profile for {x['name']}, Australian Parliament.", body, depth=1))

# ================= methodology =================
meth = f"""<div class="hero"><h1>Methodology</h1>
<p class="sub">Every number on this site comes from a public, verifiable source. Every politician is measured with identical
queries, windows and math regardless of party.</p></div>
<div class="card"><h2 style="margin-top:0">Coverage</h2>
<p><b>United States:</b> every sitting member of Congress ({len(US["people"])} members) from the public domain
unitedstates/congress-legislators dataset. <b>Australia:</b> every current member of the 48th Parliament
({len(AU["people"]) if AU else 0} members) from Wikipedia's official member lists. Nobody is included or excluded for editorial
reasons. The two 2026 spotlight race pages add news metrics for the highest-profile open Senate seats.</p>
<h2>Sources</h2>
<p><b>Wikipedia attention.</b> Wikimedia Pageviews API, user pageviews of each politician's English Wikipedia article
over 14 days. A neutral, party-agnostic proxy for public curiosity.</p>
<p><b>Bluesky.</b> Public AT Protocol appview. US accounts are counted only with a valid platform verification whose display
name matches the politician; Australian accounts come from each politician's Wikidata entry. Parody and fan accounts are
excluded, which is why many politicians correctly show as absent.</p>
<p><b>Account handles.</b> US X, Instagram, Facebook and YouTube handles come from the public domain
unitedstates/congress-legislators social media dataset. Australian X and Bluesky handles come from Wikidata.</p>
<p><b>X follower counts.</b> Retrieved through the <a href="https://developers.juicer.io/?utm_source=political-pulse">Juicer
Data API</a> profiles endpoint, exact handle matches only. Yes, the same API powers this page and is available to anyone.</p>
<p><b>News volume and tone</b> (spotlight races). GDELT DOC 2.0 API, raw article count over 28 days and average document tone.
Ambiguous names carry a disambiguating term. Tone is a linguistic measure of coverage, not public opinion.</p>
<p><b>Photos.</b> Official congressional photos from the public domain unitedstates/images collection.</p>
<h2>What this is not</h2>
<p>Attention is not support. Coverage tone is not voter sentiment. Nothing here predicts election outcomes,
and no metric is computed differently by party. Data refreshes weekly.</p>
<h2>Who built this</h2>
<p>Political Pulse is a project by <a href="https://www.juicer.io/?utm_source=political-pulse">Juicer</a>, the social feed
platform that senators, parliaments, city governments and campaigns use to show their live social media on their websites.
The pipeline is being released as open source so journalists and researchers can extend it.</p></div>"""
(SITE / "methodology.html").write_text(page("Political Pulse methodology",
    "How Political Pulse measures attention, identically for every politician.", meth))

print(f"built: index({len(US['people'])} members, {filled} attention-filled, {verified} bsky-verified) "
      f"+ 2 races + AU({len(AU['people']) if AU else 0}) + {len(list((SITE / 'p').glob('*.html')))} profiles")
