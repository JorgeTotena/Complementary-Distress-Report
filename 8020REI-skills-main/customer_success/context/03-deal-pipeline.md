# Complete Process: From Property to Closed Deal with 8020REI

## General Overview

8020REI is a B2B SaaS platform that provides predictive and exclusive data to professional real estate investors (wholesalers). The model works as a **data-to-deals pipeline**: 8020REI identifies properties with the highest probability of sale, and the investor (client) executes the marketing, negotiation, and closing.

```
+---------------------------------------------------------------------------+
|                    COMPLETE CYCLE: PROPERTY -> DEAL                       |
|                                                                           |
|   8020REI (Data Provider)              Client (Wholesaler)               |
|   ----------------------------         ----------------------             |
|   1. Acquires county data        ->   4. Receives monthly list            |
|   2. Applies client's BuyBox     ->   5. Executes marketing              |
|   3. Generates scored lists      ->   6. Contacts sellers                |
|                                        7. Negotiates contracts            |
|                                        8. Assigns/Sells to buyer          |
|                                        9. Closes and collects             |
|                                        10. Reports results ->             |
|                                                                           |
|   < < < < < < < FEEDBACK LOOP < < < < < < < < < < < < < <                |
+---------------------------------------------------------------------------+
```

---

## Phase 1: Initial Setup (Onboarding)

### 1.1 The Investor Subscribes to 8020REI

The professional investor (ICP: 50+ deals/year, $10K+/month in marketing) discovers 8020REI and subscribes. The onboarding process is:

```
Registration at booking.8020rei.com
         |
         v
Meet the CSM (Customer Success Manager)
         |
         v
BuyBox Setup Call (define targeting criteria)
         |
         v
Onboarding Call (platform training + Feedback Loop)
         |
         v
First Data Delivery (~2 weeks later)
```

### 1.2 BuyBox Configuration

The **BuyBox** is the heart of the system. It defines exactly which properties the investor wants. It's configured during onboarding and refined over time.

| Parameter | Example |
|-----------|---------|
| **Price range** (estimated market value) | $80,000 - $300,000 |
| **Property type** | Single-family, multi-family |
| **Size** | 1,300+ sqft, 3-5 bedrooms |
| **Location** | Specific counties (exclusive) |
| **Distress signals** | Ownership 25+ years, absentee, tax delinquency |
| **Exclusions** | Corporations, trusts, already contacted |

### 1.3 County Exclusivity

8020REI limits the number of clients per county. Each county has a finite number of "seats" -- once filled, no competitor can subscribe to that market. **1,200+ protected counties.**

```
County A:  [Client 1] [Client 2] [FULL X]
County B:  [Client 3] [AVAILABLE] [AVAILABLE]
County C:  [Client 4] [Client 5] [FULL X]
```

**Why does it matter?** If your competitor uses BatchLeads or PropStream, both receive the same list. With 8020REI, YOU are the only one in your county with that intelligence.

---

## Phase 2: Data Generation (8020REI)

### 2.1 Data Acquisition

8020REI aggregates data from multiple sources:

```
County Records ---------+
Tax Assessors -----------+
Proprietary Sources -----+---> 8020REI Data Engine ---> AI Scoring
Public Records ----------+
Distress Data -----------+
```

### 2.2 Identifying Motivated Sellers (The 5 D's)

The system looks for property owners under pressure to sell:

| Signal | Description | Example |
|--------|-------------|---------|
| **Death** | Probate/succession properties where heirs want to liquidate | Owner deceased, heirs in another state |
| **Divorce** | Court-ordered disposition | Divorce decree forces sale |
| **Delinquency** | Tax liens, mortgage default, code violations | 3 years of unpaid taxes |
| **Downsizing** | Elderly owners in large homes | 25+ years of ownership, 3-5 BR, 1,300+ sqft |
| **Disrepair** | Deferred maintenance, vacant, condemned | Empty house, tall grass, broken windows |

### 2.3 Absentee Owner Levels

| Level | Definition | Motivation |
|-------|------------|------------|
| **Level 0** | Lives at the property | Low |
| **Level 1** | Mailing address in the same state but different from the property | Medium |
| **Level 2** | Mailing address out of state | High |

### 2.4 Triple AI Scoring

Each property receives three types of scores:

```
+---------------------------------------------------+
|              TRIPLE SCORE SYSTEM                   |
|                                                    |
|  1. BuyBox IQ                                      |
|     AI trained on the client's specific            |
|     CLOSED deals (not generic)                     |
|                                                    |
|  2. Distress Score                                 |
|     Based on seller motivation signals             |
|     (the 5 D's, equity, owner profile)             |
|                                                    |
|  3. Reverse Buy Box (TM)                           |
|     Identifies the 40% of opportunities that       |
|     traditional filters DON'T detect               |
|     ("Hidden Gems")                                |
+---------------------------------------------------+
```

### 2.5 Hidden Gems

Properties where the year built or last sale date is unknown in public records. Other providers ignore them because they can't estimate their value. 8020REI uses a proprietary AVM model to value them.

**Impact:** ~40% of client revenue comes from Hidden Gems. Less competition because nobody else sees them.

### 2.6 AVM (Automated Valuation Model)

```
vConfidenceScore >= 70?
         |
    +----+----+
    | YES     | NO
    v         v
  Vendor    Proprietary AVM
  AVM       (weighted regression)
             |
             +-- Lot size
             +-- Built area (sqft)
             +-- Bedrooms / Bathrooms
             +-- Year built
             +-- Market value (tax assessment)
```

### 2.7 Skip Tracing

Once properties are identified, 8020REI appends contact information:

- Phone numbers (cell, landline)
- Email addresses
- Additional contact information

Lists are delivered **marketing-ready** -- the client can start reaching out immediately.

### 2.8 Action Plans

Each property receives a channel assignment based on its score:

| Urgency Tier | Action | Channel |
|--------------|--------|---------|
| **High** (high score) | Immediate contact | Cold call + SMS |
| **Medium** | Nurturing campaign | Direct mail + follow-up |
| **Low** | Long-term list | Periodic mail |

---

## Phase 3: Data Delivery to the Client (Fulfillment)

### 3.1 Monthly Delivery

Each month, the client receives an updated list based on their BuyBox:

```
8020REI generates list --> AI Scoring --> Skip Trace --> Action Plans
                                                           |
                                                           v
                                                  DELIVERY TO CLIENT
                                                  +-- Property list
                                                  +-- Contact data
                                                  +-- Motivation scores
                                                  +-- Action plans by channel
                                                  +-- Valuation data
```

### 3.2 Data Refresh

| Aspect | Frequency |
|--------|-----------|
| Property data | Daily refresh |
| Distress signals | Continuous updates |
| Valuations | Monthly |
| Complete lists (fulfillment) | Monthly |

---

## Phase 4: The Client Executes Marketing

### 4.1 Marketing Channels

With the list in hand, the wholesaler executes multichannel marketing:

```
                    8020REI LIST
                         |
          +--------------+-----------------+
          |              |                 |
          v              v                 v
    +----------+   +----------+      +----------+
    | DIRECT   |   | COLD     |      | SMS /    |
    | MAIL     |   | CALLING  |      | TEXTING  |
    |          |   |          |      |          |
    | Persona- |   | Cold     |      | Persona- |
    | lized    |   | calls to |      | lized    |
    | letters  |   | owners   |      | texts    |
    +----+-----+   +----+-----+      +----+-----+
         |              |                 |
         +--------------+-----------------+
                        v
              LEADS (Responses)
```

### 4.2 Conversion Funnel (Industry Benchmarks)

```
Marketing Spend
      |
      v
Gross Leads -------------------- 100%
      |
      v  (30-36% conversion)
Qualified Leads ---------------- 30-36%
      |
      v  (50-60% conversion)
Appointments ------------------- 15-22%
      |
      v  (80% attendance)
In-person Meetings ------------- 12-17%
      |
      v  (22%+ close rate)
Contracts ---------------------- 3-4%
      |
      v  (<10% fallout)
Closed Deals ------------------- 2.5-3.5%
```

### 4.3 Optimal Contact Sequence

```
Day 1: SMS --> Day 2: SMS --> Day 3: Voicemail Drop --> Day 4-5: Call
                                                              |
                                                    14-30 day pause
                                                              |
                                                         Repeat cycle
```

**Speed-to-lead target: < 60 seconds.** The first to call has a massive advantage.

---

## Phase 5: Negotiation and Contract

### 5.1 Deal Analysis (4 Underwriting Lenses)

Before making an offer, the wholesaler evaluates the property under 4 primary exit strategies:

| Exit Strategy | Minimum Target Profit | Description |
|---------------|----------------------|-------------|
| **Wholesale** (assignment) | $20,000+ | Assign contract to investor buyer |
| **Wholetail** | $30,000+ | Buy, minimal cleanup, resell as-is |
| **Fix & Flip** | $50,000+ | Buy, renovate ($40-60K rehab), sell retail |
| **Novation** | $20,000-$30,000+ | List on MLS under novation agreement |

**Additional exit strategies used by clients:** Buy & Hold (rental income), Creative Financing (seller financing, lease options), Subject To (take over existing mortgage payments).

### 5.2 Deal Approval Process

```
Acquisition Manager (AM) records video of the deal
         |
         v
Underwriter reviews photos FIRST (without seeing the video)
         |
         v
Underwriter runs all 4 calculators independently
         |
         v
Underwriter watches the AM's video
         |
         v
Approval or counteroffer with adjusted pricing
```

### 5.3 Negotiation Techniques with the Seller

The approach is **seller-led discovery** -- collaborative, not adversarial:

```
1. AMPLIFY THE CURRENT PAIN
   "How many more sleepless nights is the price difference worth?"
                    |
                    v
2. PAINT THE FUTURE STATE
   "Imagine sitting in your living room, the house already sold,
    the bills paid. How does that feel?"
                    |
                    v
3. COST OF INACTION
   "My biggest fear is that we can't make this work.
    How many more missed birthdays is the extra money worth?"
```

### 5.4 Signing the Purchase Contract

The wholesaler signs a **purchase contract** with the seller at a below-market price. This contract includes an **assignment clause** that allows transferring it to a third party.

```
SELLER ---- Contract A->B ---- WHOLESALER (Investor)
   |                                    |
   |    Agreed price: $80,000          |   Market value: ~$120,000
   |    (below market)                 |   Available spread: ~$40,000
   +------------------------------------+
```

---

## Phase 6: Disposition (Selling the Deal)

### 6.1 Exit Strategy Selection

| Channel | Best For | Average Margin | Speed | Complexity |
|---------|----------|----------------|-------|------------|
| **Wholesale** (open house) | Volume, consistency | $38-40K | 2-4 weeks | Low |
| **Novation** | Retail price, no rehab | Higher per deal | 30-60 days | Medium |
| **Retail listing** (MLS) | Maximum theoretical price | Variable | 60-90+ days | High |
| **Build-to-Rent** | Recurring relationships | Lower per unit | Pre-sold | High |

### 6.2 Wholesale: The Most Common Process

```
+--------------------------------------------------------+
|                  WHOLESALE PROCESS                      |
|                                                         |
|  1. Contract signed with seller (A->B)                  |
|           |                                             |
|           v                                             |
|  2. Deal package preparation:                           |
|     - iGuide / Matterport 360                           |
|     - Professional photos + drone                       |
|     - Specific inspections                              |
|     - Complete analysis + comps                         |
|           |                                             |
|           v                                             |
|  3. Marketing to buyer network:                         |
|     - Blast to cash buyers list                         |
|     - Open house for investors                          |
|           |                                             |
|           v                                             |
|  4. Buyer selected:                                     |
|     - $10,000 earnest money (non-refundable)            |
|     - Non-cancellable contract                          |
|     - $1,000/day for late closing                       |
|           |                                             |
|           v                                             |
|  5. Contract assignment (B->C)                          |
|     - Wholesaler assigns their position to the buyer    |
|     - Collects assignment fee (price difference)        |
|           |                                             |
|           v                                             |
|  6. Title closing                                       |
|     - The buyer (C) closes directly                     |
|       with the seller (A)                               |
|     - Wholesaler receives their fee at closing          |
|                                                         |
|  RESULT: Assignment fee = ~$20,000-$40,000+             |
|  TIME: 2-4 weeks from contract                          |
|  RISK: Low (never takes ownership)                      |
+--------------------------------------------------------+
```

### 6.3 Novation: Alternative for Compressed Markets

```
SELLER ---- Novation Agreement ---- INVESTOR
    |                                        |
    |  Seller maintains title               |  Investor lists on MLS
    |  Signs all documents                  |  Finds retail buyer
    |                                        |  Coordinates photography and showings
    |                                        |
    +--------------- RETAIL BUYER -----------+
                         |
                    Direct closing

Investor earns: Spread between novation price and retail price
Average time: ~70 days
```

---

## Phase 7: Closing the Deal

### 7.1 Closing Flow

```
Buyer deposits earnest money ($10,000)
         |
         v
Title company verifies clean title
         |
         v
Buyer due diligence:
+-- Property inspection
+-- Title verification
+-- Zoning and permits review
+-- Financing confirmation
+-- Property insurance
         |
         v
Closing documents signed
         |
         v
Funds distributed:
+-- Seller receives agreed price
+-- Wholesaler receives assignment fee
+-- Title company receives fees
+-- Commissions (if applicable)
         |
         v
Title transferred to final buyer
```

### 7.2 Closing Control Metrics

| Mechanism | Detail |
|-----------|--------|
| Earnest money | $10,000 non-refundable, deposited in company account |
| Late closing fee | $1,000/day |
| Non-cancellable contract | Structured to make exit very difficult |
| Lender authorization | Buyer signs direct communication authorization |

**Result:** 95%+ closing rate on assigned contracts.

---

## Phase 8: The Feedback Loop (Competitive Advantage)

### 8.1 The Virtuous Cycle

The Feedback Loop is the **core differentiator** of 8020REI. It's a virtuous cycle where client results improve data quality:

```
    +------------------------------------------------------+
    |                                                       |
    |              FEEDBACK LOOP                            |
    |                                                       |
    |   +---------+         +----------+                    |
    |   |         |         |          |                    |
    |   | SHARE   |-------->| OPTIMIZE |                    |
    |   |         |         |          |                    |
    |   +----^----+         +----+-----+                    |
    |        |                   |                          |
    |        |                   v                          |
    |   +----+----+         +----------+                    |
    |   |         |         |          |                    |
    |   | CLOSE   |<--------| TARGET   |                    |
    |   |         |         |          |                    |
    |   +---------+         +----------+                    |
    |                                                       |
    +------------------------------------------------------+
```

| Step | Description |
|------|-------------|
| **1. SHARE** | Client reports monthly results: closed deals, bad contacts, opt-outs |
| **2. OPTIMIZE** | AI models learn from results, refine targeting criteria |
| **3. TARGET** | Next monthly list is more precise, with higher-probability leads |
| **4. CLOSE** | Better targeting = higher conversion rate, lower cost per deal |

### 8.2 Data the Client Shares

| Category | Data |
|----------|------|
| **Results** | Closed deals, leads generated, appointments scheduled |
| **Opt-Out** | Dead contacts, litigants, Do Not Mail/Call/SMS |
| **Number Status** | Wrong numbers, DNC, decision makers |

### 8.3 Integration Methods

```
Method 1: CRM Integration (automated)
+-- Salesforce
+-- Podio
+-- Left Main REI
+-- REsimpli
    -> Automatic monthly sync

Method 2: Manual Upload
+-- Download Google Sheets template
+-- Fill in monthly results
+-- Upload at feedback.8020rei.com
```

### 8.4 Feedback Loop Impact

```
MONTH 1:   Generic list based on initial BuyBox
           Conversion: baseline
                |
MONTH 3:   AI learns from 2 months of results
           Conversion: +10-15%
                |
MONTH 6:   BuyBox IQ trained on client's actual deals
           Conversion: +25-30%
                |
MONTH 12+: Mature model, compounding data
           Conversion: significantly higher
           Cost per deal: significantly lower
```

---

## Complete Pipeline Summary

```
======================================================================
                        COMPLETE PIPELINE
======================================================================

 8020REI                                      CLIENT (WHOLESALER)
 -------                                      ---------------------

 +------------------+
 | 1. DATA          |  County data, tax records,
 |    ACQUISITION   |  distress signals, public records
 +--------+---------+
          |
 +--------v---------+
 | 2. APPLY         |  Filter properties based on
 |    BUYBOX        |  client-specific criteria
 +--------+---------+
          |
 +--------v---------+
 | 3. TRIPLE AI     |  BuyBox IQ + Distress Score +
 |    SCORING       |  Reverse Buy Box (TM)
 +--------+---------+
          |
 +--------v---------+
 | 4. SKIP TRACE    |  Add phones, emails,
 |    + ACTION PLAN |  assign marketing channels
 +--------+---------+
          |
 +--------v---------+
 | 5. DELIVERY      |  Monthly list ready for
 |    (FULFILLMENT) |  marketing
 +--------+---------+
          |
          |======================================|
          |                                      |
          |                             +--------v---------+
          |                             | 6. MULTICHANNEL  |
          |                             |    MARKETING     |
          |                             |    Mail+Call+SMS |
          |                             +--------+---------+
          |                                      |
          |                             +--------v---------+
          |                             | 7. QUALIFY       |
          |                             |    LEADS         |
          |                             |    Responses ->  |
          |                             |    Appointments  |
          |                             +--------+---------+
          |                                      |
          |                             +--------v---------+
          |                             | 8. NEGOTIATE     |
          |                             |    CONTRACT      |
          |                             |    Price < mkt   |
          |                             +--------+---------+
          |                                      |
          |                             +--------v---------+
          |                             | 9. DISPOSITION   |
          |                             |    Wholesale /   |
          |                             |    Novation /    |
          |                             |    Flip          |
          |                             +--------+---------+
          |                                      |
          |                             +--------v---------+
          |                             | 10. CLOSING      |
          |                             |     Title co.    |
          |                             |     Fee collected|
          |                             +--------+---------+
          |                                      |
          |              +-----------------------+
          |              |
 +--------v--------------v--+
 | 11. FEEDBACK LOOP        |
 |     Client reports       |
 |     results -> AI        |
 |     improves next list   |
 +--------+-----------------+
          |
          |  Each month, the cycle repeats with smarter data
          |
          v
       REPEAT

======================================================================
```

---

## Quick Glossary

| Term | Definition |
|------|-----------|
| **BuyBox** | Investor's targeting criteria (price, type, location, distress) |
| **BuyBox IQ** | AI trained on the specific client's closed deals |
| **Reverse Buy Box (TM)** | Algorithm that finds the 40% of opportunities traditional filters miss |
| **Hidden Gems** | Properties with incomplete data that other providers can't value |
| **Skip Tracing** | Process of appending contact data (phone, email) to property owner records |
| **AVM** | Automated Valuation Model -- automatic property valuation model |
| **Assignment Fee** | The wholesaler's profit: difference between contract price and buyer's price |
| **Novation** | Agreement where the investor lists the property on MLS without taking ownership |
| **CSM** | Customer Success Manager -- client success manager at 8020REI |
| **Fulfillment** | Monthly delivery of data/lists to the client |
| **Earnest Money** | Buyer's deposit as a good-faith guarantee ($10K typical) |
| **Title Company** | Company that verifies clean title and facilitates closing |
| **Distress Signals** | Seller motivation indicators (the 5 D's) |
| **MRR** | Monthly Recurring Revenue -- recurring monthly income from subscriptions |

---

> **Sources:** 8020REI internal documentation: `docs/BUSINESS_CONTEXT.md`, `docs/PLATFORM.md`, `docs/GLOSSARY.md`, `docs/DATA_SCHEMA.md`, and knowledge base in `docs/real-estate/`.
