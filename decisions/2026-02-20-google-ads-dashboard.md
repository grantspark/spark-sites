# Google Ads Dashboard Integration

**Date:** 2026-02-20
**Status:** proposed
**Context:** VIP client dashboards (spark-dashboards repo) currently show Meta/Facebook data only. Need to add Google Ads.

## Options

| Option | Setup | Automation | Notes |
|--------|-------|------------|-------|
| **A. Manual JSON** | Zero | None — copy from Ads UI | Recommended starting point |
| B. Google Ads Scripts → Sheets | Medium | Weekly auto-export | No developer token needed |
| C. Google Ads API direct | Heavy | Full automation | Developer token approval required |

## Decision

Start with **Option A (manual)**. Add Google Ads numbers to client JSON files during weekly updates. Revisit Scripts → Sheets when volume justifies it.

## What Changes

- Add `source` field to campaign type (`"meta"` | `"google"`)
- Add source badge to campaign cards in the dashboard UI
- Update client JSON files to include Google Ads campaigns
