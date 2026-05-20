from src.db import get_connection
from src.fetch import fetch_data
from src.transform import clean_data
from src.load import load_data
from src.skills import match_skills
from src.velocity import update_velocity
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
        log.error("Clean failed - stopping pipeline")
        return
    log.info(f"Cleaned to {len(result)} rows")
    
    result["skills_found"] = result["job_title"].apply(match_skills)
    total_skills = result["skills_found"].apply(len).sum()
    log.info(f"Extracted {total_skills} skill matches across {len(df)} postings")
    
    conn = get_connection()
    if conn is None:
        log.error("Database connection failed - stopping pipeline")
        return
    log.info("Connection to Database established")
    
    new_rows = load_data(result, conn)
    log.info(f"Inserted {new_rows} new rows")
    
    fast_expired = update_velocity(conn)
    log.info(f"{fast_expired} postings flagged as fast-expiring")
    
    conn.close()
    log.info("Pipeline complete")
    
    





if __name__ == "__main__":
    run()