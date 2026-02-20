---
type: decision
date: 2026-02-20
status: accepted
linked_research:
  - research/2026-02-20-meta-api-dashboard-research.md
  - research/2026-02-20-dashboard-architecture-research.md
supersedes: null
---

# Decision: VIP Client Dashboard Architecture

## Context

Spark Sites manages VIP clients with ongoing Meta ads and/or organic social. Clients need a simple, branded way to see the value we're delivering. The primary metric is **people introduced to your business** (Meta reach — paid + organic). We want something dead simple, above the fold, updated weekly.

**Reference model:** [Huddle Duck client dashboard](https://clients.huddleduck.co.uk/demo1) — dark theme, 3 hero stats, per-campaign cards, metric legend, last sync timestamp.

## Options

### Option A: Separate repo (`spark-dashboards`) — Next.js static export on Netlify (recommended)

A standalone repo with Next.js static export. Each client gets a JSON config file and a data file. A GitHub Actions cron job pulls Meta API data weekly, commits updated JSON, and triggers a Netlify rebuild. Each client gets a unique URL path.

**Site structure:**

```
/ (home — static showcase)
├── Screenshot of a client dashboard (social proof)
├── Brief copy: "Spark Sites — Client Reporting"
├── Single link back to startwithspark.com
├── Not an internal tool — just a landing page if anyone finds the root URL
│
/[client-slug] (client-facing)
├── Header: client name + logo + Spark branding
├── Hero stats (3 big numbers):
│   ├── People introduced to your business (total reach)
│   ├── Weeks partnered
│   └── Active campaigns
├── Live campaigns (card per campaign):
│   ├── Campaign name + status badge
│   ├── Spend | Reach | Clicks | CTR
│   └── Health indicator (green/yellow/red)
├── Recently ended campaigns (collapsed)
├── Quick actions: Book a call | Request changes
├── Metric legend: "What do these numbers mean?"
└── Footer: "Last sync: [date]" + Spark branding
```

**Data pipeline:**

```
Meta API (weekly cron) → Node script → JSON per client → git commit → Netlify build hook → static site
```

**Repo structure:**

```
spark-dashboards/
├── app/
│   ├── page.tsx                    # Home (internal: all clients grid)
│   └── [slug]/
│       └── page.tsx                # Client dashboard
├── components/
│   ├── hero-stats.tsx              # 3 big numbers
│   ├── campaign-card.tsx           # Per-campaign metrics
│   ├── metric-legend.tsx           # "What do these numbers mean?"
│   └── client-card.tsx             # Home grid card
├── data/
│   ├── clients.json                # Client roster (name, slug, logo, ad account ID, page ID)
│   └── metrics/
│       ├── acme-plumbing.json      # Latest metrics for Acme
│       └── bobs-hvac.json          # Latest metrics for Bob's
├── scripts/
│   └── pull-meta-data.mjs          # GitHub Actions runs this weekly
├── .github/
│   └── workflows/
│       └── sync-metrics.yml        # Weekly cron
├── next.config.js                  # output: 'export'
└── netlify.toml
```

**Pros:**
- Clean separation — dashboard is its own concern, not tangled with agency or client repos
- Zero monthly cost (GitHub Actions free tier + Netlify free tier + Meta API free)
- Data is version-controlled (every weekly pull is a git commit — free historical snapshots)
- Branded to Spark — full Tailwind/shadcn control
- Onboarding a new client = add a JSON entry + their Meta credentials as GitHub secrets
- Client gets a clean URL they can bookmark
- Scales to 20+ clients without architecture changes

**Cons:**
- Another repo to maintain
- Meta Business Verification required (1-2 week process)
- System User token management (never expires, but if revoked, everything breaks)

### Option B: Inside spark-sites

Add a `dashboard/` folder to spark-sites with the same static export approach.

**Pros:**
- One less repo

**Cons:**
- Mixes agency marketing site concerns with client reporting
- spark-sites already has its own purpose (agency reference files, research, decisions)
- Different deploy target (spark-sites isn't a Next.js app)
- Violates the same separation principle that led to separate client repos

### Option C: Third-party tool (Looker Studio, AgencyAnalytics, etc.)

Use an existing SaaS dashboard product.

**Pros:**
- No code to maintain
- Some have native Meta connectors

**Cons:**
- Monthly cost ($30-150/mo for connectors or platform fees)
- Not branded to Spark
- Less control over the experience
- Can't match the Huddle Duck simplicity — most tools are over-featured
- Dependency on third-party pricing and availability

## Decision

**We chose: Option A (Separate repo, Next.js static export)**

The Huddle Duck reference proves that simple wins. Three hero numbers, campaign cards, a metric legend, and a sync timestamp. That's it. No login portals, no complex BI tools, no monthly SaaS fees. A static site rebuilt weekly from fresh Meta data gives clients exactly what they need: proof that we're introducing people to their business.

The separate repo follows the same principle as the client repo decision (Feb 12) — different concerns, different repos. spark-sites is the agency brain. spark-dashboards is the client-facing proof layer.

## Consequences

### What Becomes Easier
- Clients see value at a glance — one URL, one page, no login
- Sales conversations backed by live data ("look at your dashboard")
- Upsell signals visible (campaigns ending, reach plateaus)
- Client retention — dashboard proves ongoing value every week

### What Becomes Harder
- Meta Business Verification is a prerequisite (1-2 weeks)
- Each new client needs their ad account ID and page ID added
- If Meta API changes (ongoing organic metric deprecation), scripts need updating

### What We're Accepting
- The dashboard shows what Meta reports — we can't control attribution accuracy
- Organic metrics are in flux (Meta retiring legacy reach by June 2026) — use new metric names from day one
- Weekly sync means data is 0-7 days stale (acceptable for this use case)
- No real-time data — this is a reporting dashboard, not a monitoring tool

## Implementation Phases

### Phase 1: Foundation (can start now)
- Create `spark-dashboards` repo
- Build the client page template (hero stats, campaign cards, metric legend)
- Build the home page (internal client grid)
- Use mock/hardcoded data for design iteration
- Deploy to Netlify

### Phase 2: Meta API Connection (blocked on Business Verification)
- Apply for Meta Business Verification
- Create Meta Developer App (type: Business)
- Request Advanced Access: `ads_read`, `pages_read_engagement`, `business_management`
- Generate System User token
- Build `pull-meta-data.mjs` script
- Test with one client's ad account

### Phase 3: Automation
- Set up GitHub Actions weekly cron
- Configure Netlify build hook
- Onboard first real client
- Verify data accuracy against Ads Manager

### Phase 4: Polish
- Client ranking/gamification (optional)
- Email notification when dashboard updates
- Historical trend charts (data already in git history)
- StatiCrypt password protection (if clients request it)

## What Changes

No existing reference files change. This is a new project:

1. **New repo:** `spark-dashboards` on GitHub (grantspark org)
2. **New Netlify site:** `spark-dashboards.netlify.app` (or custom domain later)
3. **Meta Developer App:** New app in Meta Business Suite for API access
4. **GitHub Secrets:** Meta System User token + per-client credentials stored as repo secrets

## Review Date

Revisit after Phase 2 completes (Meta verification approved, first real client data flowing).
