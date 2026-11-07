# This file downloads the data required for this project from the UC Irvine ML Repository
# Data Source: Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D.

import time
import argparse
import pandas as pd
from pathlib import Path

DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00502/online_retail_II.xlsx"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_PATH = DATA_DIR / "raw_online_retail_II.csv"
    
def fetch_raw_data(force=False):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if OUTPUT_PATH.exists() and not force:
        print(f"[!] File already exists: {OUTPUT_PATH}")
        print("[*] Skipping download. Use --force to overwrite.")
        return

    print(f"[*] Extracting raw data from : {DATA_URL}")

    try:
        start_time = time.time()

        df = pd.read_excel(DATA_URL, engine="calamine")
        df.to_csv(OUTPUT_PATH, index=False)

        if not OUTPUT_PATH.exists() or OUTPUT_PATH.stat().st_size == 0:
            raise RuntimeError("[!] Output CSV is missing or empty.")

        elapsed_time = time.time() - start_time

    except Exception as e:
        raise RuntimeError(f"[!] Data ingestion failed: {e}") from e

    print(f"[*] Completed in {elapsed_time:.2f} seconds.")
    print(f"[+] Saved locally to: {OUTPUT_PATH}")
    print(f"[+] Record Count: {len(df)} rows X {len(df.columns)} columns")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download and Convert the UCI Online Retail II dataset."
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the existing CSV file."
    )

    args = parser.parse_args()
    fetch_raw_data(force=args.force)