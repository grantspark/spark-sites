---
type: decision
status: accepted
date: 2026-02-18
---

# Lead Gen Agent — Parameters

Design parameters for the Spark Sites prospect scraping agent.
Built to be configurable — duplicate and swap params for client use.

---

## Geography

**Region:** Polk County, FL

**Cities:**
- Lakeland
- Winter Haven
- Plant City
- Polk City
- Bartow
- Auburndale

---

## Industries

- Home services
- Chiropractic care
- Beauty salons

---

## Prospect Signals (Fit Criteria)

A business is a prospect if it matches one or more of:

1. **No website** — Google Business listing has no website listed
2. **Outdated website** — footer copyright year is behind current year
3. **No socials** — website has no links to social media profiles

---

## Output Pipeline

1. **Leads land in a markdown file** — presented to user for review
2. **Verification step** — user approves/rejects each lead before it moves
3. **ClickUp task creation** — one task per approved lead, pushed to Sales list
4. **Email** — future phase, not built yet

---

## Design Principles

- Parameters are top-of-file config — easy to swap for new geography, industry, or signals
- Duplicatable for client use — give a client a copy, change the config, run it for them
- Human in the loop before any CRM action — leads are never auto-pushed

---

## Resolved Configuration

| Parameter | Value |
|-----------|-------|
| Leads per run | 5 (quality check phase) |
| Run trigger | Manual for now — scheduled after testing confirms quality |
| Markdown location | `research/leads/YYYY-MM-DD-leads.md` |
| ClickUp destination | Spark Sites Sales list, status: `prospect` |

---

## Token Efficiency Notes

- Pull more raw results from Google Maps (20–30), filter down to 5 qualifying leads
- Filtering happens on structured data (no website, footer year, socials) — not full page reads
- Only fetch website content for businesses that have a website listed
- Goal: qualify leads cheaply, summarize expensively only for the final 5

---

## Phases

| Phase | Trigger | Status |
|-------|---------|--------|
| 1 — Manual test | User-triggered | Build this first |
| 2 — Scheduled | Cron/interval | After quality confirmed |
| 3 — Email delivery | TBD | Future |
