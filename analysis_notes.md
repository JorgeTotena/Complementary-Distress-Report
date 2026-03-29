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

Fulfillment file and COO file are joined on three keys: **FOLIO + ADDRESS + ZIP**

Normalization applied to all three columns before joining:
- Convert to string
- Strip leading/trailing whitespace
- Convert to UPPERCASE

```python
JOIN_KEYS = ["FOLIO", "ADDRESS", "ZIP"]
for col in JOIN_KEYS:
    df[col] = df[col].astype(str).str.strip().str.upper()
```

---

## 6. COO Columns Appended to Fulfillment Data

The following columns are taken from the COO file and appended to matched rows:

| COO source column | Final column name |
|---|---|
| LAST SALE DATE | LAST SALE DATE |
| MARKETING FIRST RECOMMENDATION | MARKETING FIRST RECOMMENDATION |
| YEAR BUILT | YEAR BUILT |
| MARKETING DM COUNT | COO MARKETING DM COUNT |
| MARKETING CC COUNT | MARKETING CC COUNT |
| MARKETING SMS COUNT | MARKETING SMS COUNT |

Note: `MARKETING DM COUNT` is renamed to `COO MARKETING DM COUNT` to avoid collision with the same column that exists in the fulfillment file.

---

## 7. Output File Structure

`Data ready for analysis.xlsx` has two sheets:

| Sheet name | Contents |
|---|---|
| `Fulfillment properties` | All rows from the merged fulfillment file (225K+ rows for FreedomREI) |
| `Sold properties on fulfillment` | Only rows that matched a COO record AND have a LAST SALE DATE |

The analysis is performed exclusively on `Sold properties on fulfillment`.

---

## 7b. Distress Overview File — What It Is and What It Is NOT

The file placed in `03_distress_overview/input/` is a **separate, independent platform snapshot**. It is:

- A current-state picture of all properties ever recommended for the client, with their live distress flags
- Used **only** to populate the "Distress Universe — Platform Overview" table in Page 4 of the report
- **Not joined** with the fulfillment data
- **Not used** to determine which properties are included in the analysis
- **Not used** to read distress signals for the sold properties — those come exclusively from `Data ready for analysis.xlsx`

The entire sold properties analysis (signal counts, percentages, county breakdown, buyer type, annex) is driven solely by `02_data_preparation/output/Data ready for analysis.xlsx`. The distress overview file has zero impact on any analytical result.

---

## 8. Technical Notes

- **Excel engine:** Use `openpyxl` for all write operations. `xlsxwriter` hits a 65,530-URL limit when the fulfillment file contains a `LINK PROPERTIES` column (common with large datasets). `openpyxl` has no such limit.
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

Use the Atlas Residential report style for all headers:
- **Cover title:** "Of the [N] properties on [Client]'s fulfillment list that were sold during this period, these are the distress signals that were active at the time of delivery"
- **Page 2 (Situation & Key Finding):** "At [Client]'s request, 8020REI reviewed [N] fulfillment properties confirmed sold between [dates] — [Top1] and [Top2] were the most consistently active signals at the time of delivery"
- **Page 3 (Supporting Evidence):** "[County A] and [County B] show the same signal pattern — [Top1] + [Top2] — confirming the finding holds across [Client]'s active markets"
- **Page 4 (Recommendations):** "When [Client] takes action now to convert more properties from the fulfillment list into conversations, they can get more deals"

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

## 11. FreedomREI Baseline Numbers (March 2026)

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
