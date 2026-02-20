---
type: research
date: 2026-02-20
topic: Meta API for VIP Client Dashboard
method: web-research
---

# Meta Marketing API + Pages API: Client Reporting Dashboard Research

## Purpose

Research practical details for building a client reporting dashboard that pulls paid ads performance and organic Page metrics from Meta's APIs. This is for Spark Sites operating as an agency managing multiple client Facebook/Instagram ad accounts and Pages.

---

## 1. Authentication: System User Tokens vs. Long-Lived User Tokens

### Token Types Comparison

| Token Type | Lifespan | Best For | Refresh Required? |
|---|---|---|---|
| **Short-lived user token** | ~1-2 hours | Testing/dev only | Yes, constantly |
| **Long-lived user token** | ~60 days | Single-user apps | Yes, every 60 days |
| **System User token** | **Never expires** | **Agencies, production** | **No** (unless revoked) |
| **Page token** | Inherited from user token | Page-specific operations | Depends on parent token |

### Recommendation: System User Tokens

For an agency managing multiple client accounts, **System User tokens are the clear winner**:

- **Never expire** -- no token refresh headaches in production
- **Not tied to a personal Facebook account** -- if an employee leaves, nothing breaks
- **Created inside Business Manager** -- proper access control
- **Can be scoped** to specific ad accounts and Pages
- **Required for server-to-server** automation (no browser login flow)

### How to Set Up a System User Token

1. Go to **Business Settings** > **Users** > **System Users**
2. Click **Add** > name it (e.g., "Spark Dashboard Bot")
3. Set role to **Admin** (needed for full read access across client assets)
4. Click **Generate New Token**
5. Select your App (the Meta Developer App you created)
6. Choose permissions: `ads_read`, `pages_read_engagement`, `business_management`, `read_insights`
7. **Set Token Expiration to "Never"**
8. Copy the token immediately -- Meta will **never show it again**
9. Assign the System User access to each client's ad account and Page via **Assets** tab

### Setting Up the Meta Developer App

1. Go to [developers.facebook.com](https://developers.facebook.com)
2. **Create App** > Select **"Business"** type (this unlocks Marketing API access)
3. Connect it to your **Spark Business Manager**
4. Under **Add Product**, select **Marketing API**
5. Under **App Settings** > **Basic**, fill in all required fields (Privacy Policy URL, App Icon, etc.)
6. Under **Permissions**, request the needed scopes (see Section 3)
7. Complete **Business Verification** in Security Center (see Section 3)

---

## 2. Key API Endpoints

### A. Ad Account Insights: `/act_{ad_account_id}/insights`

This is the primary endpoint for paid campaign performance.

**Base URL:**
```
GET https://graph.facebook.com/v22.0/act_{ad_account_id}/insights
```

**Key fields for a client dashboard:**

| Field | What It Returns | Notes |
|---|---|---|
| `reach` | Unique people who saw ads | Deduplicated; 13-month retention limit |
| `impressions` | Total ad appearances | Not deduplicated |
| `spend` | Total amount spent | In account currency |
| `clicks` | All clicks (link + other) | Includes profile clicks, reactions |
| `inline_link_clicks` | Link clicks only | More accurate for CTR |
| `cpc` | Cost per click | Calculated: spend / clicks |
| `cpm` | Cost per 1,000 impressions | Calculated: (spend / impressions) * 1000 |
| `ctr` | Click-through rate | Calculated: clicks / impressions |
| `frequency` | Avg times each person saw ad | 6-month retention limit |
| `actions` | Array of conversion events | Purchases, leads, etc. |
| `cost_per_action_type` | Cost per conversion | Paired with actions array |
| `conversions` | Off-Facebook conversions | Requires Pixel/CAPI |

**Example API call -- last 30 days summary:**
```
GET /act_{id}/insights?
  fields=reach,impressions,spend,clicks,inline_link_clicks,cpc,cpm,ctr,frequency,actions
  &date_preset=last_30d
  &level=account
```

**Example -- daily breakdown:**
```
GET /act_{id}/insights?
  fields=reach,impressions,spend,clicks,cpc,cpm,ctr
  &date_preset=last_30d
  &time_increment=1
  &level=campaign
```

**Available `date_preset` values:**
`today`, `yesterday`, `last_3d`, `last_7d`, `last_14d`, `last_28d`, `last_30d`, `last_90d`, `this_week_mon_today`, `this_week_sun_today`, `last_week_mon_sun`, `last_week_sun_sat`, `this_month`, `last_month`, `this_quarter`, `last_quarter`, `this_year`, `last_year`, `lifetime`

**Custom date range (alternative to `date_preset`):**
```json
{
  "time_range": {
    "since": "2026-01-01",
    "until": "2026-01-31"
  }
}
```

**Aggregation levels (`level` param):**
- `account` -- rolled up to account (default)
- `campaign` -- per campaign
- `adset` -- per ad set
- `ad` -- per individual ad

**Summary in a single call:**
Use `default_summary=true` to get aggregated totals included in the response alongside row-level data.

### B. Page Insights: `/{page_id}/insights`

**CRITICAL NOTE (Nov 2025 Deprecations):** Meta has been deprecating Page Insights metrics aggressively. As of late 2025:

**Deprecated metrics (return errors):**
- `page_impressions` -- replaced by `page_views`
- `page_fans` -- no direct replacement
- Legacy `reach` metrics -- being replaced by "Viewers"

**Metric rename mapping (Meta Business Suite):**

| Legacy Term | New Term | API Impact |
|---|---|---|
| Reach | **Viewers** | Unique people who saw content |
| Impressions | **Views** | Total content screen appearances |
| Engagement | **Interactions** | Intentional actions only |

**Still-functional Page metrics (verify before relying on):**
- `page_views_total` -- total Page views
- `page_engaged_users` -- unique users who engaged
- `page_post_engagements` -- total engagement actions on posts
- `page_fan_adds` -- new Page likes/follows (may be limited)
- `page_actions_post_reactions_total` -- reactions breakdown

**Important:** Ads Manager metrics (reach, impressions, engagement) are **NOT affected** by these deprecations. The deprecations apply to **organic Page metrics only**.

**Example call:**
```
GET /{page_id}/insights?
  metric=page_views_total,page_engaged_users,page_post_engagements
  &period=day
  &since=2026-01-21
  &until=2026-02-20
```

**Period options:** `day`, `week`, `days_28`, `month`, `lifetime`

### C. Rate Limits

Meta uses a **Business Use Case (BUC)** scoring system, not simple request counts:

| Factor | Detail |
|---|---|
| **Window** | Rolling 1-hour window |
| **Base calls** | ~60 calls (base allocation) |
| **Per active ad** | +400 additional capacity per active ad in the account |
| **Scoring** | Read calls = 1 point; Write calls = 3 points |
| **Insights queries** | Count as "heavier" due to query complexity |
| **Error penalty** | -0.001 capacity per error response |
| **Error codes** | `613` (rate limit) or `80004` (too many calls) |
| **Instagram Graph API** | Separate limit: 200 requests/hour base |

**How to check current usage:**
Include `x-business-use-case-usage` header in responses. This tells you your current percentage of the limit.

**Practical guidance:**
- For a dashboard pulling data once/day for 5-10 client accounts, you will almost never hit rate limits
- Batch multiple queries into a single request where possible
- If pulling daily: stagger client pulls over minutes, not all at once
- Use async requests for large date ranges or many breakdowns

---

## 3. Permissions & Business Verification

### Required Permissions

| Permission | Purpose | Access Level Needed |
|---|---|---|
| `ads_read` | Read ad performance data, campaign info | **Advanced Access** |
| `pages_read_engagement` | Read Page engagement metrics | **Advanced Access** |
| `pages_show_list` | List Pages the user manages | Standard Access |
| `business_management` | Access Business Manager features | **Advanced Access** |
| `read_insights` | Read insights for Pages/apps | **Advanced Access** |
| `public_profile` | Basic profile info | Standard Access |

**Optional but useful:**
- `pages_manage_posts` -- if you also want to post content via API
- `instagram_basic` + `instagram_manage_insights` -- if pulling IG metrics too
- `ads_management` -- only if creating/editing ads programmatically (not needed for read-only dashboard)

### Standard Access vs. Advanced Access

- **Standard Access:** Lets you use permissions on your **own** ad accounts and Pages only (where you are admin). Good for testing.
- **Advanced Access:** Required for accessing **client** accounts. Requires **App Review** and **Business Verification**.

### Business Verification Process

1. Go to **Business Settings** > **Security Center**
2. Click **Start Verification**
3. Submit:
   - Legal business name (must match government records)
   - Business address
   - Business phone number
   - Business website (startwithspark.com)
   - Tax ID / EIN or business registration document
   - Government-issued ID of business admin
4. Meta reviews in **1-5 business days** (can take longer)
5. Once verified, you can apply for **Advanced Access** per permission

### Advanced Access Application (per permission)

- Each permission requires a **separate justification**
- You must explain **how your app uses the permission** and **why it benefits users**
- Some permissions require a **screencast** demonstrating the functionality
- Review typically takes **5-10 business days**
- Rejection requires resubmission with updated justification

### Common Pitfalls

- Business verification is a **prerequisite** for Advanced Access -- you cannot skip it
- Business verification and App Review are **separate processes**
- If your app is in "Development Mode," only admin/developer/tester roles can use it
- You must **switch to Live Mode** after getting Advanced Access for client access

---

## 4. Data Freshness & Delays

### How Often Does Meta Update Insight Data?

| Data Type | Freshness | Notes |
|---|---|---|
| **Delivery metrics** (impressions, reach, clicks, spend) | **~15 minutes** | Near real-time |
| **Conversion/action metrics** | **24-72 hours** for full accuracy | Attribution continues to adjust |
| **Attribution adjustments** | Up to **28 days** after event | Click-through conversions can be re-attributed |
| **Unique metrics** (unique_clicks, reach) | Same day, but can adjust | Deduplication refines over time |

### Key Implications for Dashboard

1. **For a client-facing monthly report:** pulling data 48+ hours after the period ends gives stable numbers
2. **For real-time dashboards:** delivery metrics (spend, clicks, impressions) update within ~15 min, but conversion counts will drift upward over days
3. **Best practice:** Re-pull the trailing 7 days of data on each sync to capture attribution updates
4. **Recommended sync interval:** Every 6-12 hours for active campaigns; once daily for reporting dashboards

### Data Retention Limits (as of Jan 2026)

| Metric Type | Max Historical Range |
|---|---|
| Aggregate totals (spend, clicks, impressions) | **37 months** |
| Unique-count fields (reach, unique_actions) | **13 months** |
| Hourly breakdowns | **13 months** |
| Frequency breakdowns | **6 months** |

**Warning:** Queries beyond these windows return **empty datasets** (not errors) -- silent failures that can break dashboards.

### Attribution Window Changes (Jan 12, 2026)

**Deprecated windows:**
- 7-day view-through (`7d_view`)
- 28-day view-through (`28d_view`)

**Still available:**
- 1-day click, 7-day click, 28-day click
- 1-day engaged view
- 1-day view

This means view-through conversion attribution is significantly reduced. Expect conversion counts to appear 30-40% lower compared to legacy reporting that used 28-day view windows.

---

## 5. Token Management

### Token Lifespans

| Token Type | Lifespan | Refresh Method |
|---|---|---|
| Short-lived user token | ~1-2 hours | Re-authenticate via OAuth |
| Long-lived user token | ~60 days | Exchange before expiry via `/oauth/access_token` |
| **System User token** | **Never expires** | **No refresh needed** |
| Page token (from long-lived user) | Same as parent (~60 days) | Re-exchange when parent refreshes |
| Page token (from System User) | **Never expires** | **No refresh needed** |

### System User Token Management (Recommended)

- Created once in Business Manager, lasts forever
- Store securely (environment variable, secrets manager -- **never in code**)
- If compromised: revoke in Business Manager > System Users > token section
- One System User can hold tokens for multiple apps
- Assign access to each client's ad accounts and Pages via **Assets** tab

### Page Tokens via System User

When your System User has `pages_read_engagement` permission and is assigned to a client Page:
```
GET /me/accounts?access_token={system_user_token}
```
This returns Page-specific tokens that also never expire (inherited from System User).

### Long-Lived Token Refresh (if not using System User)

```
GET /oauth/access_token?
  grant_type=fb_exchange_token
  &client_id={app_id}
  &client_secret={app_secret}
  &fb_exchange_token={short_lived_token}
```
Returns a 60-day token. Must be refreshed before it expires. Set up a cron job or calendar reminder.

### Security Best Practices

- **Never expose tokens client-side** -- all API calls from server
- Store tokens in environment variables or encrypted secrets manager
- Use the minimum required permissions
- Audit System User asset access quarterly
- Revoke tokens immediately if any team member leaves

---

## 6. Static Report Generation: Can We Pull Last-30-Days in a Single Call?

### Yes -- Single Call for Aggregated Summary

```
GET /act_{id}/insights?
  fields=reach,impressions,spend,clicks,inline_link_clicks,cpc,cpm,ctr,frequency,actions
  &date_preset=last_30d
  &level=account
```

This returns a **single row** with the 30-day aggregate. No manual aggregation needed.

### Daily Breakdown in a Single Call

```
GET /act_{id}/insights?
  fields=reach,impressions,spend,clicks,cpc,cpm,ctr
  &date_preset=last_30d
  &time_increment=1
  &level=campaign
```

Returns one row per day per campaign. More data, but still a single API call.

### When You Need Multiple Calls

- **Large accounts with many campaigns:** responses may be paginated (follow `paging.next` cursor)
- **Multiple breakdown dimensions:** e.g., age + gender + platform breakdown creates many rows
- **Per-client pulls:** you need one call per ad account (no cross-account query)
- **Async required for heavy queries:** large date ranges with many breakdowns may timeout. Use async:
  ```
  POST /act_{id}/insights?
    fields=...
    &date_preset=last_90d
    &time_increment=1
    &level=ad
  ```
  Returns a `report_run_id`. Poll until status is complete, then fetch results.

### Recommended Approach for Monthly Client Report

1. **One API call per client ad account** with `date_preset=last_30d` at `level=campaign`
2. Add `default_summary=true` to get account-level totals alongside campaign breakdown
3. **One API call per client Page** for organic metrics with `period=days_28`
4. For 5-10 clients, this is ~10-20 API calls total -- well within rate limits
5. Pull once daily via cron job; store results in your database
6. Generate PDF/dashboard from stored data

---

## 7. API Version & Deprecation Timeline

| Version | Status | Notes |
|---|---|---|
| v22.0 | Current (as of Feb 2026) | Latest stable |
| v19.0-v21.0 | Still functional | Being deprecated on rolling basis |
| Legacy APIs | Deprecated Q1 2026 | Advantage Shopping, App Campaign APIs |

**Always pin to a specific version** in your API calls (e.g., `/v22.0/act_{id}/insights`). Meta deprecates old versions ~2 years after release.

---

## 8. Practical Architecture for Spark Dashboard

### Suggested Stack

```
[Cron Job / Scheduler]
        |
        v
[Node.js / Python Backend]
        |
        |-- System User Token (env var)
        |
        v
[Meta Marketing API]  +  [Meta Pages API]
        |                       |
        v                       v
   Ad Insights            Page Insights
        |                       |
        v                       v
[Database (Postgres / SQLite)]
        |
        v
[Dashboard UI / PDF Generator]
```

### Key Design Decisions

1. **Use System User tokens** -- never-expiring, not tied to personal accounts
2. **Pull data once daily** (early morning) -- sufficient for monthly reporting
3. **Re-pull trailing 7 days** each sync to capture attribution updates
4. **Store raw API responses** in database for historical comparison
5. **Pin API version** and test before upgrading
6. **Handle pagination** -- always follow `paging.next` cursors
7. **Implement exponential backoff** for rate limit errors (613, 80004)

---

## Sources

- [Windsor.ai Guide to Meta Ads API](https://windsor.ai/guide-to-facebook-meta-ads-api/)
- [AdManage.ai Meta Ads API Complete Guide (2025)](https://admanage.ai/blog/meta-ads-api)
- [Damien Gonot - Guide to Facebook Insights API](https://www.damiengonot.com/blog/guide-facebook-insights-api)
- [MagicBrief - Comprehensive Guide to Facebook Ads Reporting API](https://magicbrief.com/post/comprehensive-guide-to-the-facebook-ads-reporting-api)
- [PPC Land - Meta Restricts Attribution Windows](https://ppc.land/meta-restricts-attribution-windows-and-data-retention-in-ads-insights-api/)
- [PPC Land - Meta Deprecates Page Insights Metrics](https://ppc.land/meta-deprecates-additional-page-insights-api-metrics-from-november-15/)
- [ExtraDigital - Meta Reporting Changes 2025-2026](https://www.extradigital.co.uk/articles/marketing/meta-reporting-changes-2025/)
- [Weld - Facebook System User Token Authentication](https://weld.app/blog/facebook-system-user-token-support)
- [AgentsAPIs - Meta API Pricing & Rate Limits](https://agentsapis.com/meta-api/pricing/)
- [AdAmigo - Meta Ads API Key Creation Workflow](https://www.adamigo.ai/blog/meta-ads-api-key-creation-workflow-explained)
- [Dataslayer - Meta Ads Attribution Window Changes 2026](https://www.dataslayer.ai/blog/meta-ads-attribution-window-removed-january-2026)
