from datetime import date

def update_velocity(conn):
    """
    * Gets today's date using date.today() from the datetime module
    * Updates date_last_seen to today for all active postings using a SQL UPDATE statement
    * Queries the database for postings where date_last_seen is not equal to date_first_seen — these have been alive more than one day
    * Flags postings as expired_fast = 1 where the difference between date_last_seen and date_first_seen is 2 days or less and the posting is no longer in the current batch
    * Returns the count of fast-expired postings
    """
    
    if conn is None:
        return 0
    
    cursor = conn.cursor()
    today = str(date.today())
    
    cursor.execute(""" 
        UPDATE postings
        SET date_last_seen = ?
    """, (today,))
    
    cursor.execute("""
        SELECT COUNT(*)
        FROM postings
        WHERE julianday(date_last_seen) - julianday(date_first_seen) <= 2
        AND date_last_seen != date_first_seen
    """)
    count = cursor.fetchone()[0]
    
    cursor.execute("""
        UPDATE postings
        SET expired_fast = 1
        WHERE julianday(date_last_seen) - julianday(date_first_seen) <= 2
        AND date_last_seen != date_first_seen
    """)
    conn.commit()
    
    return count
    