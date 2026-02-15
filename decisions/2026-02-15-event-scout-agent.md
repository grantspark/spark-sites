---
type: decision
date: 2026-02-15
status: accepted
urgency: normal
---
# Event Scout Agent — Local Event Discovery for Target Avatars

## Situation

Finding local IRL networking events where our target avatars gather requires manually searching Meetup, Facebook Events, Eventbrite, coworking space calendars, and social media. This is time-consuming and easy to neglect. As IRL networking grows, a systematic approach to event discovery becomes a competitive advantage.

The Cohatch workshop where Holtzberg found us proves this channel works. We need to find more events like it, consistently.

## Decision

Build an AI agent ("Event Scout") that scrapes event sources, filters by avatar relevance, and delivers a weekly curated digest. Start in spark-sites as a prototype with config-driven architecture so it can be extracted into a standalone product for clients later.

## Architecture

```
spark-sites/
├── agents/
│   └── event-scout/
│       ├── config.yaml        # Avatars, geography, sources, schedule
│       ├── scout.py           # Main orchestration script
│       ├── sources/           # Per-source scraper modules
│       ├── output/            # Weekly digests (markdown)
│       └── requirements.txt   # Python dependencies
```

### Config-Driven Design

The agent reads all context from config.yaml — avatars, geography, sources, schedule. The codebase is generic; the config is business-specific. When offered to clients, only the config changes.

### Technical Stack

| Layer | Tool | Rationale |
|-------|------|-----------|
| Scraping | Apify actors | Already configured. Pre-built actors for Meetup, Eventbrite, Facebook Events. No scraper maintenance. |
| Social search | Apify + web search | X/Facebook event discovery beyond structured platforms |
| AI filtering | Claude API | Score events against avatar profiles from config |
| Config | YAML | Avatars, geography, sources, schedule, output preferences |
| Output | Markdown + email (future) | Markdown commits to repo. Email via SMTP or Resend later. |
| Scheduling | GitHub Actions or Apify scheduler | Runs weekly (Thursdays default), no server needed |

### Data Flow

```
Config (avatars + geography)
    ↓
Scrape (Apify actors per source)
    ↓
Normalize (common event schema)
    ↓
Filter + Score (Claude API vs avatar profiles)
    ↓
Rank + Deduplicate
    ↓
Output (markdown digest + optional email)
```

## Scope — MVP (v1)

1. Scrape Meetup + Eventbrite + Facebook Events for Lakeland/Tampa/Orlando/Winter Haven
2. Filter with Claude API against 4 audience segments (Local Business Owner, Growing Entrepreneur, Female Founder, Event Host)
3. Score and rank by avatar relevance (high/medium/low)
4. Output weekly markdown digest every Thursday
5. Email digest deferred to v2

## Geography

- Primary: Lakeland, FL
- Expanded: ~100 mile radius — Tampa, Orlando, Winter Haven
- Configurable per user/client

## Users

- Grant, Nicole, Amber (internal team)
- Future: standalone agent offered to clients (config swap, same engine)

## Repo Strategy

Lives in spark-sites/agents/event-scout/ for now. Architected for extraction into its own repo when productized. The config.yaml is the only business-specific file — everything else is generic.

## What Changes

- New directory: `agents/event-scout/` in spark-sites
- No changes to existing reference files
- Future: may inform content-strategy.md (events as a content pillar)
