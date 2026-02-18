# Lead Gen Agent — SKILL.md

Finds prospect businesses in Polk County with weak or missing digital presence.
Outputs 5 qualified leads to a markdown file for user review before any CRM action.

---

## Trigger

User says: `run leads`, `find leads`, `lead gen`, `pull prospects`

---

## Configuration

Edit these values to change geography, industries, or output behavior.
Duplicate this file for a new client — swap the config, run it.

```yaml
geography:
  county: Polk
  state: Florida
  country_code: us
  cities: [Lakeland, Winter Haven, Plant City, Polk City, Bartow, Auburndale]

industries:
  - home services
  - chiropractor
  - beauty salon

signals:
  - no_website       # Google Business has no website listed
  - outdated_website # Footer copyright year is behind current year
  - no_socials       # Website has no social media links

output:
  leads_per_run: 5
  markdown_path: research/leads/YYYY-MM-DD-leads.md
  clickup_list: Spark Sites Sales
  clickup_status: prospect
  trigger: manual
```

---

## Workflow

### Step 1 — Pass 1: No-Website Leads (cheap, run first)

Call Apify actor `lukaskrivka/google-maps-with-contact-details` once per industry.
Run all three in parallel.

**Input for each call:**
```json
{
  "searchStringsArray": ["[industry]"],
  "county": "Polk",
  "state": "Florida",
  "countryCode": "us",
  "website": "withoutWebsite",
  "maxCrawledPlacesPerSearch": 20,
  "skipClosedPlaces": true,
  "language": "en"
}
```

Replace `[industry]` with each industry from config: `home services`, `chiropractor`, `beauty salon`.

**What comes back:** Business name, address, phone, category. No website = instant qualified lead.

Collect all results. Deduplicate by business name. Tag each with signal: `no_website`.

---

### Step 2 — Do We Have 5?

Count unique leads from Pass 1.

- **5 or more** → Skip to Step 4. Take the top 5 (prioritize most recently updated listings).
- **Fewer than 5** → Proceed to Step 3 to fill remaining slots.

---

### Step 3 — Pass 2: Website Checks (only if needed)

Run the actor again per industry with `website: "withWebsite"`. Limit to 10 results per industry.

For each business returned, fetch the homepage using `apify/rag-web-browser` with this prompt:

> "Find two things only: (1) the copyright year in the footer, (2) any links to Facebook, Instagram, Twitter, LinkedIn, TikTok, or YouTube. Return nothing else."

**Signal logic:**
- Copyright year < current year → signal: `outdated_website`
- No social links found → signal: `no_socials`
- Both → tag both signals

Add qualifying businesses to the lead pool until we reach 5 total.

---

### Step 4 — Format Leads into Markdown

Create file at `research/leads/YYYY-MM-DD-leads.md` (use today's date).

**File format:**

```markdown
---
date: YYYY-MM-DD
run: manual
leads: 5
industries: home services, chiropractor, beauty salon
geography: Polk County, FL
---

# Leads — YYYY-MM-DD

5 prospects found. Review each and mark approve/reject before pushing to ClickUp.

---

## 1. [Business Name]
- **Category:** [Google Maps category]
- **Signal:** [no_website | outdated_website | no_socials]
- **Address:** [full address]
- **Phone:** [phone]
- **Website:** [URL or None]
- **Socials:** [links or None]
- **Maps:** [Google Maps URL]
- **Status:** [ ] approve / [ ] reject

---

## 2. [Business Name]
...
```

Repeat for all 5 leads.

---

### Step 5 — Present to User

Display a summary in chat:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LEADS — [date] — Polk County, FL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [Business Name] — [category] — [signal]
2. [Business Name] — [category] — [signal]
3. [Business Name] — [category] — [signal]
4. [Business Name] — [category] — [signal]
5. [Business Name] — [category] — [signal]

Full details saved to: research/leads/YYYY-MM-DD-leads.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Which leads do you want to push to ClickUp?
(Say "push all", "push 1 3 5", or "reject all")
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Wait for user response before proceeding.

---

### Step 6 — Push Approved Leads to ClickUp

For each approved lead, create a ClickUp task:

```
Tool: clickup_create_task
List: Spark Sites Sales (ID: 33882537)
Status: prospect
Name: [Business Name] — [City]
Assignees: [10521914]  # Grant
Due date: today + 3 days
Description:
  Category: [category]
  Signal: [signal]
  Phone: [phone]
  Website: [URL or None]
  Socials: [links or None]
  Maps: [Google Maps URL]
```

After all tasks are created, confirm in chat:

> "Done. X tasks created in Spark Sites Sales → prospect. Ready to run again or call it for today?"

---

## Error Handling

- **Apify returns 0 results for an industry** — skip that industry, note it in the markdown header, continue with others.
- **Pass 1 returns fewer than 5 across all industries** — run Pass 2 automatically, note in markdown that Pass 2 was used.
- **Website fetch fails** — skip that business, move to next candidate.
- **ClickUp push fails** — report the failure, leave the lead in the markdown file for manual entry.

---

## Notes

- Never auto-push to ClickUp. Always wait for user confirmation.
- Run Pass 2 only if Pass 1 doesn't fill the 5-lead quota.
- The markdown file is the source of truth — it stays even after ClickUp tasks are created.
- This skill is designed to be duplicated for clients. Change the config block only.
