---
type: research
date: 2026-02-13
source: claude-code
topics: [website-builds, ai-workflow, service-delivery, platforms]
linked_decisions: []
status: draft
---
# AI-Driven Website Builds: Process & Platform Research

## The Question

How do we move from standard website builds to AI-driven website builds as a core service?

## Current State

**What's working:**
- `/site` skill + Netlify deployment is fast and effective for brochure/informational sites
- Static HTML/CSS sites look great, deploy instantly, low maintenance
- Reference-driven generation means sites are on-brand from the start

**What's missing:**
- No CRM integration on static sites — clients who need lead management are underserved
- Limited SEO visibility — can't easily track performance, rankings, or organic traffic
- Not robust enough for clients who need more than an informational presence
- No plugin ecosystem, no forms-to-pipeline, no e-commerce

## Platforms Under Consideration

| Platform | Type | Strengths | Questions |
|----------|------|-----------|-----------|
| **Netlify + /site** | Static generation | Speed, simplicity, AI-native workflow | Enough for what % of clients? |
| **WordPress.com** | CMS (has MCP) | Plugin ecosystem, CRM integrations, SEO tools, client self-service | Can MCP make builds AI-fast? What's the workflow? |
| **Lovable** | AI app builder | App-like experiences, AI-generated | Client handoff? Maintenance? Lock-in? |
| **Manus** | AI agent platform | Autonomous builds | Maturity? Reliability? Client-facing? |

## Key Dimensions to Resolve

### 1. Client Need Segmentation
What percentage of website clients actually need more than a brochure site? This determines whether the current /site workflow covers 80% of cases or 20%.

### 2. What "AI-Driven" Means for Our Workflow
Three possible models:
- **AI builds the whole site** — client describes, AI generates (Lovable/Manus approach)
- **AI accelerates our build** — we still architect, AI does heavy lifting (WordPress MCP approach)
- **Hybrid** — simple sites fully AI-generated, complex ones AI-assisted

### 3. Business Model Implications
Current website pricing: $500-$3,500+. If AI cuts build time by 70%:
- Keep pricing, pocket the margin?
- Lower price, increase volume?
- Shift to higher-value services (strategy, ongoing growth) and use fast sites as an entry point?

These three questions shape which platforms matter and how the service model evolves.

## Frameworks Emerging

**Speed vs. Capability tradeoff:** The faster the build tool, the less capable it tends to be. Static sites are instant but limited. WordPress is powerful but slower to build. The sweet spot depends on what the client actually needs.

**Site as product vs. site as entry point:** If the site IS the deliverable, it needs to be robust. If the site is an entry point to the growth partnership (which aligns with our positioning), it just needs to convert — and the ongoing relationship is where the real value lives.

## Open Questions

- [ ] What does the WordPress.com MCP actually enable? Can it generate full sites from reference files?
- [ ] What's Lovable's handoff story — can clients maintain what AI builds?
- [ ] What's Manus's reliability and maturity level for client-facing work?
- [ ] Could we tier our offering: Tier 1 (brochure, /site + Netlify) vs. Tier 2 (full platform, WordPress)?
- [ ] What does SEO tooling look like on each platform?
- [ ] How do CRM integrations compare across platforms?
- [ ] What's the competitive landscape — are other agencies already offering AI-built sites?

## Next Steps

1. Answer the three framing questions (client breakdown, AI model, business model)
2. Deep research on WordPress.com MCP capabilities
3. Evaluate Lovable and Manus for agency use cases
4. Draft a decision on platform tiering strategy
