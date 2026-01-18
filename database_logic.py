# database_logic.py

import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = 'data/jobs.db'

def setup_database():
    """Creates the database and the jobs table if they don't exist."""
    print(f"Setting up database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT,
            date_posted TIMESTAMP,
            tags TEXT,
            normalized_title TEXT,
            category TEXT, -- New column for job type
            scrape_run_date TIMESTAMP NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Database and 'jobs' table are ready.")

def store_data(cleaned_df):
    """Takes a cleaned DataFrame and inserts it into the SQLite database."""
    if cleaned_df is None or cleaned_df.empty:
        print("No data to store in the database.")
        return

    df = cleaned_df.copy()
    
    df['scrape_run_date'] = datetime.now()
    # Convert list of tags to a comma-separated string for DB storage
    df['tags'] = df['tags'].apply(lambda tags_list: ','.join(tags_list))
    
    conn = sqlite3.connect(DB_PATH)
    try:
        df.to_sql('jobs', conn, if_exists='append', index=False)
        print(f"Successfully inserted/updated {len(df)} job records into the database.")
    except Exception as e:
        print(f"An error occurred during data insertion: {e}")
    finally:
        conn.close()