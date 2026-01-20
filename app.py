# app.py (Corrected and Professional Version)

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import sqlite3
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg') # Set non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import time # <-- Import the time module for unique filenames

# Import your refactored logic modules
from scraper_logic import run_scraper 
from cleaner_logic import clean_data
from database_logic import store_data, setup_database
from reporter_logic import generate_report

app = Flask(__name__)
app.secret_key = 'supersecretkey' 

JOB_URLS = {
    'support': 'remote-support-jobs', 'engineer': 'remote-engineer-jobs',
    'software': 'remote-software-jobs', 'senior': 'remote-senior-jobs',
    'technical': 'remote-technical-jobs', 'management': 'remote-management-jobs',
    'growth': 'remote-growth-jobs', 'lead': 'remote-lead-jobs',
    'design': 'remote-design-jobs', 'sales': 'remote-sales-jobs',
    'marketing': 'remote-marketing-jobs', 'security': 'remote-security-jobs'
}

REPORTS_DIR = 'reports'

@app.route('/')
def index():
    job_categories = list(JOB_URLS.keys())
    # Ensure this is passing the integer timestamp, not the function itself
    return render_template('index.html', job_categories=job_categories, now=int(time.time()))

@app.route('/generate', methods=['POST'])
def generate():
    # This route is correct
    data = request.get_json()
    job_type = data.get('job_type')
    if not job_type or job_type not in JOB_URLS:
        return jsonify({'status': 'error', 'message': 'Invalid job type selected.'}), 400

    url_slug = JOB_URLS[job_type]
    scrape_url = f"https://remoteok.com/{url_slug}"
    
    raw_df = run_scraper(scrape_url)
    if raw_df is None or raw_df.empty:
        return jsonify({'status': 'error', 'message': f"Could not find jobs for '{job_type}'."}), 500
        
    cleaned_df = clean_data(raw_df)
    cleaned_df['category'] = job_type 
    store_data(cleaned_df)
    report_path = generate_report(category=job_type) 
    
    if report_path and os.path.exists(report_path):
        filename = os.path.basename(report_path)
        return jsonify({'status': 'success', 'filename': filename})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to generate the report file.'}), 500

@app.route('/download/<path:filename>')
def download(filename):
    # This route is correct
    return send_from_directory(REPORTS_DIR, filename, as_attachment=True)

def get_all_categories_from_db():
    # This function is correct
    conn = sqlite3.connect('data/jobs.db')
    try:
        df = pd.read_sql_query("SELECT DISTINCT category FROM jobs", conn)
        return sorted(df['category'].dropna().tolist())
    finally:
        conn.close()

@app.route('/dashboard')
def dashboard():
    selected_category = request.args.get('category', 'software')
    
    # <<< CHANGE: Generate a unique timestamp for this specific request >>>
    # This will be used to create unique filenames to prevent concurrency issues.
    unique_id = int(time.time())

    # --- 1. Data and Plot for 30-Day Trend ---
    conn = sqlite3.connect('data/jobs.db')
    try:
        thirty_days_ago = datetime.now() - timedelta(days=30)
        query_trend = """
            SELECT date(date_posted) as post_date, COUNT(*) as job_count
            FROM jobs WHERE category = ? AND date_posted >= ?
            GROUP BY post_date ORDER BY post_date ASC
        """
        trend_df = pd.read_sql_query(query_trend, conn, params=(selected_category, thirty_days_ago))
    finally:
        conn.close()

    plt.figure(figsize=(12, 6))
    plt.plot(pd.to_datetime(trend_df['post_date']), trend_df['job_count'], marker='o', linestyle='-')
    plt.title(f'Daily Job Postings for "{selected_category.title()}" (Last 30 Days)', fontsize=16)
    plt.xlabel('Date'); plt.ylabel('Number of Jobs'); plt.grid(True); plt.tight_layout()
    # <<< CHANGE: Use the unique ID in the filename >>>
    trend_chart_path = f'static/trend_{selected_category}_{unique_id}.png'
    plt.savefig(trend_chart_path)
    plt.close()

    # --- 2. Data and Plot for Skills Comparison ---
    conn = sqlite3.connect('data/jobs.db')
    try:
        sixty_days_ago = datetime.now() - timedelta(days=60)
        # <<< CHANGE: Fix the logical bug by adding "category = ?" to the query >>>
        query_skills = "SELECT date_posted, tags FROM jobs WHERE category = ? AND date_posted >= ?"
        skills_df = pd.read_sql_query(query_skills, conn, params=(selected_category, sixty_days_ago))
        skills_df['date_posted'] = pd.to_datetime(skills_df['date_posted'])
    finally:
        conn.close()

    one_month_ago = datetime.now() - timedelta(days=30)
    df_this_month = skills_df[skills_df['date_posted'] >= one_month_ago]
    df_last_month = skills_df[skills_df['date_posted'] < one_month_ago]

    # Handle cases where one of the months might have no data
    if not df_this_month.empty:
        skills_this_month = df_this_month['tags'].str.split(',').explode().str.strip().value_counts().head(10)
    else:
        skills_this_month = pd.Series()
        
    if not df_last_month.empty:
        skills_last_month = df_last_month['tags'].str.split(',').explode().str.strip().value_counts().head(10)
    else:
        skills_last_month = pd.Series()

    comparison_df = pd.DataFrame({'This Month': skills_this_month, 'Last Month': skills_last_month}).fillna(0).astype(int)

    if not comparison_df.empty:
        comparison_df.plot(kind='barh', figsize=(12, 8))
        plt.title(f'Top Skills for "{selected_category.title()}": This Month vs. Last Month', fontsize=16)
        plt.xlabel('Number of Mentions'); plt.gca().invert_yaxis(); plt.tight_layout()
        # <<< CHANGE: Use the unique ID in the filename >>>
        comparison_chart_path = f'static/skills_comparison_{selected_category}_{unique_id}.png'
        plt.savefig(comparison_chart_path)
        plt.close()
    else:
        comparison_chart_path = None # Set to None if no data to plot

    return render_template(
        'dashboard.html',
        trend_chart=trend_chart_path,
        comparison_chart=comparison_chart_path,
        all_categories=get_all_categories_from_db(),
        selected_category=selected_category,
        # <<< CHANGE: Pass the 'now' value for cache busting >>>
        now=int(time.time()) 
    )

if __name__ == '__main__':
    if not os.path.exists(REPORTS_DIR): os.makedirs(REPORTS_DIR)
    if not os.path.exists('data'): os.makedirs('data')
    if not os.path.exists('static'): os.makedirs('static') # <-- Add check for static dir
    setup_database()
    app.run(debug=True)