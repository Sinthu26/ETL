import requests
import pandas as pd
import os
import logging

log = logging.getLogger(__name__)
URL = 'https://open.canada.ca/data/dataset/ea639e28-c0fc-48bf-b5dd-b8899bd43072/resource/e8c27948-6a40-452b-8d7d-2e1b799ca8aa/download/job-bank-open-data-all-job-postings-en-feb2026.csv'
DATAPATH = "data/raw_postings.csv"

def fetch_data():
    """
    * Downloads the Job Bank CSV using requests.get()
    * Saves it to data/raw_postings.csv
    * Loads it into a DataFrame with the correct delimiter and encoding
    * Returns the DataFrame
    """
    
    # Skip download if file exists - avoids re-fetching data on every run
    if not os.path.exists(DATAPATH):
        try:
            response = requests.get(URL, timeout=30)
            response.raise_for_status()
            with open(DATAPATH, "wb") as f:
                f.write(response.content)
        except requests.RequestException as e:
            log.error(f"Failed to download data: {e}")
            return None
            
    df = pd.read_csv(DATAPATH, delimiter="\t", encoding="utf-16")
    
    return df
