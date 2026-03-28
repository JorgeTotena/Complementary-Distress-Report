"""
analyze.py
----------
Step 3: Distress Overview breakdown.

Reads the full COO-format file (all properties ever recommended for this client,
not just sold ones) and computes how many properties have each distress signal
active, broken down by county.

This replaces the manual screenshot approach for the Distress Overview section
of the HTML report.

Input:
  03_distress_overview/input/   <- place the full COO xlsx here (one file)

Output:
  03_distress_overview/output/Distress Overview.xlsx
    Sheet "By County"     -- signal counts per county (one row per county)
    Sheet "Total"         -- signal counts across all counties combined
"""

import sys
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------------------------
# Signal definitions
# Same encoding rules as analysis_notes.md:
#   standard signals: active when value == 1
#   ABSENTEE: active when value == 1 OR 2
# ---------------------------------------------------------------------------

STANDARD_SIGNALS = [
    # High-volume signals
    "HIGH EQUITY",
    "DEFAULT RISK",
    "DOWNSIZING",
    "TAXES",
    "VACANT",
    "55+",
    "ESTATE",
    # Mid-volume signals
    "PROBATE",
    "LIENS CITY/COUNTY",
    "DIVORCE",
    "PRE-FORECLOSURE",
    "INTER FAMILY TRANSFER",
    "POOR CONDITION",
    "CODE VIOLATIONS",
    "JUDGEMENT",
    "LIENS HOA",
    "LOW CREDIT",
    # Lower-volume signals
    "BANKRUPTCY",
    "DEBT COLLECTION",
    "EVICTION",
    "WATER SHUT OFF",
    "FIRE DAMAGE",
    "AFFIDAVIT",
    "INCARCERATED",
    "DRIVING FOR DOLLARS",
    "FAILED LISTING",
    "FLOOD ZONE",
    "LIENS MECHANIC",
    "LIENS UTILITY",
    "LIENS OTHER",
    "30-60 DAYS",
]

ABSENTEE_COL = "ABSENTEE"

COUNTY_COL = "COUNTY"


def find_input_file(input_dir: Path) -> Path:
    candidates = [
        f for f in input_dir.glob("*.xlsx")
        if not f.name.startswith("~$")
    ]
    if len(candidates) == 0:
        raise FileNotFoundError(
            f"\n[ERROR] No xlsx file found in {input_dir}\n"
            f"  Place the full COO-format file there and re-run."
        )
    if len(candidates) > 1:
        print(f"\n  Multiple files found in {input_dir.name}/input/:")
        for i, f in enumerate(candidates, 1):
            print(f"    [{i}] {f.name}")
        choice = input("  Select file number: ").strip()
        try:
            return candidates[int(choice) - 1]
        except (ValueError, IndexError):
            raise ValueError("[ERROR] Invalid selection.")
    return candidates[0]


def is_active(series: pd.Series, col: str) -> pd.Series:
    """Return boolean Series: True where the signal is active."""
    if col == ABSENTEE_COL:
        return series.isin([1, 2])
    return series == 1


def run(client_name: str) -> Path:
    root = Path(__file__).parent
    input_dir = root / "input"
    output_dir = root / "output"
    output_dir.mkdir(exist_ok=True)

    print(f"\n  [3] Distress Overview breakdown -- {client_name}")

    coo_file = find_input_file(input_dir)
    print(f"      Reading: {coo_file.name}")

    df = pd.read_excel(coo_file, dtype=str)
    df.columns = df.columns.str.strip().str.upper()

    # Coerce signal columns to numeric
    all_signal_cols = STANDARD_SIGNALS + [ABSENTEE_COL]
    for col in all_signal_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Identify which signal columns actually exist in this file
    present_signals = [c for c in STANDARD_SIGNALS if c in df.columns]
    has_absentee = ABSENTEE_COL in df.columns

    if COUNTY_COL not in df.columns:
        raise ValueError(
            f"[ERROR] Column '{COUNTY_COL}' not found in {coo_file.name}.\n"
            f"  Available columns: {list(df.columns)}"
        )

    def count_signals(group: pd.DataFrame) -> pd.Series:
        counts = {}
        for col in present_signals:
            counts[col] = int(is_active(group[col], col).sum())
        if has_absentee:
            counts[ABSENTEE_COL] = int(is_active(group[ABSENTEE_COL], ABSENTEE_COL).sum())
        counts["TOTAL PROPERTIES"] = len(group)
        return pd.Series(counts)

    # By county
    by_county = df.groupby(COUNTY_COL).apply(count_signals).reset_index()

    # Total row
    total_counts = {}
    for col in present_signals:
        total_counts[col] = int(is_active(df[col], col).sum()) if col in df.columns else 0
    if has_absentee:
        total_counts[ABSENTEE_COL] = int(is_active(df[ABSENTEE_COL], ABSENTEE_COL).sum())
    total_counts["TOTAL PROPERTIES"] = len(df)
    total_row = pd.DataFrame([total_counts])

    # Write output
    output_file = output_dir / "Distress Overview.xlsx"
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        by_county.to_excel(writer, sheet_name="By County", index=False)
        total_row.to_excel(writer, sheet_name="Total", index=False)

    print(f"      Output : 03_distress_overview/output/Distress Overview.xlsx")
    print(f"               {len(by_county)} counties | {len(df):,} total properties")

    return output_file


if __name__ == "__main__":
    client = input("Client name: ").strip()
    run(client)
