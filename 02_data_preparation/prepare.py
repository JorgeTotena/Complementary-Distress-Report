"""
02_data_preparation/prepare.py
-------------------------------
Joins the merged fulfillments file with the COO (sold properties) file.

Input folder expects:
  - *_Merged_Fulfillments.parquet  (auto-copied from step 1 output)
  - A COO xlsx file             (any .xlsx whose name contains 'COO' or 'sold',
                                 case-insensitive — or the only other xlsx present)

Output:
  - output/Data ready for analysis.parquet
      Sheet 1: "Fulfillment properties"         -- all rows (left join)
      Sheet 2: "Sold properties on fulfillment" -- only rows with a matched sale date

Join key : FOLIO + ADDRESS + ZIP
COO cols appended: LAST SALE DATE, MARKETING FIRST RECOMMENDATION, YEAR BUILT,
                   COO MARKETING DM COUNT, MARKETING CC COUNT, MARKETING SMS COUNT
"""

import shutil
import sys
from pathlib import Path

import pandas as pd

INPUT_DIR  = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"

JOIN_KEYS = ["FOLIO", "ADDRESS", "ZIP"]

COO_COLS = JOIN_KEYS + [
    "LAST SALE DATE",
    "MARKETING FIRST RECOMMENDATION",
    "YEAR BUILT",
    "MARKETING DM COUNT",
    "MARKETING CC COUNT",
    "MARKETING SMS COUNT",
]

COO_RENAME = {"MARKETING DM COUNT": "COO MARKETING DM COUNT"}

# Uppercase set used for usecols filtering when reading the COO xlsx
_COO_COLS_UPPER = frozenset(c.upper() for c in COO_COLS)


def find_fulfillments_file() -> Path:
    """Find the merged fulfillments file in input/ (parquet preferred, xlsx fallback)."""
    candidates = sorted(INPUT_DIR.glob("*Merged_Fulfillments*.parquet"))
    if candidates:
        return candidates[0]
    candidates = sorted(INPUT_DIR.glob("*Merged_Fulfillments*.xlsx"))
    if not candidates:
        raise FileNotFoundError(
            f"\n[ERROR] Merged fulfillments file not found in:\n  {INPUT_DIR}\n"
            "Make sure Step 1 has been run first."
        )
    return candidates[0]


def find_coo_file() -> Path:
    """
    Find the COO file in input/. Looks for any xlsx whose name contains
    'COO' or 'sold' (case-insensitive). If not found, prompts the user.
    """
    all_xlsx = sorted(INPUT_DIR.glob("*.xlsx"))

    # Try to exclude the fulfillments file, but don't fail if it isn't there
    # (it may have been passed in-memory from the merge step)
    try:
        fulfillments_file = find_fulfillments_file()
    except FileNotFoundError:
        fulfillments_file = None

    # Exclude the fulfillments file itself
    candidates = [
        f for f in all_xlsx
        if f != fulfillments_file
        and ("coo" in f.name.lower() or "sold" in f.name.lower())
    ]

    # Fallback: any other xlsx that is not the fulfillments file
    if not candidates:
        candidates = [f for f in all_xlsx if f != fulfillments_file]

    if not candidates:
        print(f"\n[WARNING] COO file not found in:\n  {INPUT_DIR}\n")
        while True:
            answer = input(
                "Add the COO file to 02_data_preparation/input/ "
                "and press Enter to continue (or type 'exit' to cancel): "
            ).strip().lower()
            if answer == "exit":
                sys.exit(0)
            candidates = [
                f for f in sorted(INPUT_DIR.glob("*.xlsx"))
                if f != fulfillments_file
            ]
            if candidates:
                break
            print("  File not detected yet. Try again.")

    if len(candidates) > 1:
        print(f"\n  Multiple COO file candidates found:")
        for i, f in enumerate(candidates):
            print(f"    [{i + 1}] {f.name}")
        while True:
            try:
                choice = int(input("  Which one to use? Enter the number: ").strip())
                if 1 <= choice <= len(candidates):
                    return candidates[choice - 1]
            except ValueError:
                pass
            print("  Invalid number.")
    else:
        return candidates[0]


def normalize_keys(df: pd.DataFrame, keys: list) -> pd.DataFrame:
    for col in keys:
        df[col] = df[col].astype(str).str.strip().str.upper()
    return df


def run(client_name: str, fulfillments_source, fulfillments_path: Path = None) -> Path:
    """
    Join merged fulfillments with COO file and write the output.
    fulfillments_source may be a pre-loaded DataFrame (passed from merge step)
    or a Path (for standalone use). Returns the path of the output file.
    """
    print()
    print("=" * 60)
    print(f"  STEP 2 -- DATA PREPARATION")
    print(f"  Client: {client_name}")
    print("=" * 60)
    print(f"\nStarting data preparation for {client_name}...\n")

    # -- Locate COO file -------------------------------------------------------
    coo_path = find_coo_file()
    print(f"  [OK] COO file: {coo_path.name}")

    # -- Read / receive fulfillments -------------------------------------------
    if isinstance(fulfillments_source, pd.DataFrame):
        # DataFrame passed in-memory from merge step — no file I/O needed
        fulfillments = fulfillments_source.copy()
        print(f"\nUsing in-memory merged fulfillments ({len(fulfillments):,} rows)")
    else:
        # Fallback: treat fulfillments_source as a Path
        src_path = Path(fulfillments_source)
        dest_fulfillments = INPUT_DIR / src_path.name
        print(f"Copying merged fulfillments to input/...")
        shutil.copy2(src_path, dest_fulfillments)
        print(f"  [OK] {src_path.name} copied to 02_data_preparation/input/")
        print(f"\nReading merged fulfillments...")
        if dest_fulfillments.suffix == ".parquet":
            fulfillments = pd.read_parquet(dest_fulfillments)
        else:
            fulfillments = pd.read_excel(dest_fulfillments, dtype=str)
        print(f"  {len(fulfillments):,} rows, {len(fulfillments.columns)} columns")

    print(f"Reading COO file (loading {len(COO_COLS)} needed columns only)...")
    coo = pd.read_excel(
        coo_path, dtype=str,
        usecols=lambda col: col.strip().upper() in _COO_COLS_UPPER,
    )
    print(f"  {len(coo):,} rows, {len(coo.columns)} columns")

    # -- Validate required columns ---------------------------------------------
    missing_join = [c for c in JOIN_KEYS if c not in fulfillments.columns]
    if missing_join:
        raise ValueError(f"[ERROR] Missing join columns in fulfillments: {missing_join}")

    missing_coo = [c for c in COO_COLS if c not in coo.columns]
    if missing_coo:
        raise ValueError(f"[ERROR] Missing columns in COO file: {missing_coo}")

    # -- Normalize & join ------------------------------------------------------
    print(f"\nNormalizing join keys (FOLIO + ADDRESS + ZIP)...")
    fulfillments = normalize_keys(fulfillments, JOIN_KEYS)
    coo = normalize_keys(coo, JOIN_KEYS)

    coo_subset = coo[COO_COLS].rename(columns=COO_RENAME)

    dupes = coo_subset.duplicated(subset=JOIN_KEYS, keep=False).sum()
    if dupes:
        print(f"  Warning: {dupes} duplicate rows in COO (FOLIO+ADDRESS+ZIP) -- keeping first occurrence.")
        coo_subset = coo_subset.drop_duplicates(subset=JOIN_KEYS, keep="first")

    print(f"Joining...")
    merged = fulfillments.merge(coo_subset, on=JOIN_KEYS, how="left")

    matched = merged["LAST SALE DATE"].notna().sum()
    sold = merged[merged["LAST SALE DATE"].notna() & (merged["LAST SALE DATE"].str.strip() != "")]

    print(f"  {matched:,} of {len(merged):,} rows matched a COO record")
    print(f"  {len(sold):,} rows with LAST SALE DATE -> sold properties")

    # -- Write output ----------------------------------------------------------
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / "Data ready for analysis.parquet"

    print(f"\nWriting output: {output_file.name} ...")
    sold.to_parquet(output_file, index=False)

    # Persist the total fulfillment row count for the report generator.
    (OUTPUT_DIR / "fulfillment_row_count.txt").write_text(str(len(merged)))

    print(f"\n[OK] Data ready for analysis.")
    print(f"  Output : {output_file}")
    print(f"  Fulfillment properties (total) : {len(merged):,} rows  [count stored in fulfillment_row_count.txt]")
    print(f"  Sold properties on fulfillment : {len(sold):,} rows  [written to Excel]")

    return output_file


if __name__ == "__main__":
    client = input("\nClient name: ").strip() or "Client"
    merged_path = find_fulfillments_file()
    run(client, merged_path)
