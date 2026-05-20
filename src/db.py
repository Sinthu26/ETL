import sqlite3
import os
import logging

log = logging.getLogger(__name__)
DATAPATH = "data/canadalens.db"

def get_connection():
    """
    * Connects to data/canadalens.db
    * Creates a table called postings if it doesn't exist with the following columns:
        * postings_id (TEXT, PRIMARY KEY)
        * job_title(TEXT)
        * city (TEXT)
        * province (TEXT)
        * salary_maximum (REAL)
        * has_salary (INTEGER)
    * Then returns the connection
    """
    
    # First run may not have a data/ folder yet - create it safely
    os.makedirs("data", exist_ok=True)
    
    try:
        conn = sqlite3.connect(DATAPATH)
        # WAL mode allows safe concurrent reads during pipeline writes
        conn.execute("PRAGMA journal_mode=WAL")
    except sqlite3.OperationalError as e:
        log.error(f"Could not connect to database: {e}")
        return None
    
    cursor = conn.cursor()
    try: 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS postings (
                posting_id      TEXT PRIMARY KEY,
                job_title       TEXT,
                city            TEXT,
                province        TEXT,
                salary_maximum  REAL,
                has_salary      INTEGER,
                date_first_seen TEXT,
                date_last_seen  TEXT,
                expired_fast    INTEGER DEFAULT 0
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        log.error(f"Failed to create table: {e}")
        conn.close()
        return None
    
    return conn
    