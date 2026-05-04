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
  03_distress_overview/input/   <- place one or more COO xlsx files here.
                                   Multiple files are merged automatically.

Output:
  03_distress_overview/output/Distress Overview.xlsx
    Sheet "By County"     -- signal counts per county (one row per county)
    Sheet "Total"         -- signal counts across all counties combined

Parquet cache: input/_cache.parquet is written after the first xlsx read.
On subsequent runs it is loaded directly if newer than all source xlsx files.
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

FOLIO_COL = "FOLIO"
BUYBOX_COL = "BUYBOX SCORE"
LAST_SALE_COL = "LAST SALE DATE"

# Only load the columns we actually use — county + all signal columns + FOLIO/BUYBOX/SALE
# (needed to match the other Distress Report's logic: dedup by FOLIO keeping the row with
# the most recent LAST SALE DATE, then filter to BUYBOX SCORE > 0 — the addressable universe).
# The usecols callable strips/uppercases so it works regardless of file header casing.
NEEDED_COLS: frozenset[str] = frozenset(
    {COUNTY_COL, FOLIO_COL, BUYBOX_COL, LAST_SALE_COL} | set(STANDARD_SIGNALS) | {ABSENTEE_COL}
)


def load_input_data(input_dir: Path) -> pd.DataFrame:
    """
    Load COO data from input_dir.

    - If a fresh parquet cache exists (newer than all xlsx files), load it.
    - Otherwise read all xlsx files, merge them, and save a parquet cache.
    Multiple xlsx files are merged automatically — no user prompt needed.
    """
    xlsx_files = sorted(
        f for f in input_dir.glob("*.xlsx") if not f.name.startswith("~$")
    )
    if not xlsx_files:
        raise FileNotFoundError(
            f"\n[ERROR] No xlsx file found in {input_dir}\n"
            f"  Place the full COO-format file there and re-run."
        )

    parquet_path = input_dir / "_cache.parquet"
    if parquet_path.exists():
        parquet_mtime = parquet_path.stat().st_mtime
        if all(parquet_mtime > fp.stat().st_mtime for fp in xlsx_files):
            print(f"      [cache] Loading from parquet ({parquet_path.name})")
            return pd.read_parquet(parquet_path)

    _usecols = lambda col: col.strip().upper() in NEEDED_COLS  # noqa: E731

    if len(xlsx_files) == 1:
        print(f"      Reading: {xlsx_files[0].name}")
        df = pd.read_excel(xlsx_files[0], dtype=str, usecols=_usecols)
    else:
        print(f"      Merging {len(xlsx_files)} xlsx files:")
        frames = []
        for fp in xlsx_files:
            print(f"        {fp.name}")
            frames.append(pd.read_excel(fp, dtype=str, usecols=_usecols))
        df = pd.concat(frames, ignore_index=True, sort=False)
        print(f"      Merged: {len(df):,} total rows")

    print(f"      Saving parquet cache: {parquet_path.name} ...")
    df.to_parquet(parquet_path, index=False)
    return df


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

    df = load_input_data(input_dir)
    df.columns = df.columns.str.strip().str.upper()

    # Match the other Distress Report's logic: dedup by FOLIO keeping the row with
    # the most recent LAST SALE DATE, then restrict to the BuyBox universe
    # (BUYBOX SCORE > 0). Without this, raw COO row counts inflate every signal
    # total because the file carries ~167K duplicate FOLIOs and ~1.3M properties
    # outside the buybox.
    if FOLIO_COL in df.columns:
        if LAST_SALE_COL in df.columns:
            df[LAST_SALE_COL] = pd.to_datetime(df[LAST_SALE_COL], errors="coerce")
            df = df.sort_values(LAST_SALE_COL, na_position="first")
        df[FOLIO_COL] = df[FOLIO_COL].astype(str).str.strip().str.upper()
        pre = len(df)
        df = df.drop_duplicates(subset=[FOLIO_COL], keep="last").reset_index(drop=True)
        print(f"      Dedup by FOLIO: {pre:,} -> {len(df):,} rows")

    if BUYBOX_COL in df.columns:
        df[BUYBOX_COL] = pd.to_numeric(df[BUYBOX_COL], errors="coerce").fillna(0)
        pre = len(df)
        df = df[df[BUYBOX_COL] > 0].reset_index(drop=True)
        print(f"      BuyBox filter (BUYBOX SCORE > 0): {pre:,} -> {len(df):,} rows")

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
            f"[ERROR] Column '{COUNTY_COL}' not found in the input data.\n"
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
