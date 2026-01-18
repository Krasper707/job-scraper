# cleaner_logic.py

import pandas as pd
import ast

def clean_data(raw_df):
    """
    Takes a raw pandas DataFrame, cleans and validates it,
    and returns a cleaned DataFrame.
    """
    if raw_df is None or raw_df.empty:
        print("Input DataFrame is empty. No data to clean.")
        return pd.DataFrame()

    df = raw_df.copy()

    # 1. Handle Duplicates
    df.sort_values('date_posted', ascending=False, inplace=True)
    df.drop_duplicates(subset=['job_title', 'company'], keep='first', inplace=True)

    # 2. Filter Out Promotional Content
    promo_keywords = ['bootcamp', 'guaranteed', 'money back']
    df = df[~df['job_title'].str.contains('|'.join(promo_keywords), case=False, na=False)]

    # 3. Normalize Job Titles
    df['normalized_title'] = df['job_title'].str.lower()
    title_replacements = {
        r'\bml\b': 'machine learning', 'software engineer': 'swe',
        'data scientist': 'ds', 'data analyst': 'da', 'product manager': 'pm'
    }
    for pattern, replacement in title_replacements.items():
        df['normalized_title'] = df['normalized_title'].str.replace(pattern, replacement, regex=True)

    # 4. Process and Clean Tags (tags are already a list, just ensure they are strings)
    df['tags'] = df['tags'].apply(lambda x: [str(tag) for tag in x] if isinstance(x, list) else [])

    # 5. Validate Dates
    df['date_posted'] = pd.to_datetime(df['date_posted'], errors='coerce')
    df.dropna(subset=['date_posted'], inplace=True)
    
    print(f"Data cleaned. {len(df)} jobs remaining.")
    return df