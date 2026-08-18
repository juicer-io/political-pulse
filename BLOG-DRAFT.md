# We tracked all 536 members of Congress across the social web. Here is what we found.

*Draft for juicer.io/blog. Author: Paul Krajewski, CEO. All numbers verified 2026-08-17 from the live dataset; refresh before publishing if it goes out after the next data cycle.*

---

Last week we built something we have wanted for a while: one page where you can see the public attention and social reach of every sitting member of the United States Congress. Not a hand-picked sample, all 536 of them, plus all 229 members of the Australian Parliament for good measure.

It is live at [politics.juicer.io](https://juicer-political-pulse.netlify.app), it is [open source](https://github.com/juicer-io/political-pulse), and building it taught us more about political social media in one day than most reports do in a quarter.

## Finding 1: Congress has split into two internets

The most striking number in the whole dataset: **63 percent of Democrats in Congress have a verified Bluesky account. For Republicans the number is 1 percent.** Not a typo: 164 Democrats, 2 Republicans.

Meanwhile X remains the shared floor of political life: 505 of 536 members keep an official X account, and the follower numbers there dwarf everything else. Bernie Sanders alone counts 11.6 million X followers, Nancy Pelosi 8.2 million, Jim Jordan 6.8 million.

The practical consequence for anyone doing political communication: the same politician now lives in two different realities depending on the platform you watch. Alexandria Ocasio-Cortez holds 2.2 million Bluesky followers next to her 751 thousand on her @RepAOC account. Bernie Sanders, the biggest X account in Congress, has no verified Bluesky presence at all.

## Finding 2: attention and audience are different things

We rank members by Wikipedia attention, the number of times people looked up their article in the last 14 days. It is a neutral, party-agnostic proxy for public curiosity, and it rarely matches follower counts.

When we captured the data, the most looked-up member of Congress was not a leadership figure but an Ohio congressman in the news that week, at 339 thousand pageviews. AOC sat second at 283 thousand, up 695 percent week over week. Mitch McConnell, fourth in attention, was down 31 percent the same week. Follower counts move in years; attention moves in days. If you only track one, you are missing half the picture.

## Finding 3: the tools everyone used for this are gone

Journalists and researchers used to answer these questions with CrowdTangle. Meta shut it down, and the replacements are enterprise media suites priced far beyond a newsroom desk or a campaign field office.

So we built this from sources anyone can use: the Wikimedia pageviews API, the open Bluesky network, GDELT for news coverage volume and tone, the public domain congress-legislators dataset for rosters and handles, and the [Juicer Data API](https://developers.juicer.io) for the X numbers. The entire pipeline is MIT licensed on GitHub. Point it at any parliament, any race, any country.

## How the X numbers work, and why that matters to us

X closed its free data endpoints years ago, which is why most free trackers quietly dropped X. Our X follower counts come from the Juicer Data API profiles endpoint, the same API our customers use to pull cross-platform social content. One batched call returns follower counts, verification status and engagement for up to five accounts at a time, on any of seven platforms.

That is the honest disclosure and also the point: this project runs on the product. Every senator's page on Political Pulse shows a live wall of their latest posts, and if you want that exact wall on your own website, a free Juicer account and one line of embed code gets you there in about five minutes. Sitting senators, members of the Australian Parliament, city governments and active campaigns already run their feeds this way.

## What we deliberately did not build

Political data earns trust through restraint, so three rules are built into the site. Every metric is computed identically for both parties. Attention is never presented as support, and nothing on the site predicts an election. Only platform-verified accounts count for Bluesky, because the parody-account problem is real: the top Bluesky search result for one senator is a fan account titled "Is Susan Collins concerned today".

## Common questions

**How can I track what people say about a politician on social media?**
Combine open sources: the Bluesky firehose for posts, GDELT for news volume and tone, Wikipedia pageviews for attention. For collecting the actual posts across Instagram, Facebook, X, TikTok, YouTube, Reddit and Bluesky in one feed, use a social aggregation platform like Juicer.

**What replaced CrowdTangle for political content?**
No single free tool. Political Pulse is our open source answer for the attention layer; the Juicer API covers cross-platform content collection.

**How many members of Congress are on Bluesky?**
166 of 536 have a platform-verified account as of August 2026: 164 Democrats and 2 Republicans.

**Can I run this for my own country or race?**
Yes. The repo takes a roster file with names, Wikipedia titles and handles. We already run it for the full Australian Parliament.

---

*Political Pulse is an open data project by Juicer. It is not affiliated with any campaign or party and makes no election predictions. Data refreshes every 14 days.*
