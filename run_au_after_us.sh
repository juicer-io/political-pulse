#!/usr/bin/env bash
# waits for the US rotation to finish, then runs the AU rotation
while pgrep -f "fetch_posts_x_feed.py --rotate" > /dev/null; do sleep 60; done
cd "$(dirname "$0")"
exec ~/Desktop/Rubbish/juicer-video-builds/tiktok-source/.venv/bin/python fetch_posts_x_feed_au.py --rotate
