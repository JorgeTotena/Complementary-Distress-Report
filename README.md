# Fulfillment Distress Analysis — Pipeline Guide

A step-by-step guide for producing the **Fulfillment Distress Analysis** report for any 8020REI client. The pipeline answers one question: *Of the properties we delivered to this client that were subsequently sold to another buyer, what distress signals were active at the moment we first shared them?*

---

## Prerequisites (First-Time Setup)

```bash
# Python 3.9+ required
pip install -r requirements.txt

# For PDF export (Playwright / headless Chromium)
pip install playwright
python -m playwright install chromium
```

Run both blocks once. After that, the pipeline runs entirely from the command line.

---

## Folder Structure

```
historical_distress_report/
  main.py                        ← run this to execute Steps 1 and 2
  requirements.txt
  CLAUDE.md
  analysis_notes.md
  fulfillment_distress_protocol (4).txt
  01_fulfillment_merger/
    input/                       ← place monthly fulfillment XLSX files here
    output/                      ← {client}_Merged_Fulfillments.parquet (auto-generated)
    merge.py
  02_data_processing/
    input/                       ← place the full domain COO XLSX file(s) here
    output/                      ← Distress Overview.xlsx (auto-generated)
    analyze.py
  03_generate_report/
    generate.py                  ← run this separately after main.py completes
```

---

## What Files You Need

### 1. Monthly Fulfillment Files → `01_fulfillment_merger/input/`

One XLSX file per month of the fulfillment period. **Each filename must start with a date in `YYYY-MM-DD` format** — the pipeline extracts `YYYY-MM` from the filename as the `PERIOD` column for every row in that file.

**Required naming format:**
```
YYYY-MM-DD ClientName <anything>.xlsx
```

**Example — 6-month window, August 2025 through January 2026:**
```
2025-08-08 SBDHOUSING 75K Direct Mail.xlsx
2025-09-08 SBDHOUSING 116K Direct Mail.xlsx
2025-10-08 SBDHOUSING 116K Direct Mail.xlsx
2025-11-08 SBDHOUSING 116K Direct Mail.xlsx
2025-12-07 SBDHOUSING 116K Direct Mail.xlsx
2026-01-07 SBDHOUSING 129K Direct Mail.xlsx
```

The script merges all XLSX files found in this folder. The count of files and their date range directly determine the analysis window you will pass to the report generator.

> If a filename does not start with `YYYY-MM-DD`, the pipeline assigns `PERIOD = UNKNOWN` for those rows, which will break the signal reading logic. Always verify filename format before running.

### 2. Domain COO File → `02_data_processing/input/`

The full domain COO (Change of Ownership) XLSX export for the client. This single folder serves **two purposes**:

| Purpose | How it is used |
|---------|---------------|
| Signal universe counts | `analyze.py` reads all properties and aggregates active signal counts by county → `Distress Overview.xlsx` (used on Page 4 of the report) |
| Sales index | `generate.py` extracts `LAST SALE DATE` and `MARKETING FIRST RECOMMENDATION` per FOLIO → identifies which fulfilled properties were sold and when |

You can place one or multiple XLSX files — they are merged automatically. File names have no special naming requirement.

> **Performance note:** The first run parses the raw XLSX, which can be slow for large files (90K+ rows). On subsequent runs, `generate.py` and `analyze.py` each write a `.parquet` cache file to this folder and load from it automatically, skipping the slow Excel parse.

---

## Step-by-Step Workflow

### Steps 1 & 2 — Run the Pipeline

From the project root, run:

```bash
python main.py "Client Name"
```

Replace `"Client Name"` with the actual client name exactly as you want it to appear in the report (e.g., `"SBD Housing"`, `"FreedomREI"`, `"SOS Home Offers"`).

This runs two steps automatically:

| Step | What it does | Output |
|------|-------------|--------|
| **Step 1 — Fulfillment Merge** | Reads all XLSX files from `01_fulfillment_merger/input/`, adds a `PERIOD` column (e.g., `2025-08`) derived from each filename, and merges all rows into a single file | `01_fulfillment_merger/output/{client}_Merged_Fulfillments.parquet` |
| **Step 2 — Distress Overview** | Reads the COO XLSX file(s) from `02_data_processing/input/` and counts active distress signals per county across all recommended properties | `02_data_processing/output/Distress Overview.xlsx` |

When both steps complete successfully, confirm that both output files exist before proceeding to Step 3.

---

### Step 3 — Generate the Report

Once both output files exist, run the report generator from the project root:

```bash
python 03_generate_report/generate.py "Client Name" clientslug --window YYYY-MM YYYY-MM
```

#### Arguments

| Argument | What it is | Example |
|----------|-----------|---------|
| `"Client Name"` | Full client name in quotes (matches what you passed to `main.py`) | `"SBD Housing"` |
| `clientslug` | Lowercase, no-spaces version of the name — used in the output filename | `sbdhousing` |
| `--window YYYY-MM YYYY-MM` | Start month and end month of the analysis window | `--window 2025-08 2026-01` |

#### How to determine the analysis window

The window must match the date range of the fulfillment files you placed in `01_fulfillment_merger/input/`. Read the dates from the filenames:

- Earliest file: `2025-08-08 ...` → window starts `2025-08`
- Latest file: `2026-01-07 ...` → window ends `2026-01`
- Result: `--window 2025-08 2026-01`

**Standard cadence:** 6 months ending 3 months before the report date.

| Report month | Analysis window |
|-------------|----------------|
| March 2026 | `--window 2025-07 2025-12` |
| April 2026 | `--window 2025-08 2026-01` |
| June 2026 | `--window 2025-10 2026-03` |

#### Full examples

```bash
# SBD Housing — 6-month window Aug 2025–Jan 2026
python 03_generate_report/generate.py "SBD Housing" sbdhousing --window 2025-08 2026-01

# FreedomREI — 6-month window Jul–Dec 2025
python 03_generate_report/generate.py "FreedomREI" freedomrei --window 2025-07 2025-12

# SOS Home Offers — 3-month pilot Oct–Dec 2025
python 03_generate_report/generate.py "SOS Home Offers" soshomeoffers --window 2025-10 2025-12
```

---

## Outputs

Both files are saved to the project root (`historical_distress_report/`):

| File | Description |
|------|-------------|
| `YYYY-MM-distress-analysis-{slug}.html` | Self-contained HTML report (logos and CSS embedded inline) |
| `YYYY-MM-distress-analysis-{slug}.pdf` | **This is the file sent to the client** |

The `YYYY-MM` prefix in the filename matches the **end month** of the analysis window (e.g., `--window 2025-08 2026-01` → prefix `2026-01`).

---

## What `generate.py` Does Automatically

You do not need to do any analysis manually. The script handles everything:

1. Loads the merged fulfillment parquet from `01_fulfillment_merger/output/`
2. Loads the domain COO file(s) from `02_data_processing/input/` (uses cache on repeat runs)
3. Joins fulfillment × domain on `FOLIO` to find matched properties
4. Applies the **inclusion criterion**: a property is included if its `LAST SALE DATE` falls on or after the window start date (no upper bound)
5. For each included property, reads distress signals from the row where `PERIOD == Marketing First Recommendation month`; uses the closest available period as a fallback if MFR falls outside the data window
6. Applies signal encoding rules: `ABSENTEE` is active when value = `1` (in-state) or `2` (out-of-state); all other signals are active when value = `1`
7. Counts active signals per property; computes percentages, stacking distribution, county breakdown, buyer type split, and monthly sale volume
8. Reads `02_data_processing/output/Distress Overview.xlsx` to build the Distress Universe table on Page 4
9. Builds the complete multi-page HTML report with all CSS and logos embedded inline
10. Exports the PDF via Playwright / headless Chromium

---

## Report Structure

| Section | Content |
|---------|---------|
| **Page 1 — Cover** | Atlas-style title, client name, analysis window |
| **Page 2 — Situation & Key Finding** | KPI cards, active signal bar chart, signal stack distribution |
| **Page 3 — Supporting Evidence** | County breakdown table (left column), Buyer Type + Monthly Sale Volume (right column) |
| **Page 4 — Recommendations** | Signal-stack tiers, Rapid Response, Niche Lists, Distress Universe table, Next Steps |
| **Signal Breakdown section** | Full signal × county table (flows across pages as needed) |
| **Annex** | All matched properties with their active signals at delivery, grouped by county |

---

## Troubleshooting

### PDF is not generated — "Playwright not installed"

```bash
pip install playwright
python -m playwright install chromium
```

The HTML report is still generated even if Playwright is missing. You can open the HTML in a browser and print to PDF as a workaround.

### PDF export is filling up disk space on C:

Playwright creates temporary Chromium user-data directories in `C:\Temp` on each run. These accumulate if the script is interrupted before cleanup.

**Already fixed:** `generate.py` wraps the browser session in `tempfile.TemporaryDirectory()`, which is deleted automatically when the browser closes — even on error.

**One-time cleanup** if disk was already consumed before the fix:
```bash
del /S /Q "%LOCALAPPDATA%\Temp\playwright*"
del /S /Q "%TEMP%\playwright*"
```

Note: The Playwright/Chromium install at `%LOCALAPPDATA%\ms-playwright\` (~300–600 MB) is a fixed one-time cost and does not grow with use.

### Fulfillment rows show `PERIOD = UNKNOWN`

The filename of one or more fulfillment XLSX files does not start with `YYYY-MM-DD`. Rename the files to match the required format and re-run `main.py`.

### Very slow first run on Step 2 or Step 3

Normal behavior when parsing a large COO XLSX file for the first time. The script saves a `.parquet` cache after the first parse. Subsequent runs load from cache and are significantly faster.

---

## Reference: Previous Reports

| Client | Window | Sold properties | Counties |
|--------|--------|----------------|---------|
| SBD Housing (Apr 2026) | Aug 2025–Jan 2026 | 4,886 | Clay, Jackson, Johnson, Wyandotte |
| FreedomREI (Mar 2026) | Jul–Dec 2025 | 181 | Duval, Clay, Nassau |
| SOS Home Offers (Mar 2026) | Oct–Dec 2025 | 104 | Columbia, Richmond, Aiken (Edgefield: 0 matched) |
