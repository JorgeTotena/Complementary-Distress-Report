"""
04_generate_report/generate.py
-------------------------------
Step 4: Analyse the data and produce the HTML report + PDF for any client.

Protocol reference: fulfillment_distress_protocol (4).txt
  - Signals read at Marketing First Recommendation period (value=1 only; ABSENTEE: 1 or 2)
  - Inclusion criterion: LAST SALE DATE within analysis window
  - Fallback rule: if MFR outside data window, use closest available period
  - Standard recommendations: signal-stack prioritisation, Rapid Response, repeat in 6 months,
    Niche Lists (conditional on VA capacity)
  - Report structure: 4 pages + annex (2-3 counties = standard layout)

Usage:
    python generate.py "SOS Home Offers" soshomeoffers --window 2025-10 2025-12
    python generate.py "FreedomREI" freedomrei --window 2025-07 2025-12

Output:
    PIPELINE_ROOT/YYYY-MM-distress-analysis-{slug}.html
    PIPELINE_ROOT/YYYY-MM-distress-analysis-{slug}.pdf

All paths resolved from __file__. Logos embedded as base64 — no HTTP server required.
"""

from __future__ import annotations

import argparse
import base64
import datetime
import socket
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Paths — all derived from __file__, never from cwd
# ---------------------------------------------------------------------------
SCRIPT_DIR       = Path(__file__).resolve().parent
PIPELINE_ROOT    = SCRIPT_DIR.parent
CUSTOMER_SUCCESS = PIPELINE_ROOT / "8020REI-skills-main" / "8020REI-skills-main" / "customer_success"
DATA_FILE        = PIPELINE_ROOT / "02_data_preparation" / "output" / "Data ready for analysis.xlsx"
OVERVIEW_FILE    = PIPELINE_ROOT / "03_distress_overview" / "output" / "Distress Overview.xlsx"
ROW_COUNT_FILE   = PIPELINE_ROOT / "02_data_preparation" / "output" / "fulfillment_row_count.txt"
REPORT_CSS_FILE  = CUSTOMER_SUCCESS / "standards" / "report.css"
LOGO_FULL        = CUSTOMER_SUCCESS / "logos" / "logo-full-light.png"
LOGO_ICON        = CUSTOMER_SUCCESS / "logos" / "logo-icon-light.png"

# ---------------------------------------------------------------------------
# Signal definitions — per protocol Section 2.3 and analysis_notes.md
# ---------------------------------------------------------------------------
SIGNAL_COLS = [
    "HIGH EQUITY", "DEFAULT RISK", "55+", "ABSENTEE", "DOWNSIZING",
    "VACANT", "PRE-FORECLOSURE", "ESTATE", "TAXES", "POOR CONDITION",
    "INTER FAMILY TRANSFER", "DIVORCE", "PROBATE", "LOW CREDIT",
    "CODE VIOLATIONS", "BANKRUPTCY", "LIENS CITY/COUNTY", "LIENS OTHER",
    "LIENS UTILITY", "LIENS HOA", "LIENS MECHANIC", "EVICTION",
    "30-60 DAYS", "JUDGEMENT", "DEBT COLLECTION",
]

LABEL_MAP = {
    "HIGH EQUITY": "High Equity", "DEFAULT RISK": "Default Risk", "55+": "55+",
    "ABSENTEE": "Absentee", "DOWNSIZING": "Downsizing", "VACANT": "Vacant",
    "PRE-FORECLOSURE": "Pre-Foreclosure", "ESTATE": "Estate", "TAXES": "Taxes",
    "POOR CONDITION": "Poor Condition", "INTER FAMILY TRANSFER": "Inter Family Transfer",
    "DIVORCE": "Divorce", "PROBATE": "Probate", "LOW CREDIT": "Low Credit",
    "CODE VIOLATIONS": "Code Violations", "BANKRUPTCY": "Bankruptcy",
    "LIENS CITY/COUNTY": "City/County Lien", "LIENS OTHER": "Other Lien",
    "LIENS UTILITY": "Utility Lien", "LIENS HOA": "HOA Lien",
    "LIENS MECHANIC": "Mechanic Lien", "EVICTION": "Eviction",
    "30-60 DAYS": "30-60 Days", "JUDGEMENT": "Judgement",
    "DEBT COLLECTION": "Debt Collection",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def possessive(name: str) -> str:
    """Grammatically correct possessive: names ending in s get apostrophe only."""
    return name + "'" if name.lower().endswith("s") else name + "'s"


def oxford_join(items: list[str]) -> str:
    """Join with Oxford comma: 'A, B, and C'."""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + f", and {items[-1]}"


def is_active(series: pd.Series, col: str) -> pd.Series:
    """Per protocol Section 2.3: ABSENTEE active when 1 or 2; all others active when 1."""
    if col == "ABSENTEE":
        return series.isin([1, 2])
    return series == 1


def pick_signal_row(group: pd.DataFrame) -> tuple[pd.Series, bool]:
    """
    Per analysis_notes.md Section 2 (Signal Reading Rule):
    Use the row where PERIOD == MFR month exactly.
    If MFR falls outside the data window, use the closest available period.
    Returns (row, is_fallback).
    """
    mfr_month = group["MFR_MONTH"].iloc[0]
    exact = group[group["PERIOD"] == mfr_month]
    if len(exact) > 0:
        return exact.iloc[0], False
    periods = group["PERIOD"].values
    try:
        mfr_ts = pd.Period(mfr_month, "M")
        diffs = [abs((pd.Period(p, "M") - mfr_ts).n) for p in periods]
        return group.iloc[int(np.argmin(diffs))], True
    except Exception:
        return group.iloc[0], True


def encode_logo(path: Path) -> str:
    """Return a base64 data URI for a PNG logo, or empty string if not found."""
    if not path.exists():
        return ""
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{data}"


def find_free_port(start: int = 8766) -> int:
    for port in range(start, start + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", port)) != 0:
                return port
    raise RuntimeError("No free port found in range.")


# ---------------------------------------------------------------------------
# Analysis — protocol Section 3, Step 4
# ---------------------------------------------------------------------------

def run_analysis(window_start: str | None, window_end: str | None) -> dict:
    print("  Loading sold-properties data...")
    df = pd.read_excel(DATA_FILE, sheet_name="Sold properties on fulfillment")

    df["LAST SALE DATE"] = pd.to_datetime(df["LAST SALE DATE"], errors="coerce")
    df["MARKETING FIRST RECOMMENDATION"] = pd.to_datetime(
        df["MARKETING FIRST RECOMMENDATION"], errors="coerce"
    )
    df["MFR_MONTH"] = df["MARKETING FIRST RECOMMENDATION"].dt.to_period("M").astype(str)
    df["PERIOD"] = df["PERIOD"].astype(str).str.strip()

    # Inclusion criterion: LAST SALE DATE within analysis window (analysis_notes.md Section 1)
    if window_start and window_end:
        ws = pd.Timestamp(window_start)
        we = pd.Timestamp(window_end) + pd.offsets.MonthEnd(0)
        df = df[(df["LAST SALE DATE"] >= ws) & (df["LAST SALE DATE"] <= we)]

    available_signals = [c for c in SIGNAL_COLS if c in df.columns]

    # Pick one row per FOLIO at the MFR period (signal reading rule)
    rows, fallback_flags = [], []
    for _, group in df.groupby("FOLIO"):
        row, is_fb = pick_signal_row(group)
        rows.append(row)
        fallback_flags.append(is_fb)

    adf = pd.DataFrame(rows).reset_index(drop=True)
    adf["IS_FALLBACK"] = fallback_flags

    for col in available_signals:
        adf[col] = pd.to_numeric(adf[col], errors="coerce")
        adf[f"{col}_active"] = is_active(adf[col], col).astype(int)

    adf["SIGNAL_COUNT"] = adf[[f"{c}_active" for c in available_signals]].sum(axis=1)

    def active_signals_str(row: pd.Series) -> str:
        parts = []
        for col in available_signals:
            if row.get(f"{col}_active", 0) == 1:
                label = LABEL_MAP.get(col, col.title())
                if col == "ABSENTEE" and row[col] == 2:
                    label = "Absentee (OOS)"
                parts.append(label)
        return ", ".join(parts) if parts else "&#8212;"

    adf["ACTIVE_SIGNALS_STR"] = adf.apply(active_signals_str, axis=1)

    # Total fulfillment row count
    if ROW_COUNT_FILE.exists():
        total_rows = int(ROW_COUNT_FILE.read_text().strip())
    else:
        total_rows = 0

    dov_total  = pd.read_excel(OVERVIEW_FILE, sheet_name="Total").iloc[0]
    dov_county = pd.read_excel(OVERVIEW_FILE, sheet_name="By County")

    # All counties in the client's BuyBox (from Distress Overview) — drives report tiering
    all_buybox_counties = sorted(dov_county["COUNTY"].dropna().astype(str).tolist())

    return {
        "adf": adf,
        "available_signals": available_signals,
        "total_rows": total_rows,
        "dov_total": dov_total,
        "dov_county": dov_county,
        "all_buybox_counties": all_buybox_counties,
    }


# ---------------------------------------------------------------------------
# HTML builder
# ---------------------------------------------------------------------------

def build_html(
    client_name: str,
    analysis: dict,
    report_date: str = "March 2026",
    window_label: str = "Oct \u2013 Dec 2025",
) -> str:
    adf                  = analysis["adf"]
    available_signals    = analysis["available_signals"]
    total_rows           = analysis["total_rows"]
    dov_total            = analysis["dov_total"]
    all_buybox_counties  = analysis["all_buybox_counties"]
    n                    = len(adf)

    # ---- Signal summary (sorted descending) ----
    sig_summary = sorted(
        [(LABEL_MAP.get(c, c), int(adf[f"{c}_active"].sum()))
         for c in available_signals if adf[f"{c}_active"].sum() > 0],
        key=lambda x: x[1], reverse=True,
    )
    sig_summary = [(lbl, cnt, round(cnt / n * 100, 1)) for lbl, cnt in sig_summary]

    # ---- Signal stack distribution ----
    stack = adf["SIGNAL_COUNT"].value_counts().sort_index()

    # ---- County data — include ALL BuyBox counties, even those with 0 matched sales ----
    county_data = {}
    for county, grp in adf.groupby("COUNTY"):
        cn   = len(grp)
        sigs = {LABEL_MAP.get(c, c): int(grp[f"{c}_active"].sum())
                for c in available_signals if grp[f"{c}_active"].sum() > 0}
        top3 = sorted(sigs.items(), key=lambda x: x[1], reverse=True)[:3]
        county_data[county] = {"n": cn, "pct": round(cn / n * 100, 1), "top3": top3, "all": sigs}

    # Add BuyBox counties with no matched sales (e.g. Edgefield)
    for county in all_buybox_counties:
        if county not in county_data:
            county_data[county] = {"n": 0, "pct": 0.0, "top3": [], "all": {}}

    n_buybox_counties  = len(all_buybox_counties)
    n_matched_counties = len([c for c in county_data if county_data[c]["n"] > 0])
    # Protocol tiering is based on counties WITH active matched sales (not total BuyBox):
    #   2–4 matched counties → standard structure
    #   5–6 matched counties → adapted Page 3 (ranked summary table, no side-by-side bars)
    #   7+  matched counties → portfolio report + per-county briefs

    # ---- Monthly volume ----
    adf["SALE_MONTH"] = adf["LAST SALE DATE"].dt.to_period("M")
    monthly = adf["SALE_MONTH"].value_counts().sort_index()

    # ---- Buyer / owner type ----
    owner_type   = adf["OWNER TYPE"].value_counts() if "OWNER TYPE" in adf.columns else pd.Series(dtype=int)
    investor_cnt = int(owner_type.get("Company", 0)) + int(owner_type.get("Trust", 0))
    investor_pct = round(investor_cnt / n * 100) if n else 0

    # ---- Key metrics ----
    avg_signals      = round(float(adf["SIGNAL_COUNT"].mean()), 2)
    multi_signal_cnt = int((adf["SIGNAL_COUNT"] >= 2).sum())
    multi_signal_pct = round(multi_signal_cnt / n * 100)
    zero_signal_cnt  = int((adf["SIGNAL_COUNT"] == 0).sum())
    zero_signal_pct  = round(zero_signal_cnt / n * 100, 1)
    nonzero_pct      = round((n - zero_signal_cnt) / n * 100, 1)

    # dominant_counties: sorted by matched count (includes zeros at end)
    dominant_counties  = sorted(county_data.keys(), key=lambda c: county_data[c]["n"], reverse=True)
    # matched_counties: only those with at least 1 matched sale (for narrative titles)
    matched_counties   = [c for c in dominant_counties if county_data[c]["n"] > 0]
    counties_str       = " \u00b7 ".join(sorted(county_data.keys()))
    client_poss        = possessive(client_name)

    top_labels = [s[0] for s in sig_summary]
    top1 = top_labels[0] if len(top_labels) > 0 else ""
    top2 = top_labels[1] if len(top_labels) > 1 else ""
    top3_lbl = top_labels[2] if len(top_labels) > 2 else ""

    # ---- Cover title — Atlas style: factual, readable ----
    cover_title = (
        f"Of the {n} properties on {client_poss} fulfillment list that were sold"
        f" during this period, these are the distress signals that were active"
        f" at the time of delivery"
    )

    # ---- Page 2 action title — Atlas style ----
    # Build "between Month Year and Month Year" from window_label (e.g. "Oct – Dec 2025")
    if len(sig_summary) >= 2:
        p2_title = (
            f"At {client_poss} request, 8020REI reviewed {n} fulfillment properties"
            f" confirmed sold between {window_label}"
            f" \u2014 {top1} and {top2} were the most consistently active signals"
            f" at the time of delivery"
        )
    else:
        p2_title = (
            f"At {client_poss} request, 8020REI reviewed {n} fulfillment properties"
            f" confirmed sold between {window_label}"
        )

    # ---- Page 3 action title — adapted based on matched county count ----
    # Standard (2–4 matched): side-by-side county comparison, Atlas-style title
    # Adapted (5–6 matched): ranked summary table, broader title
    if n_matched_counties >= 5:
        p3_title = (
            f"{top1} + {top2} hold as the leading signals across"
            f" {client_poss} {n_matched_counties} active markets \u2014"
            f" each county shows a distinct signal mix that warrants separate outreach messaging"
        )
    elif len(matched_counties) >= 2:
        p3_title = (
            f"{matched_counties[0]} and {matched_counties[1]} show the same signal"
            f" pattern \u2014 {top1} + {top2} \u2014 confirming the finding holds"
            f" across {client_poss} active markets"
        )
    elif matched_counties:
        p3_title = (
            f"{matched_counties[0]} confirms the signal pattern \u2014 {top1} and {top2}"
            f" were the most active signals across {client_poss} market"
        )
    else:
        p3_title = f"Signal patterns across {client_poss} active markets"

    # ---- County interpretation (concise, one sentence per county) ----
    county_interp_parts = []
    for county in sorted(county_data.keys()):
        d = county_data[county]
        top_two = oxford_join([s for s, _ in d["top3"][:2]]) if d["top3"] else "no dominant signal"
        county_interp_parts.append(
            f"{county}\u2019s profile is led by {top_two}, pointing to distinct"
            f" seller motivation that warrants tailored outreach messaging."
        )
    county_interp = " ".join(county_interp_parts)

    # ---- Tier signals for recommendations ----
    def tier_signals(county: str, n_sigs: int) -> str:
        d = county_data.get(county, {})
        top = [s for s, _ in d.get("top3", [])[:n_sigs]]
        return " + ".join(top) if top else top1

    tier1_county = dominant_counties[0] if dominant_counties else ""
    tier2_county = dominant_counties[1] if len(dominant_counties) > 1 else tier1_county
    tier1_sigs   = tier_signals(tier1_county, 3)
    tier2_sigs   = tier_signals(tier2_county, 2)

    # ---- Track B: lowest-volume, highest-urgency signal present ----
    low_vol_candidates = ["Pre-Foreclosure", "Divorce", "Judgement", "Bankruptcy", "Eviction"]
    track_b_sig = next(
        (lbl for lbl in low_vol_candidates if any(s == lbl for s, *_ in sig_summary)),
        "Pre-Foreclosure"
    )
    track_b_cnt = next((cnt for lbl, cnt, _ in sig_summary if lbl == track_b_sig), 0)

    # ---- Default Risk in distress universe ----
    has_dr  = "DEFAULT RISK_active" in adf.columns
    dr_sold = int(adf["DEFAULT RISK_active"].sum()) if has_dr else 0
    dr_pct  = round(dr_sold / n * 100, 1) if n else 0

    # ---- Logos (base64 embedded — no HTTP server needed) ----
    logo_full_src = encode_logo(LOGO_FULL)
    logo_icon_src = encode_logo(LOGO_ICON)

    # ---- CSS: load canonical report.css, add distress-specific overrides ----
    base_css = REPORT_CSS_FILE.read_text(encoding="utf-8") if REPORT_CSS_FILE.exists() else ""

    # Supplemental CSS: match the FreedomREI proven spacing to prevent overflow,
    # add components not in report.css (bar chart, page-header border, annex).
    # Values here deliberately match the FreedomREI reference HTML which fits 11in pages.
    supplemental_css = """
/* ---- DISTRESS REPORT — SUPPLEMENTAL ---- */

/* Page header border + children (report.css defines container only) */
.page-header {
  border-bottom: 1px solid #d4d4d4;
  padding-bottom: 10px;
  margin-bottom: 24px;
}
.page-header img  { height: 20px; }
.page-header span { font-size: 0.75rem; color: #999999; }

/* Hard clip — prevent any content from bleeding past the page boundary */
.page { overflow: hidden; }

/* Spacing overrides — match FreedomREI reference (proven to fit 11in pages) */
.action-title  { font-size: 1.2rem; margin-bottom: 24px; padding-bottom: 12px; }
.kpi-row       { margin-bottom: 28px; }
.kpi-card      { padding: 16px 20px; }
.kpi-value     { font-size: 1.875rem; }
.insight-box   { padding: 14px 18px; margin-bottom: 24px; }
.insight-box p { font-size: 0.875rem; }
.two-col       { gap: 28px; margin-bottom: 24px; }
.col h3        { font-size: 0.9375rem; margin-bottom: 12px; padding-bottom: 6px; }
table th       { padding: 6px 6px 6px 0; font-size: 0.6875rem; }
table td       { padding: 6px 6px 6px 0; font-size: 0.8125rem; }
ul.bullet-list li { font-size: 0.875rem; margin-bottom: 6px; }

/* Cover — tighter than report.css defaults to leave room for long titles */
.cover-logo         { margin-bottom: 48px; }
.cover-logo img     { height: 48px; }
.cover-divider      { margin-bottom: 24px; }
.cover-title        { font-size: 2.25rem; margin-bottom: 12px; }
.cover-subtitle     { font-size: 0.9375rem; margin-bottom: 32px; }
.cover-meta         { display: flex; gap: 32px; flex-wrap: wrap; margin-bottom: 32px; }
.cover-meta-item    { font-size: 11px; color: #666; }
.cover-meta-item strong { display: block; font-size: 12px; color: #1a1a1a; margin-bottom: 1px; }

/* Footer — center span: no letter-spacing at larger size to prevent blur on long names */
.page-footer .footer-client {
  font-size: 0.6875rem;
  letter-spacing: 0;
  color: #999999;
}

/* Bar chart component */
.bar-row   { display: flex; align-items: center; gap: 10px; margin-bottom: 5px; }
.bar-label { font-size: 11px; color: #2d2d2d; width: 130px; flex-shrink: 0; text-align: right; }
.bar-track { flex: 1; background: #f0f0f0; height: 13px; position: relative; }
.bar-fill  { height: 100%; background: #0B5394; }
.bar-pct   { font-size: 10px; font-weight: 700; color: #0B5394; width: 38px; flex-shrink: 0; }
.bar-n     { font-size: 10px; color: #666; width: 28px; flex-shrink: 0; text-align: right; }

/* Flowing sections — signal breakdown, recommendations, annex: no fixed height */
.annex-page {
  width: 8.5in;
  margin: 0 auto;
  padding: 48px 56px 48px;
  position: relative;
  background: #ffffff;
  page-break-inside: auto;
  page-break-before: always;
}
@media screen { .annex-page { border: 1px solid #d4d4d4; margin-bottom: 24px; } }

/* Table header repeats on page break */
.annex-page thead { display: table-header-group; }
.annex-page table th { font-size: 0.5625rem; padding: 4px 4px 4px 0; }
.annex-page table td { font-size: 0.625rem;  padding: 3px 4px 3px 0; }
.annex-page table tr { page-break-inside: avoid; }

/* flow-footer: static footer for flowing sections — never fixed, never repeats */
.flow-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 0.625rem;
  color: #999999;
  letter-spacing: 0.05em;
  border-top: 1px solid #d4d4d4;
  padding-top: 10px;
  margin-top: 32px;
}
.flow-footer a { color: #999999; text-decoration: none; }
.flow-footer .footer-client { font-size: 0.6875rem; letter-spacing: 0; color: #999999; }
"""

    # ====================================================================
    # Sub-component HTML builders
    # ====================================================================

    def bar_rows_html() -> str:
        """Bar chart — cap at 12 rows so the left column never overflows."""
        if not sig_summary:
            return ""
        display = sig_summary[:12]
        max_pct = display[0][2]
        rows = []
        for label, cnt, pct in display:
            w = round(pct / max_pct * 100, 1) if max_pct else 0
            rows.append(
                f"<div class='bar-row'>"
                f"<span class='bar-label'>{label}</span>"
                f"<div class='bar-track'><div class='bar-fill' style='width:{w}%'></div></div>"
                f"<span class='bar-pct'>{pct}%</span>"
                f"<span class='bar-n'>{cnt}</span>"
                f"</div>"
            )
        return "\n      ".join(rows)

    def stack_rows_html() -> str:
        rows = []
        for sig_count, cnt in stack.items():
            pct   = round(int(cnt) / n * 100, 1)
            label = f"{int(sig_count)} signal{'s' if sig_count != 1 else ''}"
            rows.append(
                f"<tr><td>{label}</td>"
                f"<td class='num'>{int(cnt)}</td>"
                f"<td class='num'>{pct}%</td></tr>"
            )
        return "\n          ".join(rows)

    def county_rows_html() -> str:
        rows = []
        for county in sorted(county_data.keys()):
            d = county_data[county]
            if d["n"] > 0:
                top3_str = " &middot; ".join(
                    f"{s}&nbsp;{round(c / d['n'] * 100)}%" for s, c in d["top3"]
                )
            else:
                top3_str = "<span style='color:#aaa'>No matched transactions this period</span>"
            rows.append(
                f"<tr><td><strong>{county}</strong></td>"
                f"<td class='num'>{d['n']}</td>"
                f"<td class='num'>{d['pct']}%</td>"
                f"<td style='font-size:10px'>{top3_str}</td></tr>"
            )
        return "\n          ".join(rows)

    def owner_rows_html() -> str:
        rows = []
        for ot, cnt in owner_type.items():
            rows.append(
                f"<tr><td>{ot}</td>"
                f"<td class='num'>{int(cnt)}</td>"
                f"<td class='num'>{round(int(cnt) / n * 100, 1)}%</td></tr>"
            )
        return "\n          ".join(rows)

    def monthly_rows_html() -> str:
        month_names = {
            "01": "January", "02": "February", "03": "March", "04": "April",
            "05": "May", "06": "June", "07": "July", "08": "August",
            "09": "September", "10": "October", "11": "November", "12": "December",
        }
        rows = []
        for period, cnt in monthly.items():
            ps = str(period)
            try:
                yr, mo = ps.split("-")
                label  = f"{month_names.get(mo, mo)} {yr}"
            except ValueError:
                label = ps
            rows.append(f"<tr><td>{label}</td><td class='num'>{int(cnt)}</td></tr>")
        return "\n          ".join(rows)

    def dov_rows_html() -> str:
        dov_order = [
            ("HIGH EQUITY", "High Equity"), ("55+", "55+"),
            ("ABSENTEE", "Absentee"), ("DOWNSIZING", "Downsizing"),
            ("VACANT", "Vacant"), ("ESTATE", "Estate"), ("TAXES", "Taxes"),
            ("PRE-FORECLOSURE", "Pre-Foreclosure"), ("POOR CONDITION", "Poor Condition"),
            ("INTER FAMILY TRANSFER", "Inter Family Transfer"),
            ("PROBATE", "Probate"), ("DIVORCE", "Divorce"),
            ("JUDGEMENT", "Judgement"), ("CODE VIOLATIONS", "Code Violations"),
            ("BANKRUPTCY", "Bankruptcy"),
        ]
        rows = []
        for col, label in dov_order:
            if col not in dov_total.index:
                continue
            universe = int(dov_total[col])
            if universe == 0:
                continue
            sold_cnt = int(adf[f"{col}_active"].sum()) if f"{col}_active" in adf.columns else 0
            sold_str = f"{sold_cnt} ({round(sold_cnt / n * 100, 1)}%)" if n else "0 (0%)"
            rows.append(
                f"<tr><td>{label}</td>"
                f"<td class='num'>{universe:,}</td>"
                f"<td class='num'>{sold_str}</td></tr>"
            )
        return "\n          ".join(rows)

    def signal_breakdown_table_html() -> str:
        """Atlas-style signal breakdown table — only counties with matched sold properties as columns."""
        # Exclude counties with 0 matched sales: they add no signal data
        active_counties = sorted(c for c in county_data if county_data[c]["n"] > 0)
        county_headers = "".join(
            f"<th class='num'>{c.upper()}</th>" for c in active_counties
        )
        rows = []
        for lbl, cnt, pct in sig_summary:
            county_cells = ""
            for county in active_counties:
                d  = county_data[county]
                cc = d["all"].get(lbl, 0)
                county_cells += f"<td class='num'>{cc}&nbsp;({round(cc/d['n']*100)}%)</td>"
            rows.append(
                f"<tr><td>{lbl}</td>"
                f"<td class='num'>{cnt}</td>"
                f"<td class='num'>{pct}%</td>"
                f"{county_cells}</tr>"
            )
        return f"""<table>
        <thead>
          <tr>
            <th>Signal</th>
            <th class="num">Count</th>
            <th class="num">% of Total ({n})</th>
            {county_headers}
          </tr>
        </thead>
        <tbody>
          {"".join(rows)}
        </tbody>
      </table>"""

    def annex_rows_html() -> str:
        adf_sorted    = adf.sort_values(["COUNTY", "ADDRESS"]).reset_index(drop=True)
        rows          = []
        current_county = None
        for _, row in adf_sorted.iterrows():
            county = row["COUNTY"]
            if county != current_county:
                rows.append(
                    f"<tr style='background:#E8F0FE'>"
                    f"<td colspan='7' style='font-family:Georgia,serif;font-weight:700;"
                    f"font-size:11px;padding:8px 4px 4px'>{county} County</td></tr>"
                )
                current_county = county
            folio     = str(row.get("FOLIO", ""))
            address   = str(row.get("ADDRESS", ""))
            city      = str(row.get("CITY", ""))
            addr_full = f"{address}, {city}" if city and city not in ("", "nan") else address
            owner_tp  = str(row.get("OWNER TYPE", ""))
            mfr       = row["MARKETING FIRST RECOMMENDATION"]
            mfr_str   = mfr.strftime("%b %Y") if pd.notna(mfr) else ""
            fb_note   = (
                ' <span style="color:#B45309;font-size:8px">(approx.)</span>'
                if row["IS_FALLBACK"] else ""
            )
            sale_date = row["LAST SALE DATE"]
            sale_str  = sale_date.strftime("%b %d, %Y") if pd.notna(sale_date) else ""
            signals   = row["ACTIVE_SIGNALS_STR"]
            rows.append(
                f"<tr>"
                f"<td>{county}</td>"
                f"<td>{addr_full}</td>"
                f"<td style='font-size:9px'>{folio}</td>"
                f"<td>{owner_tp}</td>"
                f"<td>{mfr_str}{fb_note}</td>"
                f"<td>{sale_str}</td>"
                f"<td>{signals}</td>"
                f"</tr>"
            )
        return "\n      ".join(rows)

    # ====================================================================
    # Counties with no matched transactions — flag for report callout
    # ====================================================================
    zero_counties = [c for c in all_buybox_counties if county_data[c]["n"] == 0]
    if zero_counties:
        zc_list = oxford_join(zero_counties)
        zc_universe = ", ".join(
            f"{c}: {int(analysis['dov_county'].loc[analysis['dov_county']['COUNTY']==c, 'HIGH EQUITY'].values[0]):,} properties in distress universe"
            if 'HIGH EQUITY' in analysis['dov_county'].columns and len(analysis['dov_county'].loc[analysis['dov_county']['COUNTY']==c]) > 0
            else c
            for c in zero_counties
        )
        zero_county_flag_html = f"""<div class="insight-box warn" style="margin-top:12px">
        <p><strong>Note \u2014 {zc_list}:</strong> No matched sold properties were recorded
        in {"this county" if len(zero_counties) == 1 else "these counties"} during {window_label}.
        {"It" if len(zero_counties) == 1 else "They"} {"is" if len(zero_counties) == 1 else "are"}
        active in {client_poss} BuyBox and included in the distress universe, but produced no
        transactions to analyse during this window. The repeat analysis scheduled for September 2026
        will clarify whether this reflects a quiet period or a structural gap in that market.</p>
      </div>"""
    else:
        zero_county_flag_html = ""

    # ====================================================================
    # Distress Risk note (Default Risk is not in platform overview)
    # ====================================================================
    dr_note_html = (
        f"<p style='font-size:10px;color:#666;margin-top:4px'>"
        f"Default Risk is a platform-computed score and does not appear in the universe"
        f" counts above. {dr_sold} sold properties ({dr_pct}%) carried it at delivery.</p>"
    ) if has_dr and dr_sold > 0 else ""

    # ====================================================================
    # Assemble HTML
    # ====================================================================
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{client_name} \u2014 Fulfillment Distress Analysis \u2014 {report_date}</title>
  <style>
{base_css}
{supplemental_css}
  </style>
</head>
<body>

<button class="download-btn" onclick="window.print()">&#8595; Download PDF</button>

<!-- ============================================================
     PAGE 1 — COVER
     ============================================================ -->
<section class="page cover">
  <div class="cover-logo">
    <img src="{logo_full_src}" alt="8020REI">
  </div>
  <div class="cover-divider"></div>
  <h1 class="cover-title">{cover_title}</h1>
  <p class="cover-subtitle">
    Fulfillment Distress Analysis &middot; {window_label} &middot; Prepared {report_date}
  </p>
  <div class="cover-meta">
    <div class="cover-meta-item"><strong>Client</strong>{client_name}</div>
    <div class="cover-meta-item"><strong>Analysis Window</strong>{window_label}</div>
    <div class="cover-meta-item"><strong>Counties</strong>{counties_str}</div>
    <div class="cover-meta-item"><strong>Matched Properties</strong>{n} sold</div>
    <div class="cover-meta-item"><strong>Report Type</strong>Fulfillment Distress Analysis</div>
  </div>
  <span class="cover-confidential">{client_name}</span>
  <footer class="page-footer">
    <span><a href="https://8020rei.com">8020rei.com</a></span>
    <span class="footer-client">{client_name}</span>
    <span>Page 1</span>
  </footer>
</section>


<!-- ============================================================
     PAGE 2 — SIGNAL ANALYSIS
     ============================================================ -->
<section class="page">
  <div class="page-header">
    <img src="{logo_icon_src}" alt="8020REI">
    <span>{client_name} &middot; Fulfillment Distress Analysis &middot; {report_date}</span>
  </div>
  <span class="section-label">Situation &amp; Key Finding</span>
  <p class="action-title">{p2_title}</p>
  <div class="kpi-row">
    <div class="kpi-card">
      <div class="kpi-label">Properties Reviewed</div>
      <div class="kpi-value">{n}</div>
      <div class="kpi-context">Sold within {window_label}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Counties</div>
      <div class="kpi-value">{n_buybox_counties}</div>
      <div class="kpi-context">{counties_str}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Top Signal</div>
      <div class="kpi-value">{sig_summary[0][2] if sig_summary else 0}%</div>
      <div class="kpi-context">{top1} of all sold properties</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Multi-Signal</div>
      <div class="kpi-value">{multi_signal_pct}%</div>
      <div class="kpi-context">Held 2 or more signals at delivery</div>
    </div>
  </div>
  <div class="insight-box">
    <p><strong>Key finding:</strong> {nonzero_pct}% of matched properties carried at least one
    active distress signal at delivery &mdash; and {multi_signal_pct}% carried two or more.
    Signal stacking is the pattern that defines a transacting property in {client_poss} market.</p>
  </div>
  <div class="two-col">
    <div class="col">
      <h3>Active Signals at Time of Delivery</h3>
      <p style="font-size:11px;color:#666;margin-bottom:10px">Value&nbsp;=&nbsp;1 at Marketing First Recommendation period. {n}&nbsp;matched properties.</p>
      {bar_rows_html()}
    </div>
    <div class="col">
      <h3>Signal Stack Distribution</h3>
      <p style="font-size:11px;color:#666;margin-bottom:10px">Active signals per sold property at delivery.</p>
      <table>
        <thead><tr><th>Active Signals</th><th class="num">Properties</th><th class="num">Share</th></tr></thead>
        <tbody>
          {stack_rows_html()}
        </tbody>
      </table>
      <div style="margin-top:12px">
        <p style="font-size:12px;color:#2d2d2d;font-weight:700;margin-bottom:4px">Important framing</p>
        <p style="font-size:12px;color:#2d2d2d;line-height:1.55">
          {top1} and {top2} appear most frequently because they are the largest distress
          segments in this market &mdash; not because they are uniquely predictive alone.
          Their value is as amplifiers: a property stacking multiple signals is a meaningfully
          higher-urgency target than any single flag in isolation.
        </p>
      </div>
    </div>
  </div>
  <footer class="page-footer">
    <span><a href="https://8020rei.com">8020rei.com</a></span>
    <span class="footer-client">{client_name}</span>
    <span>Page 2</span>
  </footer>
</section>


<!-- ============================================================
     PAGE 3 — MARKET CONTEXT
     ============================================================ -->
<section class="page">
  <div class="page-header">
    <img src="{logo_icon_src}" alt="8020REI">
    <span>{client_name} &middot; Fulfillment Distress Analysis &middot; {report_date}</span>
  </div>
  <span class="section-label">Supporting Evidence</span>
  <p class="action-title">{p3_title}</p>
  <div class="two-col">
    <div class="col">
      <h3>County Breakdown &mdash; Matched Sold Properties</h3>
      <table>
        <thead>
          <tr><th>County</th><th class="num">Sold</th><th class="num">Share</th><th>Top Signals</th></tr>
        </thead>
        <tbody>
          {county_rows_html()}
        </tbody>
      </table>
      {zero_county_flag_html}
    </div>
    <div class="col">
      <h3>Buyer Type &mdash; Who Purchased These Properties</h3>
      <table>
        <thead><tr><th>Buyer Type</th><th class="num">Properties</th><th class="num">Share</th></tr></thead>
        <tbody>
          {owner_rows_html()}
        </tbody>
      </table>
      <p style="font-size:12px;color:#2d2d2d;margin-top:6px;margin-bottom:10px">
        <strong>{investor_pct}% of matched properties sold to investor entities</strong>
        (company or trust). These buyers operate with pre-approved financing and dedicated
        acquisition teams &mdash; advantages that only close the window faster once a property
        is identified.
      </p>
      <h3 style="margin-top:10px">Monthly Sale Volume</h3>
      <table>
        <thead><tr><th>Month</th><th class="num">Properties Sold</th></tr></thead>
        <tbody>
          {monthly_rows_html()}
        </tbody>
      </table>
    </div>
  </div>
  <footer class="page-footer">
    <span><a href="https://8020rei.com">8020rei.com</a></span>
    <span class="footer-client">{client_name}</span>
    <span>Page 3</span>
  </footer>
</section>


<!-- ============================================================
     PAGE 3B — SIGNAL BREAKDOWN (flows across pages as needed)
     ============================================================ -->
<section class="annex-page">
  <div class="page-header">
    <img src="{logo_icon_src}" alt="8020REI">
    <span>{client_name} &middot; Fulfillment Distress Analysis &middot; {report_date}</span>
  </div>
  <span class="section-label">Supporting Evidence</span>
  <p class="action-title" style="font-size:1rem">
    Distress Signal Breakdown &mdash; All {n} Sold Properties
  </p>
  <p style="font-size:11px;color:#666;margin-bottom:8px">Active signals at time of delivery. Value&nbsp;=&nbsp;1 at Marketing First Recommendation period.</p>
  {signal_breakdown_table_html()}
  <div class="flow-footer">
    <span><a href="https://8020rei.com">8020rei.com</a></span>
    <span class="footer-client">{client_name}</span>
    <span>Page 3b</span>
  </div>
</section>


<!-- ============================================================
     PAGE 4 — RECOMMENDATIONS (flowing — content determines length)
     per protocol Section 4: signal-stack prioritisation, Rapid Response,
     repeat in 6 months, Niche Lists (conditional)
     ============================================================ -->
<section class="annex-page">
  <div class="page-header">
    <img src="{logo_icon_src}" alt="8020REI">
    <span>{client_name} &middot; Fulfillment Distress Analysis &middot; {report_date}</span>
  </div>
  <span class="section-label">Recommendations</span>
  <p class="action-title">
    Acting on these findings now gives {client_name} a direct path to more closed deals
    &mdash; prioritising the right signals, responding faster, and reaching motivated sellers
    before competing buyers engage.
  </p>
  <div class="two-col">
    <div class="col">
      <h3>1. Prioritise Signal-Stacked Properties First</h3>
      <p style="font-size:12px;color:#2d2d2d;margin-bottom:8px">
        Sort and work the fulfillment list by signal count, then by these validated combinations:
      </p>
      <ul class="bullet-list">
        <li><strong>Tier 1 &mdash; {tier1_county} focus:</strong> {tier1_sigs}.
          Any property carrying all of these is the highest-urgency target.
          Outreach within 48&nbsp;hours of delivery.</li>
        <li><strong>Tier 2 &mdash; {tier2_county} focus:</strong> {tier2_sigs}.
          Work within the delivery week.</li>
        <li><strong>Tier 3 &mdash; secondary signals:</strong> {top1} + {top_labels[3] if len(top_labels) > 3 else "Estate"}.
          Lower urgency, lower competition. Include as a weekly sweep.</li>
      </ul>
      <h3>2. Activate Rapid Response</h3>
      <p style="font-size:12px;color:#2d2d2d;margin-bottom:8px">
        The monthly delivery cycle means {client_name} first sees properties 30+ days after they
        enter the market. Rapid Response adds a parallel, same-day channel when a property
        matching the BuyBox first appears in the platform &mdash; without replacing the current
        outreach workflow. It is the direct answer to the speed-to-contact gap investor buyers exploit.
      </p>
      <h3>3. Build Two Niche List Tracks
        <span style="font-size:10px;font-weight:400;color:#666">(if VA capacity allows)</span>
      </h3>
      <ul class="bullet-list">
        <li><strong>Track A &mdash; {top1} + {top2}:</strong> Large pool, validated signal
          combination. Consistent outreach cadence via VA.</li>
        <li><strong>Track B &mdash; {track_b_sig}
          ({track_b_cnt} {"property" if track_b_cnt == 1 else "properties"} in this analysis):</strong>
          Small universe, high seller urgency, low investor competition. Each property is
          more actionable precisely because the pool is small.</li>
      </ul>
    </div>
    <div class="col">
      <h3>Distress Universe &mdash; Platform Overview</h3>
      <p style="font-size:10px;color:#666;margin-bottom:6px">
        Total properties flagged per signal across {client_poss} active counties
        (8020REI platform, {report_date}).
      </p>
      <table>
        <thead>
          <tr>
            <th>Distress Signal</th>
            <th class="num">Platform Total</th>
            <th class="num">Sold ({n})</th>
          </tr>
        </thead>
        <tbody>
          {dov_rows_html()}
        </tbody>
      </table>
      {dr_note_html}
      <h3 style="margin-top:10px">Next Steps</h3>
      <table>
        <thead><tr><th>Action</th><th>Owner</th><th>By</th></tr></thead>
        <tbody>
          <tr><td>Present findings and signal-stack tiers to {client_name}</td><td>CSM</td><td>Apr 2026</td></tr>
          <tr><td>Configure BuyBox weighting for Tier 1 signal stack</td><td>Client + CSM</td><td>Apr 2026</td></tr>
          <tr><td>Activate Rapid Response for top counties</td><td>Client</td><td>Apr 2026</td></tr>
          <tr><td>Evaluate VA capacity for Niche List Tracks A and B</td><td>Client</td><td>Apr 2026</td></tr>
          <tr><td>Schedule repeat Fulfillment Distress Analysis</td><td>CSM</td><td>Sep 2026</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="flow-footer">
    <span><a href="https://8020rei.com">8020rei.com</a></span>
    <span class="footer-client">{client_name}</span>
    <span>Page 4</span>
  </div>
</section>


<!-- ============================================================
     ANNEX — flows across as many pages as needed
     ============================================================ -->
<section class="annex-page">
  <div class="page-header">
    <img src="{logo_icon_src}" alt="8020REI">
    <span>{client_name} &middot; Fulfillment Distress Analysis &middot; {report_date} &middot; Annex</span>
  </div>
  <span class="section-label">Annex</span>
  <p class="action-title" style="font-size:1rem">
    All {n} matched properties sorted by county &mdash; signals read at Marketing First
    Recommendation period. <span style="color:#B45309">Amber</span> = closest available period used (MFR outside data window).
  </p>
  <table>
    <thead>
      <tr>
        <th>County</th>
        <th>Address</th>
        <th>Folio</th>
        <th>Owner Type</th>
        <th>First Rec.</th>
        <th>Sale Date</th>
        <th>Active Signals at Delivery</th>
      </tr>
    </thead>
    <tbody>
      {annex_rows_html()}
    </tbody>
  </table>
  <div class="flow-footer">
    <span><a href="https://8020rei.com">8020rei.com</a></span>
    <span class="footer-client">{client_name}</span>
    <span>Annex</span>
  </div>
</section>

</body>
</html>"""


# ---------------------------------------------------------------------------
# PDF export — uses file:// URL (logos embedded as base64, no server needed)
# ---------------------------------------------------------------------------

def export_pdf(html_path: Path, pdf_path: Path) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  [WARN] Playwright not installed. Run: pip install playwright && python -m playwright install chromium")
        print("  Skipping PDF export.")
        return

    url = html_path.as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page    = browser.new_page()
        page.goto(url)
        page.wait_for_load_state("networkidle")
        page.pdf(
            path=str(pdf_path),
            format="Letter",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Step 4: Generate HTML report and PDF for any client."
    )
    parser.add_argument("client_name", help="Full client name, e.g. 'SOS Home Offers'")
    parser.add_argument("client_slug", help="Short identifier for filenames, e.g. 'soshomeoffers'")
    parser.add_argument(
        "--window", nargs=2, metavar=("START", "END"), default=[None, None],
        help="Analysis window YYYY-MM YYYY-MM, e.g. --window 2025-10 2025-12",
    )
    _today = datetime.date.today()
    _default_report_date = _today.strftime("%B %Y")
    parser.add_argument("--report-date", default=_default_report_date)
    parser.add_argument("--window-label", default=None)
    args = parser.parse_args()

    window_start, window_end = args.window

    window_label = args.window_label
    if not window_label and window_start and window_end:
        abbr = {"01":"Jan","02":"Feb","03":"Mar","04":"Apr","05":"May","06":"Jun",
                "07":"Jul","08":"Aug","09":"Sep","10":"Oct","11":"Nov","12":"Dec"}
        sy, sm = window_start.split("-")
        ey, em = window_end.split("-")
        window_label = (
            f"{abbr[sm]} \u2013 {abbr[em]} {sy}"
            if sy == ey else
            f"{abbr[sm]} {sy} \u2013 {abbr[em]} {ey}"
        )
    elif not window_label:
        window_label = "All available data"

    print()
    print("=" * 60)
    print(f"  STEP 4 \u2014 GENERATE REPORT")
    print(f"  Client : {args.client_name}")
    print(f"  Slug   : {args.client_slug}")
    print(f"  Window : {window_label}")
    print("=" * 60)

    for label, path in [
        ("Analysis data",     DATA_FILE),
        ("Distress overview", OVERVIEW_FILE),
        ("report.css",        REPORT_CSS_FILE),
        ("Logo (full)",       LOGO_FULL),
        ("Logo (icon)",       LOGO_ICON),
    ]:
        if not path.exists():
            print(f"  [WARN] {label} not found: {path}")

    if not DATA_FILE.exists():
        print(f"\n[ERROR] Analysis data not found. Run main.py first.")
        sys.exit(1)
    if not OVERVIEW_FILE.exists():
        print(f"\n[ERROR] Distress overview not found. Run main.py first.")
        sys.exit(1)

    print("\n  Running analysis...")
    analysis = run_analysis(window_start, window_end)
    n = len(analysis["adf"])
    print(f"  {n} matched sold properties.")

    print("  Building HTML...")
    html = build_html(
        client_name=args.client_name,
        analysis=analysis,
        report_date=args.report_date,
        window_label=window_label,
    )

    # Determine file stem from window end (or today)
    if window_end:
        yr, mo = window_end.split("-")[:2]
        stem   = f"{yr}-{mo}-distress-analysis-{args.client_slug}"
    else:
        import datetime
        stem = datetime.date.today().strftime("%Y-%m") + f"-distress-analysis-{args.client_slug}"

    html_path = PIPELINE_ROOT / f"{stem}.html"
    pdf_path  = PIPELINE_ROOT / f"{stem}.pdf"

    html_path.write_text(html, encoding="utf-8")
    print(f"  HTML : {html_path}")

    print("  Exporting PDF...")
    export_pdf(html_path, pdf_path)

    if pdf_path.exists():
        print(f"  PDF  : {pdf_path}")
    else:
        print("  PDF export skipped or failed.")

    print()
    print("=" * 60)
    print(f"  DONE \u2014 {args.client_name}")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
