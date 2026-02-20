---
type: decision
date: 2026-02-20
status: accepted
linked_decisions:
  - decisions/2026-02-12-brand-name-evolution.md
  - decisions/2026-02-12-growth-partner-positioning.md
---
# Parent Brand Website Architecture

## Situation

The parent brand needs its own website. Two options: build it under sparkmysite.com (subdirectory or subdomain) or as a separate WordPress install on sparkmygrowth.com.

## Decision

**Separate WordPress install on sparkmygrowth.com.**

## Rationale

- **Brand hierarchy:** The parent brand cannot live under a sub-brand's domain. sparkmysite.com is the websites offer — nesting the agency there is architecturally backwards.
- **SEO independence:** Parent brand targets different keywords (growth partner, marketing strategy, Lakeland marketing) than sparkmysite.com (web design, websites).
- **Content scale:** Heavy content pipeline planned — WordPress on its own domain gives room to scale without cluttering the websites offer.
- **Clean story:** sparkmygrowth.com is the agency. sparkmysite.com is one service. Each domain does one job.

## Domain Map

| Domain | Purpose | Platform |
|--------|---------|----------|
| sparkmygrowth.com | Parent brand / agency | WordPress |
| sparkmysite.com | Websites offer (sub-brand) | WordPress |
| sparkmycampaign.com | Client dashboards | Next.js static / Netlify |
| startwithspark.com | Vanity / legacy | Netlify (current), may redirect to sparkmygrowth.com |

## What Changes

- WordPress install needed on sparkmygrowth.com
- startwithspark.com homepage copy (already drafted in `outputs/2026-02-12-spark-parent-brand-homepage/`) targets the new domain
- startwithspark.com eventually redirects to sparkmygrowth.com (timing TBD)

## Open Questions

1. Hosting provider for the WordPress install
2. When to redirect startwithspark.com → sparkmygrowth.com
3. Parent brand name finalized (Spark / Spark Growth Partner / Spark Growth Agency)
