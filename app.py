# app.py

from flask import Flask, render_template, request,jsonify, send_from_directory, flash, redirect, url_for
import os
from scraper_logic import run_scraper 
from cleaner_logic import clean_data
from database_logic import store_data, setup_database
from reporter_logic import generate_report

app = Flask(__name__)
# A secret key is needed for flashing messages
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
    return render_template('index.html', job_categories=job_categories)

@app.route('/generate', methods=['POST'])
def generate():
    # This route now expects a JSON request from JavaScript
    data = request.get_json()
    job_type = data.get('job_type')

    if not job_type or job_type not in JOB_URLS:
        return jsonify({'status': 'error', 'message': 'Invalid job type selected.'}), 400

    url_slug = JOB_URLS[job_type]
    scrape_url = f"https://remoteok.com/{url_slug}"
    
    print(f"--- Starting pipeline for: {job_type} at {scrape_url} ---")

    raw_df = run_scraper(scrape_url)
    if raw_df is None or raw_df.empty:
        return jsonify({'status': 'error', 'message': f"Could not find jobs for '{job_type}'."}), 500
        
    cleaned_df = clean_data(raw_df)
    cleaned_df['category'] = job_type 
    store_data(cleaned_df)
    
    report_path = generate_report(category=job_type) 
    
    if report_path and os.path.exists(report_path):
        filename = os.path.basename(report_path)
        # Return a success response with the filename for downloading
        return jsonify({'status': 'success', 'filename': filename})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to generate the report file.'}), 500

# --- NEW ROUTE TO HANDLE FILE DOWNLOADS ---
@app.route('/download/<path:filename>')
def download(filename):
    """Serves a file from the reports directory for download."""
    return send_from_directory(REPORTS_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    # Ensure necessary directories exist
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Run the initial database setup
    setup_database()
    
    # Run the Flask app
    app.run(debug=True)