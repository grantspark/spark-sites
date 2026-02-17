---
name: proposal
description: "Generate client proposals from explicit requests and implicit needs. Reads pricing matrix, offer files, and product ladder to produce line-itemized proposals with upsell recommendations. Use when: user says proposal, quote, estimate, scope, or describes a client request. Supports intake from conversation notes, call transcripts, or direct description."
---

# Proposal Generator

Turn client requests into structured proposals — what they asked for, what they actually need, and how to phase it.

---

## Critical Rules

1. **Never invent pricing.** Every line item must trace to `reference/domain/pricing-matrix.md` or an `offers/[service]/offer.md` file. If a service isn't in the matrix, flag it and ask.
2. **Never skip the explicit request.** The proposal always leads with exactly what the client asked for, quoted at the prices in the matrix.
3. **Upsells are recommendations, not surprises.** The "Recommended" section explains WHY each addition matters — connected to the client's situation, not generic.
4. **Never fabricate labor hours.** Use the estimates in the pricing matrix. If a task isn't listed, estimate conservatively and mark it as "estimated."
5. **Proposals are client-facing documents.** Write in Spark's voice (warm, clear, educational). No internal jargon, no margin notes in the output.

---

## Step 0: Find Business Repo

**CWD-first:** If `reference/core/` exists in CWD, you're in the business repo — use it.

If CWD is NOT a business repo:
- Check `.claude/settings.local.json` for additionalDirectories that contain `reference/core/`
- Or ask the user for the path

---

## Step 1: Load Pricing Context

Read these files (all required):

| File | Path | Purpose |
|------|------|---------|
| Pricing Matrix | `reference/domain/pricing-matrix.md` | Internal costs, labor hours, upsell triggers |
| Product Ladder | `reference/domain/product-ladder.md` | How services connect, upsell paths |
| Soul | `reference/core/soul.md` | Voice and values for proposal tone |
| Voice | `reference/core/voice.md` | How Spark communicates |

Also load the specific offer file(s) for whatever services the client is asking about:

```
reference/offers/[service]/offer.md
```

If the client mentions multiple services, load all relevant offer files.

---

## Step 2: Gather Client Context

Ask the user for the intake. Accept any of these formats:

| Input Type | Example | How to Handle |
|------------|---------|---------------|
| **Direct description** | "S&D Real Estate wants an MLS install" | Parse explicit requests, note industry signals |
| **Call notes / transcript** | Pasted text from a call | Extract explicit asks AND implicit signals |
| **Email / message** | Forwarded client communication | Same — explicit + implicit |
| **Bullet list** | "Website, SEO, maybe social" | Treat as explicit, probe for details |

### What to Extract

**Explicit requests** — What the client directly asked for:
- Specific services mentioned
- Specific features mentioned (e.g., "MLS install", "e-commerce", "blog")
- Budget mentioned (if any)
- Timeline mentioned (if any)

**Implicit needs** — What the context reveals they also need:
- Use the "Implicit Need Signals" table in the pricing matrix
- Use the "Cross-Sell / Upsell Quick Reference" table
- Industry-specific signals (real estate = MLS + local SEO + Google Ads; restaurant = Google Business + social + influencer events; etc.)
- Things they mentioned in passing but didn't ask for ("nobody can find us" = SEO)

**Client details:**
- Business name
- Industry / business type
- Location (if relevant for local services)
- Existing website (if any)
- Current marketing (if mentioned)

### If Details Are Thin

If the user gives a one-liner like "S&D wants an MLS install," work with what you have. Cross-reference against the pricing matrix and product ladder to build recommendations. Don't interrogate — generate the best proposal you can from available info, and flag assumptions.

---

## Step 3: Build the Proposal

### Structure

Every proposal follows this format:

```markdown
---
type: output
subtype: proposal
date: YYYY-MM-DD
client: [Business Name]
status: draft
---

# Proposal: [Client Name]

**Prepared by:** Spark
**Date:** [Date]
**Valid for:** 30 days

---

## Understanding

[2-4 sentences summarizing what the client needs and why. Demonstrates
we listened. References their situation, not generic marketing speak.]

---

## Scope: What You Asked For

[Line items for exactly what the client explicitly requested.
Each item includes description, what's included, and price.]

| Service | Description | Price |
|---------|-------------|-------|
| [service] | [what's included, briefly] | $X |
| [service] | [what's included, briefly] | $X |

**Subtotal:** $X

---

## Recommended: What Will Make This Work

[Upsell section. Each recommendation tied to the client's specific
situation with a one-sentence "why this matters for you" rationale.]

| Service | Why It Matters | Price |
|---------|---------------|-------|
| [service] | [specific rationale tied to THEIR business] | $X |
| [service] | [specific rationale tied to THEIR business] | $X |

**Subtotal (if all recommended):** $X

---

## Investment Summary

| | Services | Price |
|---|---------|-------|
| **What you asked for** | [list] | $X |
| **Recommended additions** | [list] | $X |
| **Total (with recommendations)** | | $X |

*Recommended additions are optional. We'll deliver what you asked for
regardless — these are our professional recommendations based on your goals.*

---

## Phasing (if applicable)

[Only include if the total scope is large enough to warrant phases.
Helps clients who can't do everything at once.]

### Phase 1: [Name] — [Timeline]
- [deliverables]
- Investment: $X

### Phase 2: [Name] — [Timeline]
- [deliverables]
- Investment: $X

---

## What's Next

1. Review this proposal
2. Let us know which services you'd like to move forward with
3. We'll send an invoice for the first phase
4. Kick-off call to align on details and timeline

---

## About Spark

[Brief — pull from soul.md. 2-3 sentences max. Not a sales pitch,
just a reminder of who we are.]
```

### Phasing Rules

- **Under $2,000 total:** No phasing needed unless client signals budget constraints
- **$2,000–$5,000:** Suggest 2 phases (core deliverable first, then additions)
- **Over $5,000:** Always phase. Lead with the most impactful deliverable.
- **Phase 1 always includes the explicit request.** Never push what they asked for to Phase 2.

### Pricing Rules

- Use exact prices from the pricing matrix and offer files
- For ranges (e.g., "$1,500–$2,500"), pick the midpoint or ask user to specify
- For custom pricing (influencer events), note "Custom — quoted after scoping"
- For add-ons not in the matrix, estimate and mark: "(estimated — confirm before sending)"
- **Recurring vs. one-time:** Clearly separate. Monthly costs get their own line with "/mo" suffix
- **Third-party costs:** Note but don't include in totals (e.g., "Ad spend is additional, billed directly by Google/Meta")

---

## Step 4: Internal Notes (Not Client-Facing)

After the proposal, generate an internal-only section for the team:

```markdown
---

## Internal Notes (DO NOT SEND TO CLIENT)

### Labor Estimate
| Service | Est. Hours | Rate | Internal Cost |
|---------|-----------|------|---------------|
| [service] | X hrs | $120/hr | $X |

**Total labor cost:** $X
**Total quoted:** $X
**Gross margin:** X%

### Upsell Strategy
- [What to emphasize in the follow-up call]
- [Which recommended service has the highest close probability]
- [What to listen for that would trigger additional recommendations]

### Assumptions
- [Any assumptions made due to incomplete info]
- [Anything flagged as "estimated" in the proposal]
```

---

## Step 5: Email Draft (Ember Voice)

Every proposal includes a ready-to-send email written in the **Ember** persona.

**Ember** is Spark's client-facing support voice — energetic, warm, people-first friendly. Think: the person at the front desk who genuinely lights up when someone walks in. Not salesy, not formal, just glad to help.

> **TODO:** Full Ember persona definition coming (will live in `reference/brand/ember.md`). Until then, use these guidelines.

### Ember Voice Rules

- **Open with energy.** Warm, specific greeting — not "Dear Client" or "Hope this finds you well." Something like "Hey [Name]!" or "Hi [Name]! Great chatting with you about [thing]."
- **Get to the estimate fast.** One sentence of context, then the number. Don't bury the lead.
- **Close with the link + question pattern.** Always this exact structure:

```
Here's how to get started: [LINK]

Or, did you have any questions before we get started?
```

- **Sign off warm.** Short, human. "Talk soon!" or "Excited to get this going!" — not "Best regards."
- **Keep it short.** The proposal has all the details. The email is the friendly nudge to open it.

### Email Template

```
Subject: Your [project type] estimate is ready!

Hey [Name]!

[One warm sentence referencing the conversation or their business — show you were listening.]

Here's a quick look at what we put together:

[Brief scope summary — 2-3 bullet points max, with total]

Here's how to get started: [LINK]

Or, did you have any questions before we get started?

[Warm sign-off],
Spark Team
```

### Save Location

Save the email draft as: `outputs/YYYY-MM-DD-proposal-{client-slug}/email.md`

---

## Step 6: Save and Present

1. Save to: `outputs/YYYY-MM-DD-proposal-{client-slug}/proposal.md`
2. Save internal notes: `outputs/YYYY-MM-DD-proposal-{client-slug}/internal-notes.md`
3. Save email draft: `outputs/YYYY-MM-DD-proposal-{client-slug}/email.md`
4. Present a summary to the user (not the whole proposal — they can read the files):
   - What was quoted (explicit)
   - What was recommended (upsell)
   - Total range
   - Any flags or assumptions
5. Ask: "Want me to adjust anything before you send this?"

---

## Offer Context Resolution

When the client requests multiple services, load ALL relevant offer files. This is not single-offer mode — proposals often span the entire product ladder.

```
Client asks for "website and SEO"
→ Load: offers/websites/offer.md + offers/seo/offer.md + pricing-matrix.md
```

For services that cross-sell naturally (per the product ladder), proactively load adjacent offer files to inform the Recommended section.

---

## Examples

### Example: S&D Real Estate — MLS Install

**Explicit:** MLS/IDX installation on existing website
**Implicit signals:** Real estate → local SEO, Google Ads (homebuyer keywords), site navigation updates, Google Business optimization

**Scope (What They Asked For):**
- MLS/IDX Installation: $450
- Site edits (navigation, listing pages): included in MLS install

**Recommended:**
- Local SEO one-time optimization: $900 (people need to find those listings)
- Google Business Profile setup: $150 (real estate is hyper-local)
- Google Ads setup + management: $350 setup + $350/mo (capture "homes for sale in [city]" searches)

**Phasing:** Phase 1 = MLS + site edits ($450). Phase 2 = SEO + Google ($1,400 + $350/mo).

---

## Recovery from Compaction

If context compresses mid-task:

1. Check `outputs/` for in-progress proposals: `ls -ltd outputs/*-proposal-*/ 2>/dev/null | head -3`
2. Re-read the pricing matrix and product ladder
3. Ask user: "I see a draft proposal for [client]. Continue from here?"

---

## When NOT to Use

- Internal pricing discussions (just read the pricing matrix directly)
- Existing client scope changes (update the existing proposal, don't start fresh)
- Quick verbal quotes (just reference the pricing matrix — no formal proposal needed)

Use `/proposal` when generating a structured, sendable document for a prospective or existing client.
