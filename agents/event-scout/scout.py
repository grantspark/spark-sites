#!/usr/bin/env python3
"""
Event Scout — Local event discovery agent for target avatars.

Scrapes Meetup, Eventbrite, Lu.ma, and Facebook Events,
then uses AI to score events against your target audience profiles.

Usage:
    python scout.py                    # Run with default config
    python scout.py --config my.yaml   # Run with custom config
    python scout.py --dry-run          # Show what would be searched (no API calls)
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import yaml
from apify_client import ApifyClient
from dateutil import parser as dateparser


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

def load_config(config_path: str = None) -> dict:
    """Load configuration from YAML file."""
    if config_path is None:
        config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def get_date_range() -> tuple[str, str]:
    """Return (start_date, end_date) for next 2 weeks."""
    today = datetime.now()
    end = today + timedelta(days=14)
    return today.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# Source: Event Scraper Pro (Meetup + Eventbrite + Lu.ma)
# ---------------------------------------------------------------------------

def scrape_event_scraper_pro(client: ApifyClient, config: dict) -> list[dict]:
    """Scrape events from Meetup, Eventbrite, and Lu.ma via Event Scraper Pro."""
    source_config = config["sources"]["event_scraper_pro"]
    if not source_config.get("enabled", True):
        return []

    date_from, date_to = get_date_range()
    cities = config["location"]["cities"]

    actor_input = {
        "keywords": source_config["search_keywords"],
        "country": config["location"]["country"],
        "cities": cities,
        "platforms": source_config["platforms"],
        "dateFrom": date_from,
        "dateTo": date_to,
        "includeOnline": source_config.get("include_online", False),
        "includeFree": True,
        "includePaid": True,
        "maxItemsPerPlatform": source_config.get("max_results_per_platform", 50),
        "useApifyProxy": True,
    }

    print(f"  Scraping Meetup/Eventbrite/Lu.ma for {', '.join(cities)}...")
    run = client.actor(source_config["actor"]).call(
        run_input=actor_input,
        timeout_secs=180,
    )
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    print(f"  Found {len(items)} events from Event Scraper Pro")
    return items


def scrape_facebook_events(client: ApifyClient, config: dict) -> list[dict]:
    """Scrape events from Facebook Events."""
    source_config = config["sources"]["facebook_events"]
    if not source_config.get("enabled", True):
        return []

    actor_input = {
        "searchQueries": source_config["search_queries"],
        "maxEvents": source_config.get("max_events", 50),
    }

    print(f"  Scraping Facebook Events...")
    # Timeout after 3 minutes — Facebook scraper paginates aggressively
    run = client.actor(source_config["actor"]).call(
        run_input=actor_input,
        timeout_secs=180,
    )
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    print(f"  Found {len(items)} events from Facebook")
    return items


# ---------------------------------------------------------------------------
# Normalize events to common schema
# ---------------------------------------------------------------------------

def normalize_event(raw: dict, source: str) -> dict:
    """Normalize a raw event from any source into a common schema."""
    if source == "event_scraper_pro":
        return {
            "title": raw.get("title") or raw.get("name", "Untitled"),
            "description": raw.get("description", ""),
            "date": raw.get("date") or raw.get("startDate", ""),
            "time": raw.get("time") or raw.get("startTime", ""),
            "location": raw.get("location") or raw.get("venue", ""),
            "city": raw.get("city", ""),
            "url": raw.get("url") or raw.get("link", ""),
            "organizer": raw.get("organizer") or raw.get("group", ""),
            "attendees": raw.get("attendees") or raw.get("rsvpCount", 0),
            "price": raw.get("price", "Free"),
            "platform": raw.get("platform") or raw.get("source", source),
            "source": source,
        }
    elif source == "facebook":
        return {
            "title": raw.get("name") or raw.get("title", "Untitled"),
            "description": raw.get("description", ""),
            "date": raw.get("startDate") or raw.get("date", ""),
            "time": raw.get("startTime") or raw.get("time", ""),
            "location": raw.get("location") or raw.get("place", {}).get("name", ""),
            "city": raw.get("city", ""),
            "url": raw.get("url", ""),
            "organizer": raw.get("organizer", {}).get("name", "") if isinstance(raw.get("organizer"), dict) else raw.get("organizer", ""),
            "attendees": raw.get("usersInterested", 0) or raw.get("usersGoing", 0),
            "price": raw.get("price", "See event"),
            "platform": "Facebook",
            "source": "facebook",
        }
    return raw


# ---------------------------------------------------------------------------
# AI Scoring — Score events against avatar profiles
# ---------------------------------------------------------------------------

def score_events_with_ai(events: list[dict], config: dict) -> list[dict]:
    """Use Gemini to score each event's relevance to target avatars."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("  WARNING: GOOGLE_API_KEY not set. Skipping AI scoring.")
        for event in events:
            event["score"] = "unscored"
            event["avatar_match"] = []
            event["reasoning"] = "AI scoring unavailable"
        return events

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    # Build avatar context for the prompt
    avatar_descriptions = []
    for name, avatar in config["avatars"].items():
        avatar_descriptions.append(f"- **{name}**: {avatar['description']}")
    avatar_context = "\n".join(avatar_descriptions)

    # Batch events into groups of 10 for efficiency
    scored_events = []
    batch_size = 10

    for i in range(0, len(events), batch_size):
        batch = events[i : i + batch_size]
        events_text = ""
        for j, event in enumerate(batch):
            events_text += f"\n[Event {j+1}]\n"
            events_text += f"Title: {event['title']}\n"
            events_text += f"Description: {(event['description'] or '')[:500]}\n"
            events_text += f"Location: {event['location']}\n"
            events_text += f"Organizer: {event['organizer']}\n"

        prompt = f"""You are an event relevance scorer for a local web design and marketing company called Spark Sites, based in Lakeland, FL.

Score each event below for how likely our TARGET AVATARS would attend. We want to find events where we can network with potential clients.

TARGET AVATARS:
{avatar_context}

EVENTS TO SCORE:
{events_text}

For EACH event, respond with a JSON array. Each item must have:
- "index": the event number (1-based)
- "score": "high", "medium", or "low"
- "avatar_match": array of matching avatar names (e.g., ["local_business_owner", "growing_entrepreneur"])
- "reasoning": one sentence explaining the score

Score "high" if the event is SPECIFICALLY for our avatars (business networking, entrepreneur meetups, small business workshops).
Score "medium" if our avatars MIGHT attend (general professional events, community gatherings, coworking events).
Score "low" if it's unlikely (purely social, niche hobby, corporate-only).

Return ONLY the JSON array, no other text."""

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    response_mime_type="application/json",
                ),
            )

            text = response.text.strip()
            # Parse JSON response
            scores = json.loads(text)

            for score_item in scores:
                idx = score_item["index"] - 1
                if 0 <= idx < len(batch):
                    batch[idx]["score"] = score_item.get("score", "low")
                    batch[idx]["avatar_match"] = score_item.get("avatar_match", [])
                    batch[idx]["reasoning"] = score_item.get("reasoning", "")

        except Exception as e:
            print(f"  WARNING: AI scoring failed for batch: {e}")
            for event in batch:
                event.setdefault("score", "unscored")
                event.setdefault("avatar_match", [])
                event.setdefault("reasoning", "Scoring failed")

        scored_events.extend(batch)
        print(f"  Scored {min(i + batch_size, len(events))}/{len(events)} events...")

    return scored_events


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def deduplicate(events: list[dict]) -> list[dict]:
    """Remove duplicate events based on title + date similarity."""
    seen = set()
    unique = []
    for event in events:
        # Normalize key: lowercase title + date prefix
        key = (event["title"].lower().strip(), str(event["date"])[:10])
        if key not in seen:
            seen.add(key)
            unique.append(event)
    print(f"  Deduplicated: {len(events)} -> {len(unique)} unique events")
    return unique


# ---------------------------------------------------------------------------
# Markdown Digest Generation
# ---------------------------------------------------------------------------

def generate_digest(events: list[dict], config: dict) -> str:
    """Generate a markdown digest of scored events (high + medium only)."""
    today = datetime.now().strftime("%Y-%m-%d")
    date_from, date_to = get_date_range()

    # Sort: high first, then medium
    score_order = {"high": 0, "medium": 1}
    high = [e for e in events if e.get("score") == "high"]
    medium = [e for e in events if e.get("score") == "medium"]
    kept = high + medium
    dropped = len(events) - len(kept)

    lines = [
        f"---",
        f"type: digest",
        f"date: {today}",
        f"agent: event-scout",
        f"status: active",
        f"---",
        f"",
        f"# Event Scout Digest — {today}",
        f"",
        f"**Business:** {config['business_name']}",
        f"**Geography:** {', '.join(config['location']['cities'])}",
        f"**Date range:** {date_from} to {date_to}",
        f"**Events:** {len(kept)} relevant ({len(high)} high, {len(medium)} medium) — {dropped} low-relevance filtered out",
        f"",
    ]

    if high:
        lines.append("---")
        lines.append("")
        lines.append("## High Relevance — Go to These")
        lines.append("")
        for event in high:
            lines.extend(_format_event(event))

    if medium:
        lines.append("---")
        lines.append("")
        lines.append("## Medium Relevance — Worth Considering")
        lines.append("")
        for event in medium:
            lines.extend(_format_event(event))

    if not kept:
        lines.append("---")
        lines.append("")
        lines.append("*No high or medium relevance events found this week.*")
        lines.append("")

    return "\n".join(lines)


def _format_event(event: dict) -> list[str]:
    """Format a single event for the digest (detailed)."""
    lines = [
        f"### {event['title']}",
        f"",
        f"- **Date:** {event.get('date', 'TBD')} {event.get('time', '')}".strip(),
        f"- **Location:** {event.get('location', 'TBD')}",
        f"- **Platform:** {event.get('platform', 'Unknown')}",
        f"- **Attendees:** {event.get('attendees', 'N/A')}",
        f"- **Price:** {event.get('price', 'See event')}",
        f"- **Organizer:** {event.get('organizer', 'Unknown')}",
        f"- **Avatar match:** {', '.join(event.get('avatar_match', []))}",
        f"- **Why:** {event.get('reasoning', '')}",
    ]
    if event.get("url"):
        lines.append(f"- **Link:** {event['url']}")
    lines.append("")
    desc = event.get("description", "")
    if desc:
        lines.append(f"> {desc[:300]}{'...' if len(desc) > 300 else ''}")
        lines.append("")
    return lines



# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Event Scout — Local event discovery agent")
    parser.add_argument("--config", type=str, help="Path to config YAML file")
    parser.add_argument("--dry-run", action="store_true", help="Show config without making API calls")
    args = parser.parse_args()

    print("=" * 60)
    print("EVENT SCOUT — Local Event Discovery Agent")
    print("=" * 60)

    # Load config
    config = load_config(args.config)
    print(f"\nBusiness: {config['business_name']}")
    print(f"Cities: {', '.join(config['location']['cities'])}")
    print(f"Avatars: {', '.join(config['avatars'].keys())}")

    if args.dry_run:
        print("\n[DRY RUN] Would search:")
        for source_name, source_config in config["sources"].items():
            if source_config.get("enabled", True):
                print(f"  - {source_name} ({source_config['actor']})")
        print("\nNo API calls made.")
        return

    # Check API keys
    apify_token = os.environ.get("APIFY_API_TOKEN")
    if not apify_token:
        # Try loading from vip env
        env_path = os.path.expanduser("~/.config/vip/env.sh")
        if os.path.exists(env_path):
            print("  Loading API keys from ~/.config/vip/env.sh...")
            import subprocess
            result = subprocess.run(
                ["bash", "-c", f"source {env_path} && echo $APIFY_API_TOKEN"],
                capture_output=True, text=True
            )
            apify_token = result.stdout.strip()
            os.environ["APIFY_API_TOKEN"] = apify_token

            # Also load GOOGLE_API_KEY if not set
            if not os.environ.get("GOOGLE_API_KEY"):
                result = subprocess.run(
                    ["bash", "-c", f"source {env_path} && echo $GOOGLE_API_KEY"],
                    capture_output=True, text=True
                )
                google_key = result.stdout.strip()
                if google_key:
                    os.environ["GOOGLE_API_KEY"] = google_key

    if not apify_token:
        print("\nERROR: APIFY_API_TOKEN not found.")
        print("Set it as an environment variable or add it to ~/.config/vip/env.sh")
        print("Get your token at: https://console.apify.com/account/integrations")
        sys.exit(1)

    client = ApifyClient(apify_token)

    # --- Scrape all sources ---
    print("\n[1/4] Scraping event sources...")
    all_raw_events = []

    # Event Scraper Pro (Meetup + Eventbrite + Lu.ma)
    try:
        esp_events = scrape_event_scraper_pro(client, config)
        all_raw_events.extend(
            [normalize_event(e, "event_scraper_pro") for e in esp_events]
        )
    except Exception as e:
        print(f"  ERROR with Event Scraper Pro: {e}")

    # Facebook Events
    try:
        fb_events = scrape_facebook_events(client, config)
        all_raw_events.extend(
            [normalize_event(e, "facebook") for e in fb_events]
        )
    except Exception as e:
        print(f"  ERROR with Facebook Events: {e}")

    print(f"\n  Total raw events: {len(all_raw_events)}")

    # --- Deduplicate ---
    print("\n[2/4] Deduplicating...")
    unique_events = deduplicate(all_raw_events)

    # --- AI Score ---
    print("\n[3/4] Scoring events against target avatars...")
    scored_events = score_events_with_ai(unique_events, config)

    # --- Generate digest ---
    print("\n[4/4] Generating digest...")
    digest = generate_digest(scored_events, config)

    # Save markdown — single file, overwritten each week (Zapier/N8N watches this)
    output_dir = Path(__file__).parent / config["output"]["markdown_path"].replace("agents/event-scout/", "")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "digest-latest.md"
    output_path.write_text(digest, encoding="utf-8")

    print(f"\n{'=' * 60}")
    print(f"DONE! Digest saved to: {output_path}")

    high_count = len([e for e in scored_events if e.get("score") == "high"])
    med_count = len([e for e in scored_events if e.get("score") == "medium"])
    print(f"  {high_count} high-relevance events (go to these!)")
    print(f"  {med_count} medium-relevance events (worth considering)")
    print(f"  {len(scored_events) - high_count - med_count} low-relevance events")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
