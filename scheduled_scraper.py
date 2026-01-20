# scheduled_scraper.py

import pandas as pd

from scraper_logic import run_scraper
from cleaner_logic import clean_data
from database_logic import setup_database, store_data

JOB_CATEGORIES = {
    'support': 'remote-support-jobs',
    'engineer': 'remote-engineer-jobs',
    'software': 'remote-software-jobs',
    'senior': 'remote-senior-jobs',
    'technical': 'remote-technical-jobs',
    'management': 'remote-management-jobs',
    'growth': 'remote-growth-jobs',
    'lead': 'remote-lead-jobs',
    'design': 'remote-design-jobs',
    'sales': 'remote-sales-jobs',
    'marketing': 'remote-marketing-jobs',
    'security': 'remote-security-jobs'
}

def run_daily_pipeline():
    """
    Main function to run the entire data collection pipeline for all categories.
    """
    print("--- Starting Daily Scraping Pipeline ---")
    
    setup_database()
    
    all_new_jobs = []

    # Loop through each category, scrape, and clean the data
    for category_name, url_slug in JOB_CATEGORIES.items():
        scrape_url = f"https://remoteok.com/{url_slug}"
        
        print(f"\n--- Scraping Category: {category_name} ---")
        raw_df = run_scraper(scrape_url)
        
        if raw_df is not None and not raw_df.empty:
            cleaned_df = clean_data(raw_df)
            # Add the category to each job listing
            cleaned_df['category'] = category_name
            all_new_jobs.append(cleaned_df)
    
    if not all_new_jobs:
        print("No new jobs found across all categories. Exiting.")
        return

    # Combine all cleaned dataframes into one
    final_df = pd.concat(all_new_jobs, ignore_index=True)
    
    print(f"\n--- Storing a total of {len(final_df)} new jobs in the database ---")
    # Store the combined dataframe in the database
    store_data(final_df)
    
    print("\n--- Daily Scraping Pipeline Complete ---")

if __name__ == "__main__":
    run_daily_pipeline()