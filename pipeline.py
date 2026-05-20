from src.db import get_connection
from src.fetch import fetch_data
from src.transform import clean_data
from src.load import load_data
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

log = logging.getLogger(__name__)

def run():
    log.info("Pipeline starting")
    df = fetch_data()
    if df is None:
        log.error("Fetch failed - stopping pipeline")
        return
    log.info(f"Fetched {len(df)} rows")
    
    result = clean_data(df)
    if result is None:
        log.error("Cleanfailed - stopping pipeline")
        return
    log.info(f"Cleaned to {len(result)} rows")
    
    conn = get_connection()
    if conn is None:
        log.error("Database connection failed - stopping pipeline")
        return
    log.info("Connection to Database established")
    
    new_rows = load_data(result, conn)
    log.info(f"Inserted {new_rows} new rows")
    
    conn.close()
    log.info("Pipeline complete")
    
    





if __name__ == "__main__":
    run()