"""
01_fulfillment_merger/merge.py
------------------------------
Merges all monthly fulfillment Excel files from the input/ folder into a
single Excel file in output/, adding a PERIOD column (e.g. 2025-07) derived
from each filename.

Expected filename format: YYYY-MM-DD <Client> <anything>.xlsx
Run from the pipeline/ root via main.py, or directly from this folder.
"""

import re
from pathlib import Path

import pandas as pd

INPUT_DIR  = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"


def extract_period(filename: str) -> str:
    """Return 'YYYY-MM' from filename, or 'UNKNOWN' if not found."""
    match = re.search(r"(\d{4}-\d{2})", filename)
    return match.group(1) if match else "UNKNOWN"


def run(client_name: str) -> Path:
    """
    Merge all xlsx files in input/ and write the result to output/.
    Returns the path of the merged output file.
    """
    print()
    print("=" * 60)
    print(f"  STEP 1 -- FULFILLMENT MERGE")
    print(f"  Client: {client_name}")
    print("=" * 60)

    xlsx_files = sorted(INPUT_DIR.glob("*.xlsx"))

    if not xlsx_files:
        raise FileNotFoundError(
            f"\n[ERROR] No .xlsx files found in:\n  {INPUT_DIR}\n"
            "Add the monthly fulfillment files to that folder and run again."
        )

    print(f"\nFiles found in input/ ({len(xlsx_files)}):")
    frames = []
    for fp in xlsx_files:
        period = extract_period(fp.name)
        print(f"  {fp.name}  ->  period {period}")
        df = pd.read_excel(fp, dtype=str)
        df.insert(0, "PERIOD", period)
        frames.append(df)

    total_rows = sum(len(f) for f in frames)
    print(f"\nMerging {total_rows:,} total rows...")
    merged = pd.concat(frames, ignore_index=True, sort=False)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"{client_name}_Merged_Fulfillments.xlsx"

    print(f"Writing output: {output_file.name} ...")
    merged.to_excel(output_file, index=False, engine="openpyxl")

    periods = sorted(merged["PERIOD"].unique())
    print(f"\n[OK] Merge complete.")
    print(f"  Total rows    : {len(merged):,}")
    print(f"  Total columns : {len(merged.columns)}")
    print(f"  Periods       : {', '.join(periods)}")
    print(f"  Output        : {output_file}")

    return output_file


if __name__ == "__main__":
    client = input("\nClient name: ").strip() or "Client"
    run(client)
