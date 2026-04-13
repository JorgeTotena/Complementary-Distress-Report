"""
main.py
-------
Main entry point for the Fulfillment Distress Analysis pipeline.

Steps:
  1. Merge monthly fulfillment files   -> 01_fulfillment_merger/
  2. Data preparation (join with COO)  -> 02_data_preparation/
  3. Distress Overview breakdown       -> 03_distress_overview/

Usage:
  python main.py

Expected structure:
  historical_distress_report/
    main.py                              <- this file
    01_fulfillment_merger/
      input/    <- place monthly fulfillment xlsx files here
      output/   <- generated automatically
      merge.py
    02_data_preparation/
      input/    <- place COO xlsx here; merged file is copied automatically
      output/   <- generates "Data ready for analysis.parquet"
      prepare.py
    03_distress_overview/
      input/    <- place the full COO-format file (all recommended properties)
      output/   <- generates "Distress Overview.xlsx"
      analyze.py
"""

import argparse
import importlib.util
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    parser = argparse.ArgumentParser(
        description="Fulfillment Distress Analysis — pipeline (steps 1, 2, 3)"
    )
    parser.add_argument(
        "client_name",
        nargs="?",
        default=None,
        help="Client name (e.g. 'SOS Home Offers'). Prompts if omitted.",
    )
    args = parser.parse_args()

    print()
    print("=" * 60)
    print("  FULFILLMENT DISTRESS ANALYSIS -- PIPELINE")
    print("=" * 60)

    client_name = args.client_name
    if not client_name:
        client_name = input("\nClient name: ").strip()
    if not client_name:
        print("[ERROR] Client name cannot be empty.")
        sys.exit(1)

    print(f"\nClient   : {client_name}")
    print("Steps    :")
    print("  [1] Merge monthly fulfillment files")
    print("  [2] Distress Overview breakdown")

    root = Path(__file__).parent

    # -- STEP 1: Merge fulfillments -------------------------------------------
    try:
        merge_mod = load_module("merge", root / "01_fulfillment_merger" / "merge.py")
        merge_mod.run(client_name)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    # -- STEP 2: Distress Overview breakdown ----------------------------------
    try:
        analyze_mod = load_module("analyze", root / "03_distress_overview" / "analyze.py")
        analyze_mod.run(client_name)
    except (FileNotFoundError, ValueError) as e:
        print(e)
        sys.exit(1)

    # -- Done -----------------------------------------------------------------
    print()
    print("=" * 60)
    print(f"  PIPELINE COMPLETE -- {client_name}")
    print("=" * 60)
    print(f"\n  Merged fulfillments : 01_fulfillment_merger/output/")
    print(f"  Distress Overview   : 03_distress_overview/output/Distress Overview.xlsx")
    print()


if __name__ == "__main__":
    main()
