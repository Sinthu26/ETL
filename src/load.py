import logging
from datetime import date

log = logging.getLogger(__name__)

def load_data(df, conn):
    """
    * Creates a cursor
    * Loops through the DataFrame rows with df.iterrows()
    * Uses INSERT or IGNORE to insert each row into the postings table
    * Commits after the loop
    * Returns the number of rows instead
    """
    # Checks if the DataFrame is empty to prevent the pipeline from crashing
    if df is None or df.empty:
        log.error("Received empty or None DataFrame - nothing to load")
        return 0
    
    today = str(date.today())
    
    cursor = conn.cursor()
    
    new_rows = 0
    # If the database insert fails, undo all the changes so the database stays clean
    try:
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT OR IGNORE INTO postings (posting_id, job_title, city, province, salary_maximum, has_salary, date_first_seen, date_last_seen) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (row["posting_id"], row["job_title"], row["city"], row["province"], row["salary_maximum"], row["has_salary"], today, today))
            if cursor.rowcount == 1:
                new_rows += 1
            cursor.execute("""
                UPDATE postings
                SET date_last_seen = ?
                WHERE posting_id = ?
            """, (today, row["posting_id"]))
        conn.commit()
    except Exception as e:
        log.error(f"Failed to insert rows: {e}")
        conn.rollback()
        return 0
    
    return new_rows
