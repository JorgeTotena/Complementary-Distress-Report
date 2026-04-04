# 8020REI CSM Skills

> This folder is a skill package for Customer Success Managers at 8020REI. It contains everything needed to communicate professionally, create reports, and serve clients effectively.

---

## What This Is

This is a portable skill package that gives any CSM — or any AI assistant acting on behalf of a CSM — the full operating context needed to do the job well. It is designed to be loaded into a Claude Project, dropped into a conversation as context, or read sequentially by a new team member.

The package contains:

- **Company context** — What 8020REI does, our ideal customer profile, our products, and how the platform works end to end.
- **Communication standards** — How we think before we write, how we structure arguments, and how we ensure every message has a point.
- **Design system** — How reports should look: typography, color, layout, components, and the pre-send quality checklist.
- **Report templates** — Starting-point HTML files for the most common report types, ready to populate with client data.
- **Brand assets** — Logos in light and dark variants, icon and full wordmark versions.

Everything here is opinionated by design. We follow the Pyramid Principle, MECE structure, and McKinsey-standard visual formatting because these patterns produce clear, trustworthy communication. There is no room for decoration without meaning.

---

## How to Use This

### For CSMs

1. **Start with context.** Read the files in `context/` to build a deep understanding of the business — what we sell, how the platform works, how deals flow from lead to close, how CS operates day-to-day, how marketing brings in leads, and what our terminology means.

2. **Learn the communication framework.** Read `standards/DESIGN_SYSTEM.md`, especially Part I (Communication Framework). This is not optional. The Pyramid Principle and MECE thinking are the foundation of every report, email, and client conversation you produce.

3. **Before every client interaction, answer the 5 mandatory questions.** Before you write a report, prep for a call, or draft an email:
   - What is the single most important message?
   - Who is the audience and what do they need to decide?
   - What are the 2-4 supporting arguments (MECE)?
   - What data proves each argument?
   - What is the recommended next step?

   If you cannot answer question 1 in one sentence, you are not ready.

4. **Use templates as starting points.** The `templates/` folder contains HTML report templates for every report type (general, fulfillment, BuyBox audit, health alert, onboarding summary). Open the right one, replace the placeholder content with real client data, and follow the design system rules for formatting. See `example-report.html` for what a completed report looks like.

5. **Print the quick-reference card.** Keep `quick-reference.html` on your desk or pinned — it has the 5 questions, health score thresholds, KPI targets, escalation path, and language guide on one page.

6. **Use the call prep worksheet.** Before every client call, print `call-prep.html` and fill it in. The 5 mandatory questions become a habit when they're on paper in front of you.

### For AI Assistants (Claude)

When this folder is loaded as project context, follow these rules:

- **Use `context/` files** to understand 8020REI's business, products, ICP, deal pipeline, CS operations, marketing funnel, and terminology. Ground every response in this knowledge — never invent facts about the company or its products.
- **Use `standards/DESIGN_SYSTEM.md` for ALL report generation.** Follow the Pyramid Principle, MECE structure, and action title rules strictly. Every page title must be a full sentence stating the takeaway. Every report must lead with the conclusion.
- **Use `standards/report.css`** as the CSS framework for HTML reports. Include it inline in the `<style>` tag of every generated report.
- **Use `logos/`** for brand assets in reports. Use `logo-full-light.png` for cover pages on white backgrounds. Use `logo-icon-light.png` for page headers on subsequent pages.
- **Use `templates/`** as structural references when generating reports. Match their structure and component usage.
- **Save all generated reports to `clients/`**. Every client gets a subfolder (e.g., `clients/summit-property-group/`). Place finished HTML reports in the client's folder. Read the client's `context.md` file before generating any report — it contains the running account context that grounds your output in reality.

---

## Client Folder Structure

The `clients/` folder is the structural backbone of how we organize all client work. Every client gets their own subfolder, and inside that subfolder lives a `context.md` file and all generated reports.

```
clients/
  summit-property-group/
    context.md                 ← Running account context (read before every report)
    2026-03-engagement.html    ← Generated reports live here
    2026-02-fulfillment.html
  acme-investments/
    context.md
    2026-03-buybox-audit.html
```

### The `context.md` File

Every client folder **must** contain a `context.md` file. This is the living document that captures everything an AI or CSM needs to know about the account before producing any output. It is the structural memory of the client relationship.

**What goes in `context.md`:**

- **Account overview** — Who the client is, what markets they operate in, their current plan/tier, and their primary goals.
- **Key contacts** — Names, roles, and communication preferences of the people we interact with.
- **Current BuyBox configuration** — Active counties, filters, and targeting criteria.
- **Health status** — Current health score, trend direction, and any flags or risks.
- **Recent activity** — Last contact date, last delivery, open support tickets, recent changes.
- **Historical notes** — What has worked, what has not, decisions made and why, escalation history.
- **CSM assignment** — Who owns the account and the current engagement cadence.

**Rules for `context.md`:**

1. **Update after every client interaction.** Every call, every report, every delivery should leave a trace in `context.md`. If it is not written down, it did not happen.
2. **AI must read `context.md` before generating any report for that client.** This is non-negotiable. The context file prevents hallucination and ensures continuity between interactions.
3. **Use facts, not opinions.** "Health score dropped from 3.8 to 3.2 in February" is a fact. "Client seems unhappy" is not useful. Be specific.
4. **Date every entry.** When adding notes, include the date so the timeline is always clear.

### Report File Naming

Reports follow the pattern: `YYYY-MM-[type].html`

| Example | Meaning |
|---------|---------|
| `2026-03-engagement.html` | March 2026 engagement report |
| `2026-03-fulfillment.html` | March 2026 fulfillment report |
| `2026-Q1-buybox-audit.html` | Q1 2026 BuyBox audit |
| `2026-03-health-alert.html` | March 2026 health alert |
| `2026-03-onboarding-summary.html` | March 2026 onboarding summary |

This naming convention ensures reports sort chronologically and are immediately identifiable by type.

---

## Report Generation Rules

These rules apply to every report, whether written by a person or generated by AI. No exceptions.

1. **Never generate a report without a clear conclusion.** The report title IS the conclusion. If you do not know the conclusion, ask for it before writing anything. A report without a point is not a report.

2. **Every page title must be a full sentence** — the takeaway, not a topic label. "Q1 Performance Overview" is wrong. "Client health improved in Q1, but 12 at-risk accounts need immediate intervention" is right.

3. **Follow the Pyramid Principle.** Answer first, then supporting arguments (MECE), then data evidence. Never build up to the conclusion — start with it.

4. **Format as HTML with inline CSS from report.css.** Each page is a `<section class="page">` with `page-break-after: always`. No external dependencies beyond Google Fonts for EB Garamond.

5. **Typography: Georgia for headlines, Helvetica/Arial for body.** No other fonts. Georgia conveys authority on headings. Helvetica conveys clarity on everything else. See the Design System for exact sizes and weights.

6. **Color is minimal and semantic.** `#1a1a1a` for text, `#0B5394` for accent, and status colors only when they carry meaning (green = good, amber = caution, red = bad). Never use color for decoration.

7. **No decorative elements.** No rounded corners, no shadows, no gradients, no emojis. Every visual element must serve a communication purpose. If it does not help the reader understand the message faster, remove it.

8. **Maximum 5 pages.** If a report needs more than 5 pages, the thinking is not sharp enough. Cut, consolidate, and prioritize. The constraint is the discipline.

9. **Every report ends with next steps.** Each next step includes three things: the action, the owner, and the date. "Improve engagement" is not a next step. "Schedule re-engagement call with Acme Corp (CSM: Maria, by March 15)" is.

10. **Print-ready output.** Every report must produce a clean PDF via browser Print (Save as PDF). Page breaks must fall between sections, never mid-sentence or mid-table. Test before sending.

---

## Communication Standards

### The 5 Questions (Before ANY Client Communication)

These five questions are mandatory before writing a report, preparing for a call, or drafting any client-facing message. They are the thinking framework that ensures every communication has a point.

| # | Question | Why It Matters |
|---|----------|----------------|
| 1 | **What is the single most important message?** | If you cannot say it in one sentence, you do not understand it yet. This becomes your report title or email opening line. |
| 2 | **Who is the audience and what do they need to decide?** | A report for an investor reads differently than one for a hands-on operator. Shape the depth, language, and emphasis for the reader. |
| 3 | **What are the 2-4 supporting arguments (MECE)?** | These become your page sections or talking points. If they overlap, combine them. If something is missing, add it. |
| 4 | **What data proves each argument?** | No argument without evidence. No evidence without an argument. Every number in the report must support a specific point. |
| 5 | **What is the recommended next step?** | Every communication ends with action. If there is nothing to do, the communication should not exist. |

### Tone and Voice

- **Professional but human.** We are consultants, not robots. Write in clear, direct English. Use "we" and "you." Avoid jargon unless speaking to a technical audience that expects it.
- **Direct.** Lead with the answer, not the preamble. The first sentence of any section should tell the reader what to think. The rest is evidence.
- **Evidence-based.** Every claim is backed by a number. "Engagement is strong" means nothing. "Engagement calls are at 94% on-time rate, up from 78% last quarter" means something.
- **Action-oriented.** Every communication ends with "here is what to do next." No report, email, or call ends without a clear recommended action with an owner and a timeline.
- **Never hide bad news.** If something is going wrong, address it head-on. State the problem, explain the root cause, and present a recovery plan. Clients respect honesty with a path forward. They do not respect being blindsided later.

### Number Formatting

Consistency in number formatting signals professionalism. Follow these rules in every report and communication:

- **Commas for thousands:** 1,234 not 1234. Always.
- **Currency:** $1,234 for exact figures. $1.2M or $45K for rounded large numbers.
- **Percentages:** One decimal maximum. Write 12.3%, not 12.3456%. Write 12% when the decimal adds no insight.
- **Always show comparison:** Every number should appear alongside a reference point — current vs. prior period, actual vs. target, or change over time. A number without context is just a number.

---

## Context Files Reference

The `context/` folder contains the business knowledge a CSM needs to operate. Each file covers a specific domain.

| File | What It Contains |
|------|------------------|
| `01-company-and-product.md` | What 8020REI is, the ideal customer profile, product features, competitive moats, and market positioning. |
| `02-platform.md` | The 6-app platform architecture and how the applications connect to serve the full real estate investment workflow. |
| `03-deal-pipeline.md` | The complete 8-phase deal flow from property identification to closed deal, including handoff points and key metrics at each stage. |
| `04-cs-operations.md` | CS team structure, the 13 core processes, KPIs, tools, engagement cadence, and escalation procedures. |
| `05-marketing-funnel.md` | How leads arrive — ad channels, referral programs, qualification logic, and conversion benchmarks. |
| `06-glossary.md` | Business and product terminology. Use this to ensure consistent language in all client communications. |

Read these in order. They build on each other. A CSM who has internalized these six files can speak fluently about any aspect of the business.

---

## Report Types

Each report type has a defined purpose, page count, and set of mandatory sections. Use the corresponding template in `templates/` as a starting point.

### Engagement Report (2-4 pages)
**When:** Before every client engagement call.
**Purpose:** Give the CSM and the client a clear picture of account health, recent activity, and what to discuss on the call.
**Mandatory sections:** Situation summary, key metrics with comparisons, recommendation, next steps.

### Fulfillment Report (1-2 pages)
**When:** Included with every monthly data delivery.
**Purpose:** Document what was delivered, confirm quality, and set expectations for the next cycle.
**Mandatory sections:** What was delivered (volume, scope), quality summary (match rate, accuracy), action items for the next period.

### BuyBox Audit (2-3 pages)
**When:** Quarterly, or when a client's targeting criteria need review.
**Purpose:** Evaluate whether the client's current buy box is producing results and recommend adjustments based on market data.
**Mandatory sections:** Current performance against targets, market analysis (supply, competition, pricing), recommended changes with rationale.

### Health Alert (1 page)
**When:** Immediately when a client enters at-risk status.
**Purpose:** Escalate the issue internally with a clear problem statement and recovery plan. One page forces precision.
**Mandatory sections:** What happened (the trigger), root cause analysis, recovery plan with owner and timeline.

### Onboarding Summary (2-3 pages)
**When:** At onboarding completion, before transitioning to ongoing engagement.
**Purpose:** Summarize the onboarding journey, document first results, and establish the ongoing success plan.
**Mandatory sections:** Journey summary (milestones completed), first results and early wins, ongoing plan with cadence and goals.

---

## Folder Structure

```
8020REI-CSM-Skills/
  CLAUDE.md                  ← You are here. Start here.
  context/
    01-company-and-product.md
    02-platform.md
    03-deal-pipeline.md
    04-cs-operations.md
    05-marketing-funnel.md
    06-glossary.md
  standards/
    DESIGN_SYSTEM.md         ← The full communication + design reference.
    report.css               ← Unified CSS framework for all HTML reports.
  templates/
    report.html              ← General report template (situation + recommendation).
    fulfillment-report.html  ← Monthly data delivery report.
    buybox-audit.html        ← Quarterly BuyBox performance review.
    health-alert.html        ← 1-page urgent escalation for at-risk clients.
    onboarding-summary.html  ← Onboarding completion and ongoing plan.
    quick-reference.html     ← 1-page CSM cheat sheet for daily use.
    call-prep.html           ← Printable worksheet for pre-call preparation.
    example-report.html      ← Worked example with realistic data (what "good" looks like).
  clients/                   ← All client work lives here.
    summit-property-group/
      context.md             ← Running account context (read before every report).
      2026-03-engagement.html
    acme-investments/
      context.md
      2026-03-buybox-audit.html
  logos/
    logo-full-light.png      ← Full wordmark, for white backgrounds.
    logo-full-dark.png       ← Full wordmark, for dark backgrounds.
    logo-icon-light.png      ← Icon only, for page headers on white.
    logo-icon-dark.png       ← Icon only, for dark backgrounds.
```
