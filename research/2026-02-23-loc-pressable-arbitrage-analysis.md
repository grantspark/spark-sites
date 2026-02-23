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

## Final Verdict

**The deal still works.** The 6-month delay costs ~$2,400 in LOC interest that wouldn't exist if the $10K came immediately. But you're trading $2,400 in extra interest to eliminate $12,000 in Flywheel payments — roughly a **5:1 return on the carry cost.**

After month 6: no Flywheel, no LOC balance, reduced CC debt.

### The One Risk
If the freed ~$1,300/month gets absorbed into operations instead of attacking credit cards, the arbitrage benefit evaporates. The plan only compounds if the freed cash is redirected to debt reduction.

### Key Numbers to Remember
- Monthly improvement: ~$1,322
- 6-month LOC carry cost: ~$2,413
- 6-month Flywheel savings: $12,000
- LOC balance when $10K arrives: ~$7,985
- Surplus after LOC payoff: ~$2,015
