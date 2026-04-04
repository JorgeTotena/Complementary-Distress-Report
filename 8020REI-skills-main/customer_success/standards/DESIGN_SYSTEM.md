# 8020REI Report & Communication System

> This is the canonical reference for all AI-generated reports, presentations, and documents at 8020REI. It defines how we think, how we communicate, and how we design — in that order.

> **The design exists to serve the message. If the message isn't clear, no amount of design will fix it.**

---

## Part I — Communication Framework

This section defines the thinking and communication standards every report must follow. No report should be generated without the author (or the AI) being able to answer the questions in this section first.

---

### 1. The Pyramid Principle (Barbara Minto)

Every report follows the Pyramid Principle: **lead with the answer, then support it.**

```
                    ┌─────────────┐
                    │  ANSWER     │  ← Start here. What is the one thing
                    │  (So What)  │    the reader needs to know?
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────┴─────┐ ┌───┴─────┐ ┌───┴─────┐
        │ Argument 1│ │Argument 2│ │Argument 3│  ← Supporting points
        │           │ │         │ │          │    (MECE)
        └─────┬─────┘ └────┬────┘ └────┬─────┘
              │            │           │
           [Data]       [Data]      [Data]       ← Evidence
```

**Rules:**

1. **The answer comes first.** Every page, every section, every report starts with the conclusion — not the data that led to it.
2. **Supporting arguments are MECE** — Mutually Exclusive (no overlap), Collectively Exhaustive (no gaps). If your three arguments overlap, you haven't thought clearly enough.
3. **Data supports arguments, not the other way around.** Data is evidence for a point, not the point itself. Never present data without saying what it means.

**In practice, this means:**

- The **report title** states the conclusion (not the topic).
- Each **page title** is a full sentence — the takeaway for that page.
- Each **section** within a page has a sub-header that tells you what to conclude before you read the detail.
- **Charts and tables** always have a "so what" sentence above or below them.

**Bad title:** "Q1 Client Health Overview"
**Good title:** "Client health improved in Q1, but 12 at-risk accounts need immediate intervention"

**Bad section header:** "Engagement Metrics"
**Good section header:** "Engagement calls dropped 18% in February — three CSMs fell below the 40-day SLA"

---

### 2. MECE Thinking

MECE (Mutually Exclusive, Collectively Exhaustive) is the quality standard for how we organize information.

**Mutually Exclusive:** Each category or argument covers a distinct area. No overlaps. If two sections say similar things, combine them.

**Collectively Exhaustive:** Together, all categories cover the full picture. No gaps. If the reader asks "but what about X?" and X is relevant, you missed it.

**Apply MECE to:**
- How you segment data (client tiers, churn reasons, process categories)
- How you structure arguments on a page
- How you break a report into sections

**Test:** After writing, ask: "Do any sections overlap? Is anything missing?" If yes, restructure until MECE is achieved.

---

### 3. Before You Write — The Mandatory Questions

No report should be created — by a person or by AI — without answering these five questions first. These are not optional. They are the foundation.

| # | Question | Why It Matters |
|---|----------|----------------|
| 1 | **What is the single most important message?** | If you can't say it in one sentence, you don't understand it yet. |
| 2 | **Who is the audience and what do they need to decide?** | A report for the CEO is different from one for a CSM. Shape the message for the reader. |
| 3 | **What are the 2-4 supporting arguments (MECE)?** | These become your page sections. If you have more than 4, consolidate. |
| 4 | **What data proves each argument?** | No argument without evidence. No evidence without an argument. |
| 5 | **What is the recommended next step?** | Every report must end with action. If there's nothing to do, the report shouldn't exist. |

**For CSMs:** This is not bureaucracy. This is clarity. If you cannot answer question #1 before a client call or report, you are not ready. The report structure forces you to think first, then communicate. The act of filling out these five questions IS the preparation.

---

### 4. Report Types and When to Use Them

| Type | Pages | When | Mandatory Sections |
|------|-------|------|-------------------|
| **Engagement Report** | 2-4 | Before every client engagement call | Situation, Key Metrics, Recommendation, Next Steps |
| **Fulfillment Report** | 1-2 | With every monthly delivery | What Was Delivered, Quality Summary, Action Items |
| **BuyBox Audit** | 2-3 | Quarterly | Current Performance, Market Analysis, Recommended Changes |
| **Health Alert** | 1 | When client enters at-risk status | What Happened, Root Cause, Recovery Plan |
| **Onboarding Summary** | 2-3 | At onboarding completion | Journey Summary, First Results, Ongoing Plan |

**Rule: No report exceeds 5 pages.** If it's longer, the thinking isn't sharp enough. Cut.

---

## Part II — Report Structure

---

### 5. Page Anatomy

Every page in a report follows this exact structure. No exceptions.

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  LOGO (top-left)                    Date (top-right)    │
│                                                         │
│  ─────────────────────────────────────────────────────  │
│                                                         │
│  ACTION TITLE                                           │
│  A full sentence that states the page's conclusion.     │
│  Georgia Bold, 1.25rem (20px), Navy.                    │
│  ──────────────────────────────── (2px navy rule below) │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  KPI CARD   │  │  KPI CARD   │  │  KPI CARD   │     │
│  │  Label      │  │  Label      │  │  Label      │     │
│  │  Value      │  │  Value      │  │  Value      │     │
│  │  vs. prior  │  │  vs. prior  │  │  vs. prior  │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                         │
│  SUPPORTING CONTENT                                     │
│  Tables, charts, bullet points, insight boxes.          │
│  Organized in 2-column or full-width layouts.           │
│                                                         │
│  ┌──INSIGHT BOX──────────────────────────────────────┐  │
│  │  The "so what" — what this data means and what    │  │
│  │  to do about it.                                  │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ─────────────────────────────────────────────────────  │
│  8020REI              Confidential              Page N  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Mandatory elements on every page:**
- Action title (full sentence, the takeaway)
- At least one data point or evidence
- Footer with company name, confidentiality, page number

**Mandatory elements on the first page:**
- Logo (top-left)
- Report title (the overall conclusion)
- Date and author
- "Confidential" label

**Mandatory element on the last page:**
- Recommended next steps with owners and dates

---

### 6. Page Types

**Cover Page:** Title, subtitle, author, date, logo. Nothing else. White space is the design.

**Data Page:** Action title → KPIs → Supporting content → Insight box → Footer. This is the workhorse.

**Recommendation Page:** Action title → The recommendation → Supporting rationale (MECE) → Next steps with owners/dates.

**Summary Page:** Action title → 3-4 key takeaways (numbered or in cards) → Single recommended action.

---

## Part III — Visual Design

---

### 7. Typography

Reports use the McKinsey-standard font pairing: **serif for authority, sans-serif for clarity.**

**Primary: Georgia** — Headlines, action titles, KPI values, page numbers.
**Secondary: Helvetica Neue / Arial** — Body text, tables, labels, captions, everything else.

| Element | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| **Report Title** (cover) | Georgia | 36-44px | Bold | `#1a1a1a` |
| **Action Title** (page) | Georgia | 1.25rem (20px) | Bold | `#1a1a1a` |
| **Sub-header** | Georgia | 15-17px | Bold | `#1a1a1a` |
| **KPI Value** | Georgia | 28-36px | Bold | `#0B5394` (accent) |
| **Body Text** | Helvetica/Arial | 13-15px | Regular (400) | `#2d2d2d` |
| **Table Data** | Helvetica/Arial | 12-13px | Regular (400) | `#2d2d2d` |
| **Table Header** | Helvetica/Arial | 10-11px | Bold (700) | `#666666` |
| **Caption / Source** | Helvetica/Arial | 10-11px | Regular (400) | `#a3a3a3` |
| **Section Label** | Helvetica/Arial | 10px | Bold (700) | `#0B5394` |
| **Footer** | Helvetica/Arial | 10px | Regular (400) | `#a3a3a3` |

**Typography Rules:**
- Line height: 1.2 for headlines, 1.6 for body.
- Max body text width: 680px (~75 characters per line).
- Section labels: ALL-CAPS, letterspacing 0.15em. Only element allowed in all-caps.
- Numbers in tables: right-aligned, `font-variant-numeric: tabular-nums`.
- Never use more than 3 font sizes on a single page.

---

### 8. Color Palette

Minimal and purposeful. Color means something — never decorative.

**Core Palette:**

| Role | Hex | Usage |
|------|-----|-------|
| **Black** (text) | `#1a1a1a` | Headlines, primary text |
| **Dark Gray** (text) | `#2d2d2d` | Body text, table data |
| **Gray** (secondary) | `#6b6b6b` | Table headers, secondary labels |
| **Light Gray** (muted) | `#a3a3a3` | Captions, footers, disabled |
| **Line** (borders) | `#d4d4d4` | Table rules, dividers |
| **Background** | `#ffffff` | Page background |
| **Accent Blue** | `#0B5394` | Section labels, KPI values, key highlights |
| **Accent Light** | `#E8F0FE` | Insight box backgrounds, highlight rows |

**Status Colors (used only for semantic meaning):**

| Status | Hex | When |
|--------|-----|------|
| **Positive** | `#166534` | Metrics trending up, good health |
| **Positive BG** | `#DCFCE7` | Background for positive callouts |
| **Warning** | `#B45309` | Metrics at risk, needs attention |
| **Warning BG** | `#FEF3C7` | Background for warning callouts |
| **Negative** | `#991B1B` | Metrics trending down, critical |
| **Negative BG** | `#FEE2E2` | Background for negative callouts |

**Rules:**
- Never use color without semantic meaning. If it's blue, it means "key information." If it's red, it means "bad."
- Limit to 2 colors per page beyond black/gray/white.
- Charts use: `#1d4ed8`, `#0f766e`, `#a16207`, `#7e22ce`, `#c2410c`, `#64748b` (in order).
- Never use red and green as the only differentiator (accessibility). Always pair with text labels.

---

### 9. Layout & Spacing

**Page dimensions (for HTML → PDF):**
- Width: 210mm (A4) with 56px left/right padding.
- Min height: 297mm per page (A4) or auto (for print).
- The HTML must use `page-break-after: always` between pages so PDF output is clean.

**Spacing Scale:**

| Token | Value | Use |
|-------|-------|-----|
| `xs` | 4px | Inline gaps, icon spacing |
| `sm` | 8px | Between label and value |
| `md` | 16px | Between related elements, table padding |
| `lg` | 24px | Between sections on a page |
| `xl` | 32px | Major section breaks |
| `2xl` | 48px | Page margins (top, bottom, left, right) |

**White space rule:** At least 35-40% of each page should be empty. If a page feels crowded, remove content — don't shrink text.

**Grid:** 2-column (60/40 or 50/50) for analysis pages. Full-width for tables and charts. 3-4 column for KPI card rows.

**Borders & Lines:**
- Thick rule (2px, `#0B5394`): Below action titles. Thin rule (1px, `#d4d4d4`): Above footers.
- Thin rule (1px, `#d4d4d4`): Between table rows, between sections.
- Left border (3px, `#0B5394`): Insight/callout boxes.
- No rounded corners. No box shadows. No gradients. Sharp and clean.

---

### 10. Component Library

#### Action Title
```html
<div class="action-title">
  Client health improved in Q1, but 12 at-risk accounts need
  <span class="highlight">immediate intervention</span>
</div>
```
- Georgia Bold, 1.25rem (20px), `#1a1a1a`.
- 2px solid `#0B5394` border-bottom.
- The `.highlight` span uses accent blue (`#0B5394`) for one key phrase.
- Always a full sentence. Never a topic label.

#### KPI Card
```html
<div class="kpi-row">
  <div class="kpi-card">
    <div class="kpi-label">Active Clients</div>
    <div class="kpi-value">142</div>
    <div class="kpi-delta positive">+8 vs. last month</div>
  </div>
</div>
```
- Border: 1px solid `#d4d4d4`. No radius. No shadow.
- KPI value: Georgia Bold, 28-36px, accent blue.
- Label: Helvetica 10px, uppercase, letterspacing 1.5px, gray.
- Delta: 12px, colored by status (positive/warning/negative).

#### Insight Box
```html
<div class="insight-box">
  <p><strong>Engagement calls dropped 18% in February.</strong>
  Three CSMs fell below the 40-day SLA. Root cause: holiday
  backlog and two unfilled roles in the team.</p>
</div>
```
- Left border: 3px solid `#0B5394`.
- Background: `#E8F0FE`.
- Padding: 16px 20px.
- Text: 0.875rem Helvetica, line-height 1.55.
- Variants: `.insight-box.warn` (amber border + warm bg), `.insight-box.negative` (red border + red bg), `.insight-box.positive` (green border + green bg).

#### Data Table
```html
<table>
  <thead>
    <tr><th>Client</th><th>MRR</th><th>Health</th><th>Last Contact</th></tr>
  </thead>
  <tbody>
    <tr><td>Acme Corp</td><td class="num">$2,400</td><td>Green</td><td>Mar 2</td></tr>
  </tbody>
</table>
```
- Header: 10-11px bold uppercase gray, 2px bottom border.
- Rows: alternating white / `#F9FAFB`. 1px border-bottom `#d4d4d4`.
- Numbers: right-aligned, `tabular-nums`.
- No vertical borders. Ever.

#### Phase Block
```html
<div class="phase-block">
  <div class="phase-num">Phase 1</div>
  <div class="phase-title">Lead Generation to Sales Handoff</div>
  <div class="phase-text">Marketing generates leads through ads...</div>
</div>
```
- Left border: 3px solid accent.
- Background: `#E8F0FE`.
- Phase-num: 10px uppercase bold, accent color.
- Phase-title: Georgia Bold, 15-17px.
- Phase-text: 13px Helvetica, `#2d2d2d`.

#### Bullet List
```html
<ul class="bullet-list">
  <li><strong>Fast data collection</strong> — reduces time to first value</li>
  <li><strong>Same-day fulfillment</strong> — builds immediate trust</li>
</ul>
```
- 5px solid accent-colored circle bullets.
- 13px Helvetica, `#2d2d2d`.
- Leading bold phrase for scanability.

#### Footer
```html
<div class="page-footer">
  <span><a href="https://booking.8020rei.com">8020rei.com</a></span>
  <span>Confidential</span>
  <span>Page 2</span>
</div>
```
- 1px top border `#d4d4d4`. 0.625rem Helvetica, `#999999`.
- Three items: company link, confidentiality, page number.
- Company name links to `booking.8020rei.com` but displays as `8020rei.com`.
- Link inherits footer color (`#999999`), no underline. Underline on hover.
- Positioned at bottom of page (`position: absolute; bottom: 36px; left: 56px; right: 56px`).

---

## Part IV — HTML & Print Standards

---

### 11. HTML Structure for Print-Ready Reports

Every report is a single HTML file. Each page is a `<section class="page">`. The CSS handles page breaks for PDF export.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>[Report Title] — 8020REI</title>
  <style>
    /* Paste the 8020REI report CSS here (see Section 12) */
  </style>
</head>
<body>

  <!-- Page 1: Cover -->
  <section class="page cover">
    <img src="logos/logo-full-light.png" class="logo" alt="8020REI">
    <div class="cover-content">
      <div class="cover-title">[Report Title — the conclusion]</div>
      <div class="cover-subtitle">[Context: date range, scope]</div>
      <div class="cover-meta">
        Prepared by [Name] · [Date] · Confidential
      </div>
    </div>
  </section>

  <!-- Page 2+: Data pages -->
  <section class="page">
    <div class="page-header">
      <img src="logos/logo-icon-light.png" class="page-logo" alt="">
      <span class="page-date">[Date]</span>
    </div>

    <div class="section-label">[SECTION NAME]</div>
    <div class="action-title">
      [Full sentence conclusion for this page]
    </div>

    <!-- Content: KPIs, tables, charts, insights -->

    <div class="page-footer">
      <span>8020REI</span>
      <span>Confidential</span>
      <span>Page N</span>
    </div>
  </section>

</body>
</html>
```

**Key HTML rules:**
- One `<section class="page">` per printed page.
- Every page has `page-header`, `action-title`, content, and `page-footer`.
- The footer uses `position: absolute; bottom: 36px` to stick to the bottom.
- No external dependencies. Fonts are system fonts (Georgia, Helvetica Neue/Arial).
- All images use relative paths to the `logos/` folder.

---

### 12. Base CSS Framework

This is the complete CSS that should be included in every report. Copy this verbatim.

```css
/* === 8020REI Report CSS === */

*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

html {
  font-size: 16px;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

body {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  color: #1a1a1a;
  background: #ffffff;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* --- Typography --- */
h1, h2, h3 {
  font-family: Georgia, 'Times New Roman', serif;
  font-weight: 700;
  color: #1a1a1a;
  line-height: 1.2;
}

h1 { font-size: 2.25rem; letter-spacing: -0.02em; }
h2 { font-size: 1.5rem; letter-spacing: -0.01em; }
h3 { font-size: 1.125rem; }

p, li, td, th {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 0.9375rem;
  color: #1a1a1a;
  line-height: 1.6;
}

.sub-header {
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 15px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 10px;
}

.sub-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #6b6b6b;
  margin-bottom: 4px;
}

.body-text {
  font-size: 14px;
  line-height: 1.65;
  color: #2d2d2d;
  max-width: 680px;
}

.body-sm {
  font-size: 12px;
  line-height: 1.6;
  color: #6b6b6b;
}

/* --- Page structure --- */
.page {
  width: 210mm;
  min-height: 297mm;
  margin: 0 auto;
  padding: 48px 56px;
  page-break-after: always;
  position: relative;
  background: #ffffff;
}

.page:last-child {
  page-break-after: auto;
}

@media screen {
  .page {
    border: 1px solid #d4d4d4;
    margin-bottom: 24px;
  }
}

/* --- Page header (non-cover pages) --- */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-logo { height: 22px; }
.page-date { font-size: 10px; color: #a3a3a3; }

/* --- Section label --- */
.section-label {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: #0B5394;
  margin-bottom: 8px;
  display: block;
}

/* --- Action title --- */
.action-title {
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: #1a1a1a;
  line-height: 1.35;
  margin-bottom: 28px;
  border-bottom: 2px solid #0B5394;
  padding-bottom: 12px;
}

.action-title .highlight { color: #0B5394; }

/* --- Cover --- */
.cover {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-top: 0;
}

.cover-logo { margin-bottom: 64px; }
.cover-logo img { height: 56px; display: block; }

.cover-title {
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a1a1a;
  line-height: 1.15;
  margin-bottom: 16px;
  letter-spacing: -0.02em;
}

.cover-subtitle {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 1.0625rem;
  color: #666666;
  margin-bottom: 48px;
  line-height: 1.5;
}

.cover-confidential {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: #999999;
  border-top: 1px solid #d4d4d4;
  padding-top: 16px;
  display: inline-block;
}

.cover-divider {
  width: 64px;
  height: 3px;
  background: #0B5394;
  margin-bottom: 32px;
}

/* --- Sub-section header --- */
.sub-section-header {
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 1rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-top: 8px;
  margin-bottom: 14px;
  padding-bottom: 8px;
  border-bottom: 1px solid #d4d4d4;
}

/* --- Layout --- */
.two-col {
  display: flex;
  gap: 32px;
  margin-bottom: 32px;
}

.two-col .col { flex: 1; }

.col h3 {
  font-size: 1rem;
  margin-bottom: 14px;
  padding-bottom: 8px;
  border-bottom: 1px solid #d4d4d4;
}

.row { display: flex; gap: 32px; }
.row > * { flex: 1; }

.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }
.grid-4 { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 18px; }

.divider { border-top: 1px solid #d4d4d4; margin: 20px 0; }

/* --- KPI cards --- */
.kpi-row {
  display: flex;
  gap: 0;
  margin-bottom: 32px;
}

.kpi-card {
  flex: 1;
  padding: 20px 24px;
  border: 1px solid #d4d4d4;
  border-right: none;
  text-align: center;
}

.kpi-card:last-child {
  border-right: 1px solid #d4d4d4;
}

.kpi-label {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #666666;
  margin-bottom: 6px;
}

.kpi-value {
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 2rem;
  font-weight: 700;
  color: #0B5394;
  line-height: 1.1;
}

.kpi-context {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 0.75rem;
  color: #666666;
  margin-top: 4px;
}

.kpi-delta { font-size: 12px; font-weight: 600; margin-top: 6px; }
.kpi-delta.positive { color: #166534; }
.kpi-delta.warning { color: #B45309; }
.kpi-delta.negative { color: #991B1B; }

/* --- Insight box --- */
.insight-box {
  background: #E8F0FE;
  border-left: 3px solid #0B5394;
  padding: 16px 20px;
  margin-bottom: 28px;
}

.insight-box p {
  font-size: 0.875rem;
  line-height: 1.55;
}

.insight-box strong { font-weight: 700; }
.insight-box.warn { border-left-color: #B45309; background: #FEF3C7; }
.insight-box.negative { border-left-color: #991B1B; background: #FEE2E2; }
.insight-box.positive { border-left-color: #166534; background: #DCFCE7; }

/* --- Phase block --- */
.phase-block {
  padding: 18px 22px;
  border-left: 3px solid #0B5394;
  background: #E8F0FE;
  margin-bottom: 14px;
}

.phase-num {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #0B5394;
  margin-bottom: 4px;
}

.phase-title {
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 15px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 6px;
}

.phase-text {
  font-size: 13px;
  line-height: 1.6;
  color: #2d2d2d;
}

/* --- Tables --- */
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 16px;
}

table th {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #666666;
  text-align: left;
  padding: 8px 8px 8px 0;
  border-bottom: 2px solid #1a1a1a;
}

table td {
  font-size: 0.875rem;
  padding: 8px 8px 8px 0;
  border-bottom: 1px solid #ebebeb;
  color: #2d2d2d;
  vertical-align: top;
}

table tr:last-child td { border-bottom: none; }
table tr:nth-child(even) td { background: #F9FAFB; }
table .num { text-align: right; font-variant-numeric: tabular-nums; }

/* --- Bullet list --- */
ul.bullet-list {
  list-style: none;
  padding: 0;
  margin-bottom: 16px;
}

ul.bullet-list li {
  font-size: 0.9375rem;
  line-height: 1.5;
  color: #2d2d2d;
  padding-left: 16px;
  position: relative;
  margin-bottom: 8px;
}

ul.bullet-list li::before {
  content: '';
  position: absolute;
  left: 0; top: 9px;
  width: 5px; height: 5px;
  background: #0B5394;
  border-radius: 50%;
}

ul.bullet-list li strong { color: #1a1a1a; }

/* --- Step list --- */
ol.step-list {
  list-style: none;
  counter-reset: step;
  padding: 0;
  margin-bottom: 16px;
}

ol.step-list li {
  counter-increment: step;
  display: flex;
  gap: 12px;
  align-items: flex-start;
  margin-bottom: 12px;
  font-size: 0.9375rem;
  color: #2d2d2d;
  line-height: 1.55;
}

ol.step-list li::before {
  content: counter(step);
  font-family: Georgia, 'Times New Roman', serif;
  min-width: 22px; height: 22px;
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 700;
  color: #0B5394;
  border: 1.5px solid #0B5394;
  border-radius: 50%;
  flex-shrink: 0;
}

/* --- Status colors --- */
.status-green { color: #166534; }
.status-yellow { color: #B45309; }
.status-red { color: #991B1B; }
.bg-green { background: #DCFCE7; }
.bg-yellow { background: #FEF3C7; }
.bg-red { background: #FEE2E2; }

/* --- Page footer --- */
.page-footer {
  position: absolute;
  bottom: 36px;
  left: 56px;
  right: 56px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 0.625rem;
  color: #999999;
  letter-spacing: 0.05em;
  border-top: 1px solid #d4d4d4;
  padding-top: 10px;
}

.page-footer span { font-size: 0.625rem; color: #999999; }
.page-footer a { color: #999999; text-decoration: none; }
.page-footer a:hover { text-decoration: underline; }

/* --- Placeholder styling --- */
.placeholder {
  color: #0B5394;
  background: #E8F0FE;
  padding: 1px 4px;
  font-weight: 600;
}

/* --- Utilities --- */
.mt-8 { margin-top: 8px; }
.mt-12 { margin-top: 12px; }
.mt-16 { margin-top: 16px; }
.mt-24 { margin-top: 24px; }
.mb-8 { margin-bottom: 8px; }
.mb-12 { margin-bottom: 12px; }
.mb-16 { margin-bottom: 16px; }
.mb-24 { margin-bottom: 24px; }

/* --- Print --- */
@media print {
  body { background: none; }

  .page {
    width: auto;
    min-height: auto;
    margin: 0;
    padding: 48px 56px;
    border: none;
  }

  .page-footer {
    position: fixed;
    bottom: 24px;
  }
}
```

---

## Part V — Brand Assets

---

### 13. Logo

All logos are in the `logos/` folder.

| File | Background | Use |
|------|-----------|-----|
| `logo-full-light.png` | White/light | Cover pages, headers on white |
| `logo-full-dark.png` | Dark/navy | Dark slide decks |
| `logo-icon-light.png` | White/light | Page headers (small, 22px) |
| `logo-icon-dark.png` | Dark | Dark backgrounds |

**Logo description:** Donut chart icon (~75/25 split) + "8020REI" wordmark. Light version: navy donut + sky blue highlight. Dark version: blue donut + teal highlight.

**Placement:** Cover page top-left (56px height). Subsequent pages top-left (22px height). Never stretch, rotate, or recolor.

---

## Part VI — Quality Gate

---

### 15. Pre-Send Checklist

Before any report is sent to a client or presented internally, it must pass every item below. This is non-negotiable.

**Thinking Quality:**
- [ ] The report title states a conclusion, not a topic
- [ ] Every page has an action title that is a full sentence
- [ ] Arguments are MECE — no overlaps, no gaps
- [ ] Every data point has a "so what" interpretation
- [ ] The report ends with a clear next step, owner, and date

**Content Quality:**
- [ ] All numbers are formatted (commas, $, %, K/M)
- [ ] All numbers show a comparison (vs. prior period or target)
- [ ] No page has more than one main idea
- [ ] Total pages ≤ 5
- [ ] No orphan data — every chart/table has context

**Design Quality:**
- [ ] Georgia for headlines, Helvetica/Arial for body
- [ ] Max 3 font sizes per page
- [ ] 35%+ white space per page
- [ ] No decorative color — all color has semantic meaning
- [ ] Footer on every page (company, confidential, page #)
- [ ] Logo on cover and page headers

**Print Quality:**
- [ ] Each `<section class="page">` has `page-break-after: always`
- [ ] PDF output has clean page breaks — no content cut mid-sentence
- [ ] Tested: File → Print → Save as PDF produces correct output

---

## Quick Reference

| Property | Value |
|----------|-------|
| **Headline Font** | Georgia (serif) |
| **Body Font** | Helvetica Neue / Arial |
| **Text Color** | `#1a1a1a` |
| **Body Text** | `#2d2d2d` |
| **Muted** | `#6b6b6b` |
| **Light** | `#a3a3a3` |
| **Lines** | `#d4d4d4` |
| **Accent** | `#0B5394` |
| **Accent BG** | `#E8F0FE` |
| **Positive** | `#166534` on `#DCFCE7` |
| **Warning** | `#B45309` on `#FEF3C7` |
| **Negative** | `#991B1B` on `#FEE2E2` |
| **Page Margin** | 48px top/bottom, 56px left/right |
| **Section Gap** | 24px |
| **Border Radius** | 0 (none) |
| **Max Report Pages** | 5 |
| **Chart Palette** | `#1d4ed8`, `#0f766e`, `#a16207`, `#7e22ce`, `#c2410c`, `#64748b` |
