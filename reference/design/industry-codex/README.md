# Industry Design Codex

Visual conventions per industry — colors, fonts, photography, layout, tone.
Used to inform v0 prompts and site-config.ts overrides for demo site builds.

## Industries

| File | Industry | Subcategories |
|---|---|---|
| [home-services.md](home-services.md) | Home Services | Contractor, handyman, HVAC, plumbing, cleaning, repair |
| [chiropractor.md](chiropractor.md) | Chiropractor | Family care, sports injuries, wellness, pain specialist |
| [beauty-salon.md](beauty-salon.md) | Beauty Salon | Hair salon, nail salon, boutique salon |

## How to use

1. Identify the lead's industry from the Google Maps category
2. Read the matching codex file
3. Select the palette archetype that best fits the business's positioning
4. Copy the v0 prompt template from the bottom of the file
5. Fill in business-specific details (name, city, phone, services)
6. Run through v0 API → deploy via Netlify CLI

## Adding new industries

When a new industry is added to the lead gen config, run the research workflow:
1. Web search: "best [industry] website design examples 2025"
2. Web search: "[industry] website color palette" and "[industry] website fonts"
3. Fetch 3–4 live top-ranked sites and extract patterns
4. Write a new codex file following the same structure as the existing files
5. Add a row to this README

## Last updated
2026-02-18 — Initial codex: home services, chiropractor, beauty salon
