---
type: output
subtype: internal-notes
date: 2026-02-17
client: S&D Real Estate
status: approved
---

# Internal Notes: S&D Real Estate — Lead Capture Pages

**DO NOT SEND TO CLIENT**

---

## Labor Estimate

| Service | Est. Hours | Rate | Internal Cost |
|---------|-----------|------|---------------|
| Option A — 5 manual pages + FUB integration | ~6 hrs | Flat rate | $500 |
| Option B — Agent CPT + auto-generation system | ~10 hrs | Flat rate | $900 |

---

## Technical Notes

- FUB API endpoint: POST /v1/events (not /people) for lead ingestion
- Auth: HTTP Basic with API key — must be server-side proxy, never expose key in browser
- Agent routing: Use assignedTo field in FUB API to auto-assign leads
- URL structure: Path-based (yoursite.com/agents/kristina) — NOT subdomains
- Ylopo context: Client previously had Ylopo which auto-generated agent subdomain pages. Option B replicates this behavior using WordPress Agent CPT with a checkbox toggle.
- FUB does NOT build landing pages — it's CRM only. Custom WordPress build is the right approach.
- Flywheel hosting: No .htaccess (Nginx), no wildcard SSL. Subdomain vanity URLs would require Cloudflare in front for wildcard SSL + redirect rules. Quote separately as Phase 2.

---

## Assumptions

- S&D has an existing WordPress site on Flywheel
- FUB account is active and API access available
- Starting with 5 agents (Kristina, Dee, + 3 others)
- 2FA access from Kristina still needed (noted in task comments)

---

## Upsell Strategy

- Highest close probability: Option B — "works like Ylopo did" framing
- Vanity subdomain URLs as Phase 2 add-on once pages are live
- Future: Local SEO ($900), Google Ads ($350 setup + $350/mo), GBP ($150)
