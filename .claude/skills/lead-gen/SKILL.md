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

**Template:** `startwithspark` repo (`C:/Users/grant/OneDrive/Documents/GitHub/startwithspark`)
- One-page Next.js static export
- Sections: Hero → Services Grid → Mid Banner → About → CTA Banner → Contact → Footer
- Single config file: `site-config.ts` — all copy, brand, CTAs live here
- Components pull directly from config — no component edits needed for new clients

---

#### 8a — Generate site-config.ts

Using data from the lead's markdown entry + any research from Facebook/Google Maps, populate:

```typescript
export const siteConfig = {
  brand: {
    name: "[Business Name]",
    tagline: "[Tagline or city + category]",
    email: "",          // leave blank if unknown
    domain: "",         // leave blank — no domain yet
    location: "[City], FL",
  },
  hero: {
    headline: "[Transformation or tagline headline]",
    subhead: "[What they do + why it matters in 1-2 sentences]",
    ctaText: "Call Us Now",
    ctaUrl: "#contact",
  },
  services: {
    sectionHeader: "How We Can Help",
    items: [
      // 4-6 plausible services based on category
      // Use their Google Maps category to infer what they likely offer
      // Each: { title, description, icon }
      // Icons: globe, megaphone, search, chart, palette, lightbulb, home, wrench, star, phone
    ],
  },
  midBanner: {
    tagline: "[Short punchy statement — 4-6 words]",
    subtext: "[One sentence supporting the tagline]",
    ctaText: "Call Now",
    ctaUrl: "#contact",
  },
  about: {
    sectionHeader: "About [Business Name]",
    body: [
      "[Owner name / business history / what makes them different]",
      "[Second paragraph — local roots, approach, commitment]",
    ],
  },
  ctaBanner: {
    headline: "[Action-oriented headline with their phone number or CTA]",
    ctaText: "Call (XXX) XXX-XXXX",
    ctaUrl: "tel:+1XXXXXXXXXX",
  },
  contact: {
    sectionHeader: "Get In Touch",
    subtext: "[Address + phone. Simple and direct.]",
  },
  footer: {
    tagline: "[Business Name] — [City], FL",
    subtext: "[One-liner about what they do]",
    year: new Date().getFullYear(),
  },
}
```

**Color palette:** Pull the recommended palette from the industry codex file (Step 7).
Use the archetype or family that best matches the business's positioning.
Only change the `:root` color variables in globals.css — nothing else.

---

#### 8b — Scaffold the repo

```bash
# 1. Copy the template
cp -r C:/Users/grant/OneDrive/Documents/GitHub/startwithspark \
      C:/Users/grant/OneDrive/Documents/GitHub/[client-slug]

# 2. Remove template git history
cd C:/Users/grant/OneDrive/Documents/GitHub/[client-slug]
rm -rf .git

# 3. Init fresh repo
git init
git checkout -b main

# 4. Overwrite site-config.ts with generated content (see 8a)
# 5. Update globals.css color variables from codex (see 8a)

# 6. Commit
git add .
git commit -m "[add] [Business Name] demo site — generated from lead"

# 7. Create GitHub repo and push
gh repo create grantspark/[client-slug] --private --source=. --push
```

**Client slug format:** lowercase, hyphens, no spaces. Example: `paragon-home-services`

---

#### 8c — Deploy to Netlify (fully automated via CLI)

**Prerequisites:** Netlify CLI installed (`npm install -g netlify-cli`) and authenticated (`netlify login`). Account slug: `grant-plw4ylu`.

```bash
# 1. Create the Netlify site (non-interactive — avoids Windows prompt bug)
netlify api createSite --data '{"body": {"name": "[client-slug]", "account_slug": "grant-plw4ylu"}}'
# → Returns site ID (e.g. c82ede9b-...) and URL ([client-slug].netlify.app)

# 2. Build the site
cd C:/Users/grant/OneDrive/Documents/GitHub/[client-slug]
pnpm build

# 3. Deploy using the site ID (NOT the site name — name lookup fails)
netlify deploy --prod --dir=out --site [site-id-from-step-1]
```

**Note:** `netlify sites:create` crashes on Windows with "unsettled top-level await". Always use `netlify api createSite` instead. Always use the site ID (not site name) in the deploy command.

Netlify assigns URL: `https://[client-slug].netlify.app`

After deploy, confirm in chat:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEMO SITE — [Business Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Live at: https://[slug].netlify.app
GitHub:  https://github.com/grantspark/[client-slug]

Sections: Hero / Services / About / Contact
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
