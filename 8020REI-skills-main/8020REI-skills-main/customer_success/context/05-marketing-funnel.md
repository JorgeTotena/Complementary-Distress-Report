# 8020REI Marketing Funnel

> Complete lead flow from traffic source to conversion. Reference for analytics, attribution, and reporting.

## Traffic Sources → Form Pages

| Traffic Source | Landing Page | Form Fields | Form ID | UTM Expected |
|---|---|---|---|---|
| Google/Meta paid ads | `/landing` | 4 (name, email, phone, deals) | `landing_old_form` | Yes |
| Competitor-targeted ads | `/landing/competitors` | 4 (name, email, phone, deals) | `competitor_form` | Yes |
| Organic / Direct / Website CTAs | `/form` | 5 (+ "How did you hear about us?") | `demo_form` | Sometimes |

All forms use the same `LeadForm` component (`src/components/lead-form.tsx` in the landing repo). The only differences are field count and form ID.

Every "Book a Demo" CTA across the website (pricing, features, compare, integrations, testimonials, header nav) links to `/form`. No page links directly to `/demo`.

## Qualification Logic

The qualification threshold is **11+ deals closed**. This is checked client-side after form submission.

| Deals Closed | Qualified? | Destination |
|---|---|---|
| 0 (first deal) | No | `/thank-you` |
| 1-10 | No | `/thank-you` |
| 11-20 | Yes | `/demo` |
| 21-50 | Yes | `/demo` |
| 51-100 | Yes | `/demo` |
| 101+ | Yes | `/demo` |

**Important:** The 11-deal threshold is internal only. Public messaging uses "50+ deals/year" and "$15k+/month outbound" as the ICP benchmark.

## Funnel Stages

```
Traffic → Form Page → Form Submit → Qualification → Destination → Conversion
```

### Full Flow

```
TRAFFIC
  │
  ├── Paid Ads (UTM) ──────────→ /landing (4 fields)
  ├── Competitor Ads (UTM) ────→ /landing/competitors (4 fields)
  └── Organic / Website CTA ───→ /form (5 fields)
                                      │
                                      ▼
                              FORM SUBMISSION
                              (POST /api/leads-v2)
                                      │
                            ┌─── 11+ deals? ───┐
                            │                   │
                           YES                  NO
                            │                   │
                            ▼                   ▼
                         /demo              /thank-you
                      (Calendly)         (educational page,
                            │             Skool community link)
                            │                  END
                      User books call
                            │
                            ▼
                    /thank-you-booking
                   (confirmation page)
                           END
```

## Route Redirects (301)

| Old Route | New Route | Context |
|---|---|---|
| `/landing_old` | `/landing` | Consolidated landing page |
| `/landing_old_competitors` | `/landing/competitors` | Moved under `/landing/` namespace |
| `/book-call` | `/demo` | URL simplification |

## Events Tracked Per Stage

| Funnel Stage | Event Name | Trigger |
|---|---|---|
| Page view | `page_view` | Any page load |
| Form started | `form_started` | First field interaction |
| Form submitted (qualified) | `form_submitted_qualified` | 11+ deals, form submit |
| Form submitted (unqualified) | `form_submitted_unqualified` | <11 deals, form submit |
| Form abandoned | `form_abandoned` | Page unload with partial form |
| Demo page viewed | `demo_page_viewed` | `/demo` page load |
| Booking confirmed | `booking_confirmation_viewed` | Calendly success callback |

Events are stored in BigQuery `user_events` table, partitioned by timestamp, clustered by `user_id`, `event_type`, `lead_id`.

## Conversion Values (Tracking Tiers)

| Deals Closed | Google Ads Value | Meta Event Name | Meta CAPI CompleteRegistration | Calendly/Purchase Value |
|---|---|---|---|---|
| 0-10 | $0 | FormSubmitted0to10 | -- | -- |
| 11-20 | $250 | FormSubmitted11to20 | $250 | $1,000 |
| 21-50 | $500 | FormSubmitted21to50 | $500 | $5,000 |
| 51-100 | $1,000 | FormSubmitted50Plus | $1,000 | $10,000 |
| 101+ | $1,000 | FormSubmitted50Plus | $1,000 | $10,000 |

## Meta CAPI Events

Server-side conversion events sent alongside browser pixel for deduplication:

| Event | Trigger | Event ID Pattern |
|---|---|---|
| `CompleteRegistration` | Qualified form submit (11+ deals), fired on `/demo` load | `{lead_id}_cr` |
| `Purchase` | Booking confirmation | `{lead_id}_purchase` |

Deduplication: Browser pixel and server both use the same `event_id`. Meta deduplicates matching `event_name` + `event_id` within 48 hours.

## Attribution Fields (BigQuery)

Every lead record includes:

- `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`
- `gclid` (Google), `fbclid` (Meta), `msclkid` (Microsoft), `ttclid` (TikTok)
- `landing_page_url`, `landing_page_path`
- `referrer_url`, `referrer_domain`, `initial_referral_domain`
- `form_id`, `form_type`

## Key Metrics for Reporting

| Metric | How to Calculate |
|---|---|
| Form conversion rate | `form_submitted / page_view` (per form page) |
| Qualification rate | `form_submitted_qualified / (form_submitted_qualified + form_submitted_unqualified)` |
| Booking rate | `booking_confirmation_viewed / demo_page_viewed` |
| Full funnel rate | `booking_confirmation_viewed / page_view` (per form page) |
| Cost per qualified lead | Ad spend / `form_submitted_qualified` count |
| Cost per booking | Ad spend / `booking_confirmation_viewed` count |

## Integrations Downstream

| System | When | Blocking? |
|---|---|---|
| BigQuery | Lead stored on form submit | Yes (primary store) |
| Salesmate CRM | Auto-sync after BigQuery insert | No (fire-and-forget) |
| Meta CAPI | Server-side event on qualified submit + booking | No (fire-and-forget) |
| Slack alerts | Notification on form submit | No |
| Microsoft Clarity | Session tagging throughout funnel | No (client-side) |

---

*Source: 8020REI-landing repo. Last updated: 2026-03-07.*
