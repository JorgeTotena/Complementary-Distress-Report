# 8020REI — Platform Reference

The 8020REI platform is a suite of six interconnected applications that power the business from lead acquisition through onboarding, operations, analytics, and partner growth. All apps share a central BigQuery data warehouse and Firebase authentication.

---

## Platform Overview

| App | Domain | Purpose | Primary Users |
|-----|--------|---------|---------------|
| **Landing** | `booking.8020rei.com` | Lead capture and demo booking | Prospective investors |
| **Feedback Loop** | `feedback.8020rei.com` | Data sharing education and onboarding | Active clients |
| **Ops Hub** | `opshub.8020rei.com` | Internal operations command center | 8020REI team |
| **Analytics** | `team.8020rei.com` | AI-driven BI dashboard | 8020REI team |
| **Affiliates** | `affiliates.8020rei.com` | Partner referral program portal | Affiliates and admins |
| **Apps Script** | _(serverless)_ | Data sync and automation backbone | Automated / internal |

---

## Client Lifecycle Flow

```
Prospect discovers 8020REI
        |
        v
  [ Landing ]  --> Lead capture, qualification, demo booking
        |
        v
  Client signs up
        |
        v
  [ Feedback Loop ]  --> Educates client on data sharing to improve targeting
        |
        v
  Client operates monthly
        |
        v
  [ Ops Hub ]  --> Team manages fulfillments, support, client health
  [ Analytics ]  --> Team analyzes performance, KPIs, trends
        |
        v
  Happy client refers others
        |
        v
  [ Affiliates ]  --> Partner earns recurring commissions on referrals
```

---

## 1. Landing — `booking.8020rei.com`

**What it does:** Top-of-funnel acquisition engine. Captures and qualifies leads from real estate investors interested in 8020REI services.

**Who uses it:** Prospective investors (the form), marketing team (A/B testing and campaign analytics), sales team (lead follow-up).

**How it fits in the lifecycle:** Every new client starts here. Investors land on the page via ads, referrals, or organic search and fill out a short qualification form (name, email, phone, deals closed, referral source). The system scores lead quality based on deal volume. Qualified leads (11+ deals/year) are routed to a Calendly booking page for a demo call. All leads are synced to Salesmate CRM and tracked in BigQuery.

**Key capabilities:** Lead quality scoring (spam/low/medium/high), A/B testing framework, server-side Meta Conversions API for ad attribution, duplicate detection to avoid re-contacting existing leads, admin dashboard for lead management.

---

## 2. Feedback Loop — `feedback.8020rei.com`

**What it does:** Educates clients on how sharing their deal outcomes makes 8020REI's targeting algorithm work better for them. Facilitates the data sharing that powers the Feedback Loop competitive advantage.

**Who uses it:** Active clients (to understand and set up data sharing), Customer Success team (to facilitate integrations).

**How it fits in the lifecycle:** Immediately after signup, clients are introduced to the Feedback Loop concept. This app walks them through the Share-Optimize-Target-Close cycle and helps them set up their preferred data sharing method.

**Data sharing methods:**
- **CRM integration** — Automated sync from Salesforce, Podio, Left Main REI, or REsimpli
- **Manual upload** — Download a Google Sheets template, fill in monthly results, submit

**Data categories collected:** Results (deals closed, leads generated, appointments set), opt-outs (dead leads, litigators, Do Not Mail/Call/SMS), number status (wrong numbers, DNC, decision makers).

---

## 3. Ops Hub — `opshub.8020rei.com`

**What it does:** Central command center for 8020REI's internal operations. This is where the team runs the business day-to-day — managing fulfillments, monitoring client health, handling support, and tracking performance.

**Who uses it:** Operations team, account managers, Customer Success, leadership, HR, product team.

**How it fits in the lifecycle:** Once a client is active, Ops Hub is the internal system of record for managing that client relationship. CSMs use it for engagement tracking, fulfillment management, and BuyBox configuration. It connects marketing campaign data with deal outcomes to answer "which efforts actually generate revenue?"

**Key capabilities:**
- **Campaign Analytics** — Performance by channel (Direct Mail, SMS, Cold Calling) with trend analysis
- **Client Management** — Investor profiles with health scores, engagement tracking, billing history, support tickets, and BuyBox configuration (10-tab comprehensive view)
- **Property Intelligence** — Search, filter, and map properties with marketing history and distress indicators
- **Customer Success** — Active client monitoring, SLA tracking, churn analytics, fulfillment performance
- **Support Integration** — Freshdesk ticket tracking with SLA monitoring
- **Hiring Pipeline** — TeamTailor integration for recruiting analytics
- **Product Tracking** — Jira integration for bug and feature tracking
- **Learning Management** — Internal training platform (8020 Learn) with courses and progress tracking
- **Admin Panel** — User management with 47 granular permissions, audit logging, role-based access

---

## 4. Analytics — `team.8020rei.com`

**What it does:** AI-driven business intelligence dashboard with 80+ pages of interactive charts, KPIs, and drill-down reports. All queries run in-browser with sub-second response times.

**Who uses it:** Leadership, department heads, analysts — anyone who needs data-driven answers.

**How it fits in the lifecycle:** The strategic decision-making layer. Analytics doesn't interact with clients directly. It aggregates data from every other app and external source to provide a unified view of business performance across sales, marketing, CS, fulfillment, people, and finance.

**Key dashboards:**
- **Executive Overview** — Company-wide KPIs, revenue trends, pipeline health
- **Sales** — Deal pipeline, win rates, MRR analysis, rep performance
- **Marketing** — Ad spend, lead generation, campaign ROI, channel attribution
- **Customer Success** — Client health scores, churn risk, NPS, engagement metrics
- **Fulfillment** — Delivery performance, volume trends, SLA compliance
- **People** — Hiring pipeline, team capacity, employee engagement
- **Finance** — Revenue, expenses, profitability, forecasting

**Special features:** Merlin AI (in-app assistant that answers questions about any dashboard data), weighted KPI scorecard, cross-filter system with global date range and custom filter propagation.

---

## 5. Affiliates — `affiliates.8020rei.com`

**What it does:** Full-featured partner referral program where affiliates earn recurring monthly commissions by referring real estate investors to 8020REI.

**Who uses it:** Partner affiliates (their dashboard), internal affiliate program managers (admin portal).

**How it fits in the lifecycle:** Growth engine at the end of the client lifecycle. Happy clients and industry partners refer new investors through custom referral links. When a referral becomes a paying client, the affiliate earns a flat **10% of the referred client's monthly recurring revenue**, paid monthly via Gusto payroll. There are no commission tiers — every affiliate earns the same 10% rate regardless of referral volume.

**Affiliate portal features:** Real-time earnings dashboard, client list with MRR details, commission history and tax summaries, custom referral link builder with QR codes, marketing asset library, leaderboard and achievement badges, getting-started guides.

---

## 6. Apps Script — Serverless Automation Backbone

**What it does:** The invisible engine that keeps everything running. Syncs data from 12+ business systems into BigQuery, runs AI-powered analysis, executes business audits, and sends notifications. Every other app depends on the data it collects and transforms.

**Who uses it:** Runs automatically on schedules ranging from every 5 minutes to daily. Operations team monitors via Slack alerts.

**How it fits in the lifecycle:** Apps Script is the connective tissue. It pulls data from Salesmate CRM, Fathom call recordings, Freshdesk tickets, Jira issues, ChargeOver billing, QuickBooks accounting, Meta Ads, Google Ads, and more — transforming and loading it into BigQuery so that Ops Hub, Analytics, Affiliates, and Landing all have current data.

**What it automates:**
- **Data synchronization** — CRM, billing, ads, support, accounting, and more synced to BigQuery
- **AI analysis** — Gemini-powered client health scoring, sales call QA evaluation, engagement prep notes
- **Business audits** — Revenue checks, overdue tracking, calendar availability, candidate pipeline summaries delivered via Slack
- **Workflow orchestration** — Webhook-triggered workflows for new client onboarding, call preparation, and CRM note publishing
