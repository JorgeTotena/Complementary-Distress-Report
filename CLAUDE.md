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
  main.py                          <- run this to execute steps 1, 2, and 3
  requirements.txt                 <- pip install -r requirements.txt before first run
  CLAUDE.md                        <- you are here
  analysis_notes.md                <- data methodology decisions (read before analysis)
  fulfillment_distress_protocol (4).txt  <- full protocol (mandatory reading)
  01_fulfillment_merger/
    input/                         <- place monthly fulfillment xlsx files here
    output/                        <- {client}_Merged_Fulfillments.xlsx (auto-generated)
    merge.py
  02_data_preparation/
    input/                         <- place COO xlsx here; merged file is auto-copied
    output/                        <- Data ready for analysis.xlsx (auto-generated)
    prepare.py
  03_distress_overview/
    input/                         <- place the full COO-format file (all recommended properties)
    output/                        <- Distress Overview.xlsx (auto-generated)
    analyze.py
```

The 8020REI skills package (design system, CSS, templates, brand assets) lives at:
`../8020REI-skills-main/8020REI-skills-main/customer_success/`

Previous client reports live at:
`../8020REI-skills-main/8020REI-skills-main/customer_success/clients/`

---

## Step-by-Step Workflow

### Steps 1, 2 & 3 — Run the pipeline (human task)

```
python main.py
```

The script will ask for the client name, then:
1. Merge all monthly fulfillment xlsx files from `01_fulfillment_merger/input/`
2. Auto-copy the merged file and join it with the COO file in `02_data_preparation/input/`; output `Data ready for analysis.xlsx` in `02_data_preparation/output/`
3. Read the full COO-format file from `03_distress_overview/input/` and compute the distress signal universe counts by county; output `Distress Overview.xlsx` in `03_distress_overview/output/`

The output file has two sheets:
- `Fulfillment properties` — all rows (225K+)
- `Sold properties on fulfillment` — only rows that matched a COO record

### Step 4 — Run the analysis and generate the report (Claude task)

Once `Data ready for analysis.xlsx` and `Distress Overview.xlsx` both exist, Claude performs the analysis and generates the report. **The PDF is the final deliverable.** The HTML is an intermediate artifact used only to produce the PDF — do not open it in a browser or attempt to debug its browser rendering. Follow this sequence:

#### 4a. Determine the analysis window
Per protocol Section 2.1: standard window = 6 months ending 3 months before the report date.
- Report in March 2026 → window = July–December 2025
- Document the agreed window before proceeding.

#### 4b. Load the data and apply filters
Read `02_data_preparation/output/Data ready for analysis.xlsx`, sheet `Sold properties on fulfillment`.

**Inclusion filter:** LAST SALE DATE must fall within the analysis window.

**Signal reading rule (critical):** Read distress signals from the row where PERIOD matches the MARKETING FIRST RECOMMENDATION month. If no exact match exists (MFR falls outside the data window), use the closest available period. See `analysis_notes.md` for full details.

#### 4c. Run the signal analysis
Count active signals per property. See `analysis_notes.md` for encoding rules and column list.

#### 4d. Load the Distress Overview breakdown
Read `03_distress_overview/output/Distress Overview.xlsx`. This file is a **current-state platform snapshot** — it is completely independent from the fulfillment analysis.

- Sheet `By County` — active signal counts per county (one row per county)
- Sheet `Total` — signal counts across all counties combined

**Important:** This file is used **only** to populate the Distress Universe table on Page 4. It does not affect which properties are included in the analysis, which signals are counted as active on sold properties, or any other analytical result. All analytical output comes from `02_data_preparation/output/Data ready for analysis.xlsx`.

#### 4e. Generate the HTML (intermediate artifact)
- Read the design system: `../8020REI-skills-main/8020REI-skills-main/customer_success/standards/DESIGN_SYSTEM.md`
- Read the CSS: `../8020REI-skills-main/8020REI-skills-main/customer_success/standards/report.css`
- Use the FreedomREI report as the structural reference: `../8020REI-skills-main/8020REI-skills-main/customer_success/clients/freedomrei/2026-03-distress-analysis.html`
- Read the client's `context.md` before generating (if it exists)
- Save the HTML to: `../8020REI-skills-main/8020REI-skills-main/customer_success/clients/<client-slug>/YYYY-MM-distress-analysis.html`
- Logo paths in the HTML must be `../../logos/logo-full-light.png` (cover) and `../../logos/logo-icon-light.png` (page headers) — relative to the client subfolder, two levels up to `customer_success/`
- **Do not open the HTML in a browser.** It is an intermediate artifact only.
- All pages must fit within `max-height: 11in` — author the content accordingly. Do not rely on browser preview to check fit.
- Cover footer and all page footers: use "FreedomREI" (or the client name) as the center label — not "Confidential" or "Internal". This is a client-facing report.

#### 4f. Export the PDF (final deliverable)
Start a local HTTP server rooted at `customer_success/` so logo relative paths resolve correctly, then use Playwright to export:

```bash
# From historical_distress_report/
cd ../8020REI-skills-main/8020REI-skills-main/customer_success
python -m http.server 8766 &
```

Then in Claude Code with Playwright MCP:
```js
async (page) => {
  await page.goto('http://localhost:8766/clients/<client-slug>/YYYY-MM-distress-analysis.html');
  await page.waitForLoadState('networkidle');
  await page.pdf({
    path: 'path/to/clients/<client-slug>/YYYY-MM-distress-analysis.pdf',
    format: 'Letter',
    printBackground: true,
    margin: { top: '0', right: '0', bottom: '0', left: '0' }
  });
}
```

Save the PDF in **two locations**:
1. Alongside the HTML in the client folder: `clients/<client-slug>/YYYY-MM-distress-analysis.pdf`
2. In the pipeline working directory: `historical_distress_report/YYYY-MM-<client-slug>-distress-analysis.pdf`

**The PDF is the file that gets sent to the client.**

**Report structure (4 pages + annex):**
- Page 1: Cover — Pyramid Principle title stating the conclusion
- Page 2: Signal Analysis — KPI cards, bar chart of active signals, signal stack distribution
- Page 3: Market Context — county breakdown by signal, buyer type split (Individual / Company / Trust), monthly sale volume
- Page 4: Recommendations — signal-stack tiers, Rapid Response, Niche Lists, Distress Overview universe table, Next Steps table
- Annex: All matched properties sorted by county, with active signals at delivery

The HTML is a single self-contained file (CSS inline, logos referenced by relative path). Use Python to build the annex table from the data and inject it into the HTML.

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

## Reference: FreedomREI (March 2026)

The first report produced with this pipeline. Use as a structural and analytical reference.
- Report: `../8020REI-skills-main/8020REI-skills-main/customer_success/clients/freedomrei/2026-03-distress-analysis.html`
- Context: `../8020REI-skills-main/8020REI-skills-main/customer_success/clients/freedomrei/context.md`
- Analysis window: July–December 2025 | 181 sold properties | 3 counties (Duval, Clay, Nassau)
