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

```bash
python main.py "Client Name"
```

This runs all three steps automatically:
1. Merge all monthly fulfillment xlsx files from `01_fulfillment_merger/input/`
2. Pass merged data in-memory to join with the COO file in `02_data_preparation/input/`; output `Data ready for analysis.xlsx` in `02_data_preparation/output/`
3. Read the full COO-format file from `03_distress_overview/input/` and compute the distress signal universe counts by county; output `Distress Overview.xlsx` in `03_distress_overview/output/`

`Data ready for analysis.xlsx` contains one sheet:
- `Sold properties on fulfillment` — only rows that matched a COO record AND have a LAST SALE DATE

The total fulfillment row count is stored separately in `02_data_preparation/output/fulfillment_row_count.txt`.

### Step 4 — Generate the report (Claude task)

Once `Data ready for analysis.xlsx` and `Distress Overview.xlsx` both exist, run:

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

**Report structure (4 pages + signal breakdown section + annex):**
- Page 1: Cover — Atlas-style title (see `analysis_notes.md` Section 9)
- Page 2: Situation & Key Finding — KPI cards, bar chart of active signals, signal stack distribution
- Page 3: Supporting Evidence — county breakdown (left col), buyer type + monthly sale volume (right col)
- Page 4: Recommendations — signal-stack tiers, Rapid Response, Niche Lists, Distress Universe table, Next Steps
- Signal breakdown section: full signal × county table (flows across pages as needed)
- Annex: All matched properties sorted by county, with active signals at delivery

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

## Reference: FreedomREI (March 2026)

The first report produced with this pipeline. Use as a structural and analytical reference.
- Report: `../8020REI-skills-main/8020REI-skills-main/customer_success/clients/freedomrei/2026-03-distress-analysis.html`
- Context: `../8020REI-skills-main/8020REI-skills-main/customer_success/clients/freedomrei/context.md`
- Analysis window: July–December 2025 | 181 sold properties | 3 counties (Duval, Clay, Nassau)
