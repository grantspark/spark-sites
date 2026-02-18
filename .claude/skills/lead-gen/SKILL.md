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

Create all approved tasks in parallel. For each approved lead:

**Task fields:**
```
Tool: clickup_create_task
List: Spark Sites Sales (ID: 33882537)
Status: prospect
Name: [Business Name] — [City]
Assignees: [10521914, 42473908]  # Grant + Nicole
Due date: today
Priority: urgent
Custom fields:
  - 02.Primary Phone (effdc2a0-6373-4e15-8d57-d0963276ef64): [phone in E.164 format, e.g. +18636661199]
  - Email 3 (f4a70b34-655d-4a35-b16d-9f09b2760a0c): grant@stateofthespark.com
  - Email 4 (74409a59-4466-4692-8a5a-4319c0f853d5): nicole@sparkmysite.com
```

**After all tasks are created, add a comment to each:**
```
Tool: clickup_create_task_comment
Comment: "Next step: call this lead - [phone formatted as (XXX) XXX-XXXX]"
```

Run all comment calls in parallel after tasks are created.

After all tasks and comments are done, confirm in chat:

> "Done. X tasks created in Spark Sites Sales → prospect. Ready to run again or call it for today?"

---

### Step 7 — Codex Check (runs automatically before every demo site build)

Before generating any demo site, check whether the lead's industry has a design codex.

**Codex location:** `spark-sites/reference/design/industry-codex/`

**Currently profiled industries:**
- `home-services.md` — contractor, handyman, HVAC, plumbing, cleaning, repair
- `chiropractor.md` — chiropractic care, spinal, wellness
- `beauty-salon.md` — hair salon, nail salon, boutique salon

**Logic:**

```
1. Map the lead's Google Maps category to the nearest codex industry.
   Examples:
     "Contractor" → home-services.md
     "Handyman" → home-services.md
     "Chiropractor" → chiropractor.md
     "Hair salon" → beauty-salon.md
     "Nail salon" → beauty-salon.md
     "Beauty salon" → beauty-salon.md

2. If a matching codex file exists:
   → Read it. Proceed to Step 8 (demo site build) using its palette and typography.

3. If NO matching codex file exists:
   → Run the industry design research workflow below.
   → Write the new codex file.
   → Then proceed to Step 8.
```

**Research workflow for a new industry:**

Run all three searches in parallel:

```
Search 1: "best [industry] website design examples 2025"
Search 2: "[industry] website color palette hex codes"
Search 3: "[industry] website fonts typography"
```

Then fetch 3–4 top-ranked live websites from the results and extract:
- Dominant colors with hex codes
- Accent colors / CTA colors
- Colors to avoid
- Display/heading fonts (named)
- Body fonts (named)
- Photography style and subjects
- Hero layout pattern
- Standard section order
- Trust signals used
- Tone words

Write the new codex file to:
```
spark-sites/reference/design/industry-codex/[industry-slug].md
```

Follow the exact structure of the existing codex files (see `home-services.md` as the template). Include:
- Colors section with palette families
- Typography section with pairings
- Photography section
- Layout conventions
- Tone and feel
- v0 prompt template at the bottom
- Credibility checklist

Add a row to `spark-sites/reference/design/industry-codex/README.md`.

Commit the new codex file before proceeding:
```
git add reference/design/industry-codex/
git commit -m "[add] Design codex — [industry]"
```

Confirm in chat:
> "No codex found for [industry]. Researched and wrote [industry-slug].md. Proceeding with demo site build."

---

### Step 8 — Build Demo Site (triggered on request)

User says: `build site for lead X`, `build demo for [business]`, or `build site`

**Do not run automatically.** Wait for user to request a demo site for a specific lead.

**Approach:** v0.dev — generates a unique, photo-first Next.js site from a detailed prompt.
No template ceiling. Each site looks custom and industry-appropriate.

---

#### 8a — Assemble the v0 prompt

Using data from the lead's markdown entry + the industry codex from Step 7, populate and output the complete v0 prompt template from the codex file.

Fill every bracket with real lead data:
- `[Business Name]` → from lead markdown
- `[City]` → from lead address
- `[Headline]` → craft from business positioning and codex tone guidelines
- `[Value prop]` → 1-2 sentences, outcome-focused, using codex tone words
- `[(XXX) XXX-XXXX]` → lead phone number
- `[X]+ Years / Customers / Rating` → research from Google Maps listing if available; use plausible defaults if not
- Services list → infer 4-6 from Google Maps category, match to codex photo search terms

Present the filled prompt to the user before proceeding. Say:
> "Here's the v0 prompt for [Business Name]. Ready to generate?"

---

#### 8b — Generate the site via v0

**Client slug format:** lowercase, hyphens, no spaces. Example: `paragon-home-services`

**API path (preferred):**

Read the key from Windows user env (works without restarting the session):

```powershell
$key = [System.Environment]::GetEnvironmentVariable('V0_API_KEY', 'User')
```

Write the assembled prompt to a temp file to avoid JSON escaping issues:

```powershell
# Save prompt to temp file
Set-Content -Path "$env:TEMP\v0-prompt.txt" -Value @"
[PASTE ASSEMBLED PROMPT HERE]
"@

# Build request body
$prompt = Get-Content "$env:TEMP\v0-prompt.txt" -Raw
$body = @{ model = "v0-1.5-md"; messages = @(@{ role = "user"; content = $prompt }) } | ConvertTo-Json -Depth 5

# Call v0 API
$response = Invoke-RestMethod `
  -Uri "https://api.v0.dev/v1/chat/completions" `
  -Method POST `
  -Headers @{ Authorization = "Bearer $key"; "Content-Type" = "application/json" } `
  -Body $body

# Save response content to file for Claude to parse
$response.choices[0].message.content | Set-Content "$env:TEMP\v0-output.md"
Write-Host "Response saved to $env:TEMP\v0-output.md"
```

After the API call, Claude reads `$env:TEMP\v0-output.md` and extracts the code blocks into files at `C:/Users/grant/OneDrive/Documents/GitHub/[client-slug]/`. Each code block is prefixed with its file path (e.g. `// app/page.tsx`). Claude creates the directories and writes each file.

**Manual path (fallback — no API key or API issues):**
1. Copy the filled prompt from 8a
2. Go to https://v0.dev
3. Paste the prompt → generate
4. Click **Code** → **Download** → extract zip to `C:/Users/grant/OneDrive/Documents/GitHub/[client-slug]/`

---

#### 8c — Initialize repo and push to GitHub

```bash
cd C:/Users/grant/OneDrive/Documents/GitHub/[client-slug]

# Ensure next.config has static export
# Verify: output: 'export' is set in next.config.ts

git init
git checkout -b main
git add .
git commit -m "[add] [Business Name] demo site — generated via v0"

gh repo create grantspark/[client-slug] --private --source=. --push
```

---

#### 8d — Deploy to Netlify (fully automated via CLI)

**Prerequisites:** Netlify CLI installed (`npm install -g netlify-cli`) and authenticated (`netlify login`). Account slug: `grant-plw4ylu`.

```bash
# 1. Create the Netlify site (non-interactive — avoids Windows prompt bug)
netlify api createSite --data '{"body": {"name": "[client-slug]", "account_slug": "grant-plw4ylu"}}'
# → Copy the site ID from the response (e.g. c82ede9b-...)

# 2. Build
cd C:/Users/grant/OneDrive/Documents/GitHub/[client-slug]
pnpm install
pnpm build

# 3. Deploy — use site ID, NOT site name (name lookup fails on Windows)
netlify deploy --prod --dir=out --site [site-id]
```

**Note:** `netlify sites:create` crashes on Windows with "unsettled top-level await". Always use `netlify api createSite`. Always pass the site ID to `--site`, not the name.

Netlify assigns URL: `https://[client-slug].netlify.app`

After deploy, confirm in chat:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEMO SITE — [Business Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Live at: https://[slug].netlify.app
GitHub:  https://github.com/grantspark/[client-slug]

Sections: Hero / Services / CTA / Form
Phone CTA: [(XXX) XXX-XXXX]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ready to call. Pull up the URL before you dial.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Update the ClickUp task for this lead with the demo URL in a comment:
```
Tool: clickup_create_task_comment
Comment: "Demo site live: [URL] — ready to use on cold call"
```

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
