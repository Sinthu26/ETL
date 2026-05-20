import logging
import pandas as pd

log = logging.getLogger(__name__)

def has_salary(salary):
    if salary > 0:
        return 1
    return 0

REQUIRED_COLUMNS = ["Job Title", "City", "Province/Territory", "Salary Maximum", "WIC Job Location Snapshot ID"]

def clean_data(df):
    """
    * Takes a raw DataFrame as input
    * Drops rows missing "Job Title" or "City"
    * Filters to Ontario, British Columbia, Alberta, and Québec
    * Fills missing "Salary Maximum" with 0
    * Adds a has_salary column - 1 if salary is greater than 0, 0 if not
    * Renames these four columns to clean names with no spaces or special characters:
        * "WIC Job Location Snapshot ID" → "posting_id"
        * "Job Title" → "job_title"
        * "City" → "city"
        * "Province/Territory" → "province"
        * "Salary Maximum" → "salary_maximum"
    * Returns a clean DataFrame
    """
    
    # Checks if df is None or empty at the very start since cleaning it would produce meaningless results
    if df is None or df.empty:
        log.error("Recieved empty or None DataFrame - nothing to clean")
        return None 
    
    # Checks that all requried columns exist before filtering - guards it by checking that the expected columns exist
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        log.error(f"Raw data is missing expected columns: {missing}")
        return None
    
    df = df.dropna(subset=["Job Title", "City"])
    
    df = df[df["Province/Territory"].isin([ "Ontario", "British Columbia", "Alberta", "Québec"])]
    
    # Checks if the result is empty after the province filter - adds a warning that the DataFrame is empty after cleaning
    if df.empty:
        log.warning("DataFrame is empty after cleaning - check source data")
        return None
    
    df["Salary Maximum"] = df["Salary Maximum"].fillna(0)
    
    df["has_salary"] = df["Salary Maximum"].apply(has_salary)
    
    df = df.rename(columns={
        "WIC Job Location Snapshot ID" : "posting_id",
        "Job Title" : "job_title",
        "City" : "city",
        "Province/Territory" : "province",
        "Salary Maximum" : "salary_maximum"
    })
    
    
    return df
    