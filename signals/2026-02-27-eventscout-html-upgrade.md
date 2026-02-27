---
type: signal
status: active
date: 2026-02-27
topics: [eventscout, email, html, design]
---
# EventScout HTML Email Upgrade

## What Changed
- Replaced plain markdown-to-HTML converter in `agents/event-scout/scout.py` with fully styled HTML email builder
- Matches visual style of Grant Daily and BizDev Daily emails

## New Email Format
- **Green gradient header** with event counts and city list
- **3 stat boxes:** New Events count, Score 7+ count, Top Score
- **Event cards:** Color-coded score badges (green 8+, yellow 6-7, gray below), rank circles, AI reasoning, detail grids (date, location, organizer, attendees, price, platform, best-for avatars)
- **3 sections:** New Events, Also on Your Radar (previously seen), Worth Watching
- **Styled footer** with run schedule info
- Markdown digest still attached as plaintext fallback

## Technical
- New functions: `build_digest_html_()`, `_stat_box_()`, `_event_card_html_()`
- `send_digest_email()` signature updated to accept event lists (new, seen, worth_watching)
- Uses Python `html.escape()` for XSS-safe output
- `main()` updated to pass event lists to email function

## Takes Effect
Next GitHub Actions run (Wed or Fri at 8am ET), or manual trigger from Actions tab.
