# Analysis Notes — Data Methodology Decisions

This file documents every non-obvious data decision made during the FreedomREI analysis (March 2026). Apply these rules to all future reports unless the protocol is updated.

---

## 1. Inclusion Criterion

A property is included in the analysis if its **LAST SALE DATE** falls within the analysis window.

- The timing of `MARKETING FIRST RECOMMENDATION` (MFR) does **not** affect inclusion.
- A property recommended before or after the window is still included as long as it sold within the window.

---

## 2. Signal Reading Rule (Period Filter)

Distress signals must be read from the row where `PERIOD` matches the `MARKETING FIRST RECOMMENDATION` month — not the sale date month.

**Why:** We want to know what signals were active *at the moment we first shared the property*, not at the time of sale.

### When MFR falls within the data window
Use the row where `PERIOD == MFR month` exactly.

### When MFR falls outside the data window (fallback rule)
Some properties were recommended before the data window begins or after it ends. In those cases:
- Use the **closest available PERIOD** in the data for that property.
- If the MFR is before the window, use the earliest available period for that FOLIO.
- If the MFR is after the window, use the latest available period for that FOLIO.

In the FreedomREI analysis, 10 properties had MFR dates outside the Jul–Dec 2025 window. All 10 were retained using the closest available period.

---

## 3. Distress Signal Columns and Active Value Rules

The COO file contains a large number of distress signal columns. All are standard encoding (active when value == 1) except ABSENTEE (see below). The `analyze.py` script processes all signals present in the file.

### Full COO signal column list (active when value == 1)

High-volume: HIGH EQUITY, DEFAULT RISK, DOWNSIZING, TAXES, VACANT, 55+, ESTATE
Mid-volume: PROBATE, LIENS CITY/COUNTY, DIVORCE, PRE-FORECLOSURE, INTER FAMILY TRANSFER, POOR CONDITION, CODE VIOLATIONS, JUDGEMENT, LIENS HOA, LOW CREDIT
Lower-volume: BANKRUPTCY, DEBT COLLECTION, EVICTION, WATER SHUT OFF, FIRE DAMAGE, AFFIDAVIT, INCARCERATED, DRIVING FOR DOLLARS, FAILED LISTING, FLOOD ZONE, LIENS MECHANIC, LIENS UTILITY, LIENS OTHER, 30-60 DAYS

Note: TIRED LANDLORD and generic LIENS are not present in the COO file used for FreedomREI (March 2026). The protocol document references them but they may not be active in all client configurations.

Encoding: `1` = active now, `0` = was active (no longer), blank = never active. Only `1` counts as active for signal analysis.

### ABSENTEE — special encoding

| Value | Meaning | Active? |
|-------|---------|---------|
| 1 | In-state absentee owner | Yes |
| 2 | Out-of-state absentee owner | Yes |
| 0 | Was absentee, no longer | No |
| blank | Never absentee | No |

Both `1` and `2` are treated as active for all counts, percentages, and signal stacking. This was confirmed by the client team — the protocol text only mentions value=1 but the platform uses value=2 for out-of-state.

---

## 4. Signal Count Per Property

For each property (using signals from the MFR period row):
- Count the number of active signals (applying the rules above).
- A property with 0 active signals is still included in the dataset; it just appears in the "0 signals" tier.
- Signal stack tiers used in recommendations: 3+ signals (high urgency), 2 signals (moderate), 1 signal (single), 0 signals (no distress at delivery).

---

## 5. Join Keys and Normalization

The fulfillment parquet and the domain COO files are joined on **FOLIO only**.

Normalization applied before joining:
- Convert to string
- Strip leading/trailing whitespace
- Convert to UPPERCASE

```python
ff["FOLIO"]     = ff["FOLIO"].astype(str).str.strip().str.upper()
domain["FOLIO"] = domain["FOLIO"].astype(str).str.strip().str.upper()
```

**Why FOLIO only (not FOLIO + ADDRESS + ZIP):** The three-key join used in earlier versions excluded valid matches where address formatting differed between the fulfillment export and the COO. FOLIO is the platform's canonical unique property identifier and is sufficient for a reliable join.

---

## 6. Data Sources per Field

The analysis uses two source files:

| Field | Source |
|---|---|
| All distress signal columns | Fulfillment (historical snapshot at recommendation time) |
| COUNTY, ADDRESS, CITY, OWNER TYPE, PERIOD | Fulfillment |
| LAST SALE DATE | Domain COO (`02_data_processing/input/`) |
| MARKETING FIRST RECOMMENDATION | Domain COO (`02_data_processing/input/`) |

Signal values come from the **fulfillment** because they represent the state of the property at the time it was recommended — not the current state. The domain COO is used only to retrieve `LAST SALE DATE` and `MARKETING FIRST RECOMMENDATION` (which are not present in the fulfillment export).

---

## 7. Pipeline Output Structure

| Step | Output |
|---|---|
| Step 1 — Fulfillment Merger | `01_fulfillment_merger/output/{client}_Merged_Fulfillments.parquet` |
| Step 2 — Data Processing | `02_data_processing/output/Distress Overview.xlsx` |
| Step 3 — Generate Report | `{YYYY-MM}-distress-analysis-{slug}.html` + `.pdf` |

`generate.py` builds a lightweight `_sales_cache.parquet` in `02_data_processing/input/` after the first run. It stores only FOLIO + LAST SALE DATE + MARKETING FIRST RECOMMENDATION from the full domain COO, so subsequent runs skip the slow xlsx parse.

---

## 7b. Domain COO File — Dual Role

The full domain COO file placed in `02_data_processing/input/` serves two purposes:

1. **Signal universe counts** (`analyze.py`, Step 2): aggregated by county → `Distress Overview.xlsx`, used for the "Distress Universe" table on Page 4.
2. **Sales index** (`generate.py`, Step 3): FOLIO + LAST SALE DATE + MFR extracted and cached → used to identify which fulfillment properties sold and when.

**Inclusion criterion:** A property is included in the analysis if it appears in both the fulfillment AND the domain COO with `LAST SALE DATE >= window_start`. There is **no upper bound** on the sale date — this matches the Distress Report (Column D) methodology and avoids excluding properties that sold shortly after the window closed.

### Domain dedup rule (must match the other Distress Report)

The COO file carries ~167K duplicate FOLIO rows (multiple snapshots of the same property). Both `generate.py` (sales index) and `analyze.py` (universe counts) **must** dedup with:

```python
dom = (dom.sort_values("LAST SALE DATE", na_position="first")
          .drop_duplicates("FOLIO", keep="last")
          .reset_index(drop=True))
```

Sort by `LAST SALE DATE` first so NaT rows sit at the front; `keep="last"` then keeps the row with the most recent sale per FOLIO. A naive `keep="first"` (no sort) silently picks an older or NaT sale date and drops recently-sold properties from the analysis — for Rapid Fire HB (Nov 2025–Jan 2026 window) this caused 4,990 sold properties to be reported instead of the correct 5,147 (–157, ~3% under-count).

This matches `build_domain_report.py:388-392` in the other Distress Report folder, which is the canonical reference for the calculation.

### BuyBox filter for the Distress Universe (`analyze.py`)

`analyze.py` filters domain rows to `BUYBOX SCORE > 0` before counting signals. This restricts the "Distress Universe" totals (Page 4, "Platform Total" column) to the addressable buybox — the same scope the other Distress Report's Column B uses. Without the filter, totals include properties outside the client's buybox and inflate the universe by 2–3×.

---

## 8. Technical Notes

- **Intermediate format — parquet, not xlsx:** Steps 1 and 2 now write their output as `.parquet` (pyarrow) instead of `.xlsx`. Reason: openpyxl builds the entire workbook in RAM as Python objects before flushing — on 90K+ row files this reliably kills the terminal process. Parquet writes are binary/columnar and 5–10× faster with a fraction of the memory. The final `Distress Overview.xlsx` (Step 3 output, already aggregated to a handful of rows) remains xlsx since it's tiny and opened by the team in Excel.
- **Column filtering on large reads:** `analyze.py` and `prepare.py` both pass `usecols=lambda col: col.strip().upper() in NEEDED_COLS` when reading large COO xlsx files. This loads only the columns actually needed (COUNTY + signals, or the 9 COO join/metadata columns) rather than all 50–100 columns, cutting memory usage 70–80% on the first read.
- **Parquet cache in analyze.py:** After the first xlsx read, `analyze.py` writes a `_cache.parquet` to `02_data_processing/input/`. Subsequent runs load from cache and skip the Excel parse entirely. The cache is invalidated automatically when any source xlsx file is newer than the cache.
- **Sales index cache in generate.py:** On first run, `generate.py` extracts FOLIO + LAST SALE DATE + MFR from the domain COO and saves `_sales_cache.parquet` to `02_data_processing/input/`. Invalidated automatically when xlsx files change.
- **Excel engine:** Use `openpyxl` for any remaining write operations. `xlsxwriter` hits a 65,530-URL limit when the fulfillment file contains a `LINK PROPERTIES` column (common with large datasets). `openpyxl` has no such limit.
- **groupby period logic:** Do not use `groupby().apply()` with a function that returns a DataFrame row — it causes `AttributeError: 'Series' object has no attribute 'columns'` in pandas. Use an explicit `for folio, group in df.groupby('FOLIO')` loop instead.
- **PERIOD column format:** Must be `YYYY-MM` string (e.g., `2025-07`). The merger script extracts this from the filename. Verify this format is consistent before running the join.

---

## 9. Report Structure Rules (confirmed March 2026)

### County tiering — based on counties WITH active matched sales, not total BuyBox counties

The number of counties that drives report structure is the count of counties where at least one property sold during the analysis window — not the total number of counties in the client's BuyBox.

| Matched counties with sales | Report structure |
|---|---|
| 2–4 | Standard (4 pages + signal breakdown section + annex). Side-by-side county comparison on Page 3. |
| 5–6 | Adapted Page 3. Replace county comparison with ranked summary table (top 3 signals + count per county). Signal breakdown table unchanged. |
| 7+ | Portfolio report + one-page county brief per FIPS as numbered appendix sections. |

Counties in the BuyBox with **zero matched transactions** during the window:
- Still appear in the county breakdown table on Page 3 (showing "No matched transactions this period")
- Are **excluded** from signal breakdown table columns (adding empty columns adds noise, not information)
- Are **flagged** with an amber insight box on Page 3 noting the gap and recommending the follow-up analysis will clarify whether it's a quiet period or a structural market gap
- Are included in the KPI county count (reflects the actual BuyBox scope)

### Annex date format

Marketing First Recommendation shows **month + year only** (e.g., "Oct 2025"), not the exact day.

**Why:** County recording lag means properties close 1–30 days before the transaction appears in public records. Showing an exact day could make it look like the recommendation arrived late when the delay is structural, not a platform issue. Month + year gives enough precision for the client to compare to the sale date without creating a false impression of tardiness.

Format: `mfr.strftime("%b %Y")`

### Zero-signal properties

Do **not** mention the count or percentage of properties with zero active signals anywhere in the report narrative. Focus only on properties that carried signals. The signal stack distribution table may still show the 0-signal row as raw data, but it must never be called out in the text.

### Footer

Footer center label = client name (never "Confidential" or "Internal"). This is a client-facing report.

For flowing sections (signal breakdown, recommendations, annex): use `.flow-footer` class (static `<div>`) not `.page-footer` (which is `position: fixed` in print and repeats on every page).

### Writing style

Use the Atlas Residential report style for all headers. Do **not** use long Pyramid Principle conclusion sentences as titles.

- **Cover title:** "Of the [N] properties on [Client]'s fulfillment list that were sold during this period, these are the distress signals that were active at the time of delivery"
- **Page 2 — section label:** SITUATION & KEY FINDING
- **Page 2 title:** "At [Client]'s request, 8020REI reviewed [N] fulfillment properties confirmed sold between [Month Year] and [Month Year] — [Top1] and [Top2] were the most consistently active signals at the time of delivery"
- **Page 3 — section label:** SUPPORTING EVIDENCE
- **Page 3 title:** "[County A] and [County B] show the same signal pattern — [Top1] + [Top2] — confirming the finding holds across [Client]'s active markets"
- **Page 4 — section label:** RECOMMENDATIONS
- **Page 4 title:** "Acting on these findings now gives [Client] a direct path to more closed deals — prioritising the right signals, responding faster, and reaching motivated sellers before competing buyers engage."

Avoid: "When [Client] takes action... they can get more deals" — mixes singular company name with plural pronoun and sounds too casual.

### Page 3 layout

Page 3 uses a two-column layout:

- **Left column:** County Breakdown table (+ amber flag box if any BuyBox county had zero matched sales)
- **Right column:** Buyer Type table → investor entity note paragraph → Monthly Sale Volume table

Monthly Sale Volume must always go in the **right column**, below Buyer Type. Never place it below County Breakdown in the left column — the left column is already near capacity with the county table and any zero-county flag boxes. Stacking both tables in the left column causes the page to overflow.

---

## 10. SOS Home Offers Baseline Numbers (March 2026)

| Metric | Value |
|---|---|
| Total fulfillment rows | 93,053 |
| Sold properties in window | 104 |
| Analysis window | Oct–Dec 2025 (3-month pilot) |
| Properties with MFR fallback | 8 (MFR = Nov 2024, prior to window) |
| BuyBox counties | 4 (Columbia, Richmond, Aiken, Edgefield) |
| Matched counties (active sales) | 3 (Columbia 48, Richmond 46, Aiken 10) |
| Edgefield matched | 0 (flagged in report) |
| Top signal | High Equity (32.7%) |
| Second signal | 55+ (31.7%) |
| Third signal | Absentee (30.8%) |

---

## 11. SBD Housing Baseline Numbers (April 2026)

First report produced with the current pipeline (fulfillment × domain join on FOLIO, no step 2 COO join).

| Metric | Value |
|---|---|
| Total fulfillment rows | 668,000 |
| Unique fulfillment FOLIOs | 233,266 |
| Sold properties in window | 4,886 |
| Analysis window | Aug 2025–Jan 2026 (6-month) |
| Domain COO size | 716,089 rows / 709,930 unique FOLIOs |
| Counties | 4 (Clay, Jackson, Johnson, Wyandotte) |
| Jackson count | 1,933 (39.6%) |
| Johnson count | 1,497 (30.6%) |
| Wyandotte count | 839 (17.2%) |
| Clay count | 617 (12.6%) |
| Top signal | High Equity |
| Second signal | Default Risk |

---

## 12. FreedomREI Baseline Numbers (March 2026)

For reference when sanity-checking future runs:

| Metric | Value |
|---|---|
| Total fulfillment rows | 225,145 |
| Matched COO rows | 225,145 (all rows; COO join was left join) |
| Sold properties in window | 181 |
| Properties with MFR fallback | 10 |
| Counties | 3 (Duval, Clay, Nassau) |
| Duval count | 140 |
| Clay count | 31 |
| Nassau count | 10 |
| Top signal | High Equity (43.6%) |
| Second signal | Default Risk (28.2%) |
| Third signal | Absentee (27.6%) |
