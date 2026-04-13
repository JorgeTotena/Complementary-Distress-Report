# Historical Distress Report — Claude Instructions

This folder contains the full pipeline to produce a **Fulfillment Distress Analysis** report for any 8020REI client. A team member drops the source files in, runs one script, and asks Claude to generate the HTML report.

## First-Time Setup

```
# Python 3.9+ required
pip install -r requirements.txt
```

---

## What This Report Is

A retrospective analysis that answers: *Of the properties we delivered to this client that were subsequently sold to another buyer, what distress signals were active on those properties at the moment we first shared them?*

Read the full protocol before doing anything:
- **Protocol:** `fulfillment_distress_protocol (4).txt` — defines the analysis window, data encoding rules, report structure, and standard recommendations. This is mandatory reading.

---

## Folder Structure

```
historical_distress_report/
  main.py                          <- run this to execute steps 1 and 2
  requirements.txt                 <- pip install -r requirements.txt before first run
  CLAUDE.md                        <- you are here
  analysis_notes.md                <- data methodology decisions (read before analysis)
  fulfillment_distress_protocol (4).txt  <- full protocol (mandatory reading)
  01_fulfillment_merger/
    input/                         <- place monthly fulfillment xlsx files here
    output/                        <- {client}_Merged_Fulfillments.parquet (auto-generated)
    merge.py
  03_distress_overview/
    input/                         <- place the full domain COO xlsx file(s) here
    output/                        <- Distress Overview.xlsx (auto-generated)
    analyze.py
```

> **Note:** Step 2 (data preparation / COO join) has been removed. Sold properties are now
> identified by joining the fulfillment directly against the full domain COO in `generate.py`.

The 8020REI skills package (design system, CSS, templates, brand assets) lives at:
`8020REI-skills-main/customer_success/`

Previous client reports live at:
`8020REI-skills-main/customer_success/clients/`

---

## Step-by-Step Workflow

### Steps 1 & 2 — Run the pipeline (human task)

```bash
python main.py "Client Name"
```

This runs both steps automatically:
1. Merge all monthly fulfillment xlsx files from `01_fulfillment_merger/input/` → `{client}_Merged_Fulfillments.parquet`
2. Read the full domain COO file(s) from `03_distress_overview/input/` and compute distress signal universe counts by county → `Distress Overview.xlsx`

**Analysis window rule:** The window always matches the fulfillment period — count the files in `01_fulfillment_merger/input/` and use their date range (e.g. 6 files Aug 2025–Jan 2026 → `--window 2025-08 2026-01`).

### Step 3 — Generate the report (Claude task)

Once `{client}_Merged_Fulfillments.parquet` and `Distress Overview.xlsx` both exist, run:

```bash
python 04_generate_report/generate.py "Client Name" clientslug --window YYYY-MM YYYY-MM
```

Example for FreedomREI (Jul–Dec 2025 window):
```bash
python 04_generate_report/generate.py "FreedomREI" freedomrei --window 2025-07 2025-12
```

**Output** — both files go to the pipeline root (`historical_distress_report/`):
- `YYYY-MM-distress-analysis-{slug}.html`
- `YYYY-MM-distress-analysis-{slug}.pdf` ← **this is the file sent to the client**

Logos are embedded as base64 — no HTTP server needed.

**Analysis window rule:** Standard = 6 months ending 3 months before the report date.
- Report in March 2026 → `--window 2025-07 2025-12`

All data methodology (signal reading rule, inclusion filter, encoding rules) is handled automatically by `generate.py`. See `analysis_notes.md` for the full methodology reference.

**Report structure (4 pages + signal breakdown section):**
- Page 1: Cover — Atlas-style title (see `analysis_notes.md` Section 9)
- Page 2: Situation & Key Finding — KPI cards, bar chart of active signals, signal stack distribution
- Page 3: Supporting Evidence — county breakdown (left col), buyer type + monthly sale volume (right col)
- Page 4: Recommendations — signal-stack tiers, Rapid Response, Niche Lists, Distress Universe table, Next Steps
- Signal breakdown section: full signal × county table (flows across pages as needed)

**Page 3 layout rule:** Monthly Sale Volume always goes in the **right column**, below the Buyer Type table and paragraph. Never stack it below County Breakdown in the left column — the left column is already near capacity with the county table.

**Overflow safeguard:** `.page { overflow: hidden; }` is set in the CSS. If content is too tall for a page it will be clipped visibly in the HTML, signalling that the layout needs adjustment. Fix the layout in `generate.py` — do not rely on clipping as a permanent solution.

---

## County Tiering (from protocol Section 2.4)

| Counties | Report structure |
|---|---|
| 2–3 | Standard 4-page + annex. Side-by-side county comparison on Page 3. |
| 4–6 | One report, adapted Page 3. Replace county bar chart with ranked summary table (top 3 signals + count per county). |
| 7+ | Portfolio report + one-page county brief per FIPS as numbered appendix sections. |

---

## Standard Recommendations (always include)

1. **Rapid Response** — parallel same-day outreach channel. Frame as the answer to speed-to-contact gap.
2. **Repeat analysis in 6 months** — one dataset is an observation, two is a pattern.
3. **Niche Lists (conditional on VA capacity):**
   - Track A: High Equity + Absentee — large pool, validated signal
   - Track B: Divorce + Pre-Foreclosure — small universe, high urgency, low competition

---

## Known Issues & Fixes

### PDF export drains disk space on C:
**Cause:** Playwright (used for PDF export) launches a headless Chromium browser that creates temporary user-data directories in `C:\Temp` on every run. These are not cleaned up automatically, especially if the script is interrupted, and accumulate over time.

**Fix (already applied):** `generate.py` now wraps the browser session in a `tempfile.TemporaryDirectory()`, which is deleted automatically when the browser closes — even on error.

**If disk space was already consumed** (one-time cleanup):
```bash
del /S /Q "%LOCALAPPDATA%\Temp\playwright*"
del /S /Q "%TEMP%\playwright*"
```

Note: The Playwright/Chromium install at `%LOCALAPPDATA%\ms-playwright\` (~300–600 MB) is a fixed one-time cost and does not grow with use.

---

## Reference: SBD Housing (April 2026)

The first report produced with the current pipeline (fulfillment + domain, no step 2 COO join).
- Report: `2026-01-distress-analysis-sbdhousing.html`
- Analysis window: August 2025–January 2026 | 4,886 sold properties | 4 counties (Clay, Jackson, Johnson, Wyandotte)
