# This file downloads the data required for this project from the UC Irvine ML Repository
# Data Source: Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D.

import os
import pandas as pd
import time as t

DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00502/online_retail_II.xlsx"

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
OUTPUT_PATH = os.path.join(DATA_DIR, "online_retail_II.csv")
    
def fetch_raw_data():
    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(OUTPUT_PATH):
        print(f"[!] Local file already exists: {OUTPUT_PATH}")

        choice = input("Do you want to overwrite it? (y/n): ").strip().lower()
        if choice != "y":
            print("[*] Exiting without overwriting the file.")
            return

    print(f"[*] Extracting raw data from :\n {DATA_URL}")

    try:
        start_time = t.time()

        try:
            print("[*] Attempting to read Excel file using 'calamine' engine...")
            df = pd.read_excel(DATA_URL, engine="calamine")
        
        except Exception:
            print("[!] Failed to read Excel file with 'calamine' engine. Trying default engine...")
            df = pd.read_excel(DATA_URL)
       
        df.to_csv(OUTPUT_PATH, index=False)

        elapsed_time = t.time() - start_time

        print(f"[*] Download completed in {elapsed_time:.2f} seconds.")
        print(f"[+] Saved locally to: {OUTPUT_PATH}")
        print(f"[+] Record Count: {len(df)} rows X {len(df.columns)} columns")
    
    except Exception as e:
        raise Exception(f"[!] Download failed: {e}")


if __name__ == "__main__":
    fetch_raw_data()