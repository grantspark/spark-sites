---
type: research
date: 2026-02-23
status: active
tags: [finance, loc, pressable, flywheel, cash-flow]
---

# LOC + Pressable Arbitrage Analysis (6-Month Delay Scenario)

## Context

Grant explored opening an OnDeck business line of credit ($40K limit, 52.4% APR, 24-month amortization) to execute a hosting cost arbitrage play. The plan: borrow $10K, pay Pressable annually ($8K), eliminate $2,000/month Flywheel hosting, apply $2K to credit cards, then repay the LOC when a $10K Pressable deposit arrives.

**New information (Feb 2023):** The $10K Pressable deposit is delayed 6 months.

This analysis audits the ChatGPT financial reasoning and provides an independent verdict.

---

## Current Debt Profile

- **Flywheel hosting:** $2,000/month recurring
- **Credit cards:** $27,000 balance (~28% APR estimated)
- **LOC terms:** 52.4% APR, 364-day basis, daily accrual, 24-month amortization
- **LOC payment on $10K:** $738/month (quoted)

---

## UPDATE (2026-02-27): Pressable Plan Purchased

**Actual purchase:** 200 sites at $6,600/year (not 250 sites at ~$8,300 as originally estimated).

| | Original Estimate | Actual Purchase | Delta |
|--|-------------------|-----------------|-------|
| Sites | 250 | 200 | -50 |
| Annual cost | ~$8,300 | $6,600 | **-$1,700** |
| Monthly equivalent | ~$692 | $550 | -$142/mo |
| Leftover from $10K LOC for CC | $1,700 | **$3,400** | +$1,700 |

This improves every number in the analysis below. Starting CC balance drops from $25,000 to **$23,600**. Monthly cash flow improvement increases from ~$1,322 to **~$1,364**. All scenario tables below reflect the original estimates — see updated tables at the end of this section for revised numbers.

---

## ChatGPT Accuracy Audit

### What ChatGPT Got Right
- Daily interest rate calculation: 52.4% / 364 = 0.1439%/day ($1.87/day on $1,300) — **correct**
- 30-day payoff on $1,300: ~$56 interest, ~$1,356 total — **correct**
- Implied APR from $738/month on $10K: ~52-53% — **correct** (ChatGPT said 53-55%, slightly high)
- Monthly cash flow improvement: ~$1,300-1,500/month — **correct** (verified at ~$1,322)
- Core arbitrage logic: swapping $2K/month for $738/month — **sound**
- Behavioral risk warnings about LOC creep — **accurate and important**

### What ChatGPT Got Wrong or Overstated
1. **6-month interest cost overstated by ~$600.** ChatGPT said ~$3,000-3,200. Actual amortization table shows ~$2,413.
2. **Remaining LOC balance overstated.** ChatGPT said ~$8,600-8,800. Actual: ~$7,985.
3. **Never modeled the moment the $10K arrives at month 6.** This is the most important event in the plan.
4. **"Sellability" framing was premature.** Noise at this stage — the priority is cash flow management.

---

## Independent Amortization: $10K LOC Over 6 Months

Monthly rate: 52.4% / 12 = 4.367%

| Month | Balance Start | Interest | Principal | Balance End |
|-------|-------------|----------|-----------|-------------|
| 1     | $10,000     | $437     | $301      | $9,699      |
| 2     | $9,699      | $424     | $314      | $9,385      |
| 3     | $9,385      | $410     | $328      | $9,057      |
| 4     | $9,057      | $396     | $342      | $8,715      |
| 5     | $8,715      | $381     | $357      | $8,358      |
| 6     | $8,358      | $365     | $373      | $7,985      |

**Total LOC payments:** $4,428
**Total LOC interest:** ~$2,413
**Remaining balance at month 6:** ~$7,985

---

## Monthly Cash Flow Comparison

|                  | Before    | After     |
|------------------|-----------|-----------|
| Hosting          | $2,000 (Flywheel) | $0 (paid annually) |
| LOC payment      | $0        | $738      |
| CC minimums      | ~$810 (3% of $27K) | ~$750 (3% of $25K) |
| **Total outflow** | **~$2,810** | **~$1,488** |

**Net monthly improvement: ~$1,322/month**

---

## 6-Month Cost/Benefit Analysis

### Cost side (months 1-6)
| Item | Amount |
|------|--------|
| LOC payments (6 x $738) | $4,428 |
| Of which is interest | ~$2,413 |
| CC interest (6 x $583) | ~$3,498 |
| **Total interest cost** | **~$5,911** |

### Benefit side (months 1-6)
| Item | Amount |
|------|--------|
| Flywheel eliminated (6 x $2,000) | $12,000 saved |
| Freed cash flow (6 x ~$1,322) | ~$7,932 available |

---

## What Happens at Month 6 (Pressable $10K Arrives)

- LOC balance: ~$7,985
- Pay off LOC completely: -$7,985
- **Remaining from $10K: ~$2,015** toward credit cards
- Total CC reduction by month 6: $2,000 (initial) + redirected freed cash + $2,015

---

## Do-Nothing Comparison (6 Months)

**If you do nothing:**
- Flywheel: $12,000
- CC interest: ~$3,774 ($27K x 28%/12 x 6)
- **Total bleed: ~$15,774**

**If you execute the plan:**
- LOC payments: $4,428
- CC interest: ~$3,498
- **Total cost: ~$7,926**
- Then $10K arrives, wipes LOC, surplus to cards

**Savings vs. doing nothing: ~$7,800 over 6 months.**

---

## Month-by-Month Debt Tracker

Assumes ~$1,000/month of freed cash redirected toward credit cards (conservative — $1,322 freed but some goes to operations).

### Execute the Plan

| Month | LOC Balance | CC Balance | Total Debt | Monthly Outflow | Notes |
|-------|------------|------------|------------|-----------------|-------|
| **0 (Start)** | $10,000 | $25,000 | **$35,000** | — | Borrow $10K. $8K→Pressable, $2K→cards |
| **1** | $9,699 | $24,583 | **$34,282** | $1,488 | $738 LOC + $750 CC min. ~$1K freed→cards |
| **2** | $9,385 | $24,156 | **$33,541** | $1,488 | |
| **3** | $9,057 | $23,719 | **$32,776** | $1,488 | |
| **4** | $8,715 | $23,271 | **$31,986** | $1,488 | |
| **5** | $8,358 | $22,812 | **$31,170** | $1,488 | |
| **6** | $0 | $20,797 | **$20,797** | — | $10K arrives. Pay off LOC ($7,985). $2,015→cards |

### Do Nothing (Comparison)

| Month | LOC Balance | CC Balance | Total Debt | Monthly Outflow | Notes |
|-------|------------|------------|------------|-----------------|-------|
| **0** | $0 | $27,000 | **$27,000** | — | |
| **1** | $0 | $27,000 | **$27,000** | $2,810 | Minimums barely cover interest |
| **2** | $0 | $27,000 | **$27,000** | $2,810 | |
| **3** | $0 | $27,000 | **$27,000** | $2,810 | |
| **4** | $0 | $27,000 | **$27,000** | $2,810 | |
| **5** | $0 | $27,000 | **$27,000** | $2,810 | |
| **6** | $0 | $27,000 | **$27,000** | $2,810 | CC balance stays flat — no progress |

### Side-by-Side at Month 6

| | Do Nothing | Execute Plan |
|--|-----------|-------------|
| Total debt | $27,000 | **$20,797** |
| Debt reduced | $0 | **$6,203** |
| Total paid out (6 months) | ~$16,860 | ~$8,928 |
| Hosting paid through | Month-to-month | 12 months |

You enter month 7 with **$6,200 less debt**, **$8,000 less spent**, and **a full year of hosting already paid for**.

---

## CC Paydown Scenarios (Freed Cash Redirection)

All three scenarios share the same LOC amortization. The difference is how much of the freed ~$1,322/month goes toward credit cards. CC interest rate: ~28% APR (2.333%/month).

### Scenario A: Minimum Only ($750/mo to CC)

| Month | LOC Balance | CC Balance | Total Debt | Monthly Outflow |
|-------|------------|------------|------------|-----------------|
| **0** | $10,000 | $25,000 | **$35,000** | — |
| **1** | $9,699 | $24,833 | **$34,532** | $1,488 |
| **2** | $9,385 | $24,662 | **$34,047** | $1,488 |
| **3** | $9,057 | $24,487 | **$33,544** | $1,488 |
| **4** | $8,715 | $24,308 | **$33,023** | $1,488 |
| **5** | $8,358 | $24,125 | **$32,483** | $1,488 |
| **6** | $0 | $21,923 | **$21,923** | — |

CC barely moves. Minimums mostly cover interest. Pressable surplus ($2,015) provides the only real CC hit.

### Scenario B: +$750 Extra ($1,500/mo to CC)

| Month | LOC Balance | CC Balance | Total Debt | Monthly Outflow |
|-------|------------|------------|------------|-----------------|
| **0** | $10,000 | $25,000 | **$35,000** | — |
| **1** | $9,699 | $24,083 | **$33,782** | $2,238 |
| **2** | $9,385 | $23,145 | **$32,530** | $2,238 |
| **3** | $9,057 | $22,185 | **$31,242** | $2,238 |
| **4** | $8,715 | $21,203 | **$29,918** | $2,238 |
| **5** | $8,358 | $20,197 | **$28,555** | $2,238 |
| **6** | $0 | $17,153 | **$17,153** | — |

### Scenario C: +$1,000 Extra ($1,750/mo to CC)

| Month | LOC Balance | CC Balance | Total Debt | Monthly Outflow |
|-------|------------|------------|------------|-----------------|
| **0** | $10,000 | $25,000 | **$35,000** | — |
| **1** | $9,699 | $23,833 | **$33,532** | $2,488 |
| **2** | $9,385 | $22,639 | **$32,024** | $2,488 |
| **3** | $9,057 | $21,417 | **$30,474** | $2,488 |
| **4** | $8,715 | $20,167 | **$28,882** | $2,488 |
| **5** | $8,358 | $18,888 | **$27,246** | $2,488 |
| **6** | $0 | $15,563 | **$15,563** | — |

### All Scenarios at Month 6

| | Do Nothing | Min Only | +$750 | +$1,000 |
|--|-----------|----------|-------|---------|
| CC Balance | $27,000 | $21,923 | $17,153 | $15,563 |
| LOC Balance | $0 | $0 | $0 | $0 |
| **Total Debt** | **$27,000** | **$21,923** | **$17,153** | **$15,563** |
| Debt Reduced | $0 | $5,077 | $9,847 | $11,437 |
| Monthly Outflow | $2,810 | $1,488 | $2,238 | $2,488 |
| vs. Do Nothing | — | -$1,322/mo | -$572/mo | -$322/mo |

Even the most aggressive scenario (+$1,000) still costs **$322/month less** than doing nothing. You pay less AND destroy debt faster.

---

## Final Verdict

**The deal still works.** The 6-month delay costs ~$2,400 in LOC interest that wouldn't exist if the $10K came immediately. But you're trading $2,400 in extra interest to eliminate $12,000 in Flywheel payments — roughly a **5:1 return on the carry cost.**

After month 6: no Flywheel, no LOC balance, reduced CC debt.

### The One Risk
If the freed ~$1,300/month gets absorbed into operations instead of attacking credit cards, the arbitrage benefit evaporates. The plan only compounds if the freed cash is redirected to debt reduction.

### Key Numbers to Remember (REVISED — Pressable purchased at $6,600)
- Monthly improvement: ~$1,364
- 6-month LOC carry cost: ~$2,413
- 6-month Flywheel savings: $12,000
- LOC balance when $10K arrives: ~$7,985
- Surplus after LOC payoff: ~$2,015
- Starting CC balance: $23,600 (was $25,000)
- Extra CC principal hit on day one: $1,700 more than planned

---

## Revised Scenario Tables (Pressable at $6,600)

Starting CC balance: $23,600 ($27K - $3,400 from LOC). CC interest: ~28% APR.

### Updated Monthly Cash Flow

|                  | Before    | After (Revised) |
|------------------|-----------|-----------------|
| Hosting          | $2,000 (Flywheel) | $0 (paid annually) |
| LOC payment      | $0        | $738      |
| CC minimums      | ~$810 (3% of $27K) | ~$708 (3% of $23.6K) |
| **Total outflow** | **~$2,810** | **~$1,446** |

**Net monthly improvement: ~$1,364/month**

### Revised Month 6 Comparison

| | Do Nothing | Min Only | +$750 | +$1,000 |
|--|-----------|----------|-------|---------|
| CC Balance | $27,000 | $20,323 | $15,553 | $13,963 |
| LOC Balance | $0 | $0 | $0 | $0 |
| **Total Debt** | **$27,000** | **$20,323** | **$15,553** | **$13,963** |
| Debt Reduced | $0 | $6,677 | $11,447 | $13,037 |

The $1,700 savings on Pressable flows through as ~$1,600 better CC position at month 6 across every scenario.
