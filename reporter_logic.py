# reporter_logic.py (Updated for OpenRouter)

import sqlite3
import pandas as pd
from datetime import datetime
import matplotlib

import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import os

# <<< CHANGE 1: Import the OpenAI library >>>
# We still use the official 'openai' library
from openai import OpenAI

# --- Configuration ---
DB_PATH = 'data/jobs.db'
REPORTS_DIR = 'reports'
matplotlib.use('Agg')

# <<< CHANGE 2: Your OpenRouter API Key >>>
# For a real project, use environment variables: os.getenv("OPENROUTER_API_KEY")
# NEVER commit your API key to a public Git repository if it's not a free one.
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# <<< CHANGE 3: Create a dedicated OpenAI client configured for OpenRouter >>>
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPENROUTER_API_KEY,
  default_headers={ # Optional, but recommended for identifying your app
    # "HTTP-Referer": "https://github.com/your-repo-name", # Replace with your project URL
    "X-Title": "Remote Job Scraper", # Replace with your project name
  },
)

# def _fetch_data_by_category(category):
#     # This function does not need to change
#     conn = sqlite3.connect(DB_PATH)
#     query = "SELECT * FROM jobs WHERE category = ?"
#     try:
#         df = pd.read_sql_query(query, conn, params=(category,))
#         df['date_posted'] = pd.to_datetime(df['date_posted'])
#         print(f"Fetched {len(df)} records for category '{category}'.")
#         return df
#     finally:
#         conn.close()

# def get_llm_summary(category, top_skills, top_companies):
#     """Sends analysis data to OpenRouter and returns a natural language summary."""
#     skills_str = "\n".join([f"- {skill}: {count} listings" for skill, count in top_skills.items()])
#     companies_str = "\n".join([f"- {company}: {count} listings" for company, count in top_companies.items()])

#     prompt = f"""
#     You are a data analyst writing a summary for a weekly job market report.
#     The report is for the job category: "{category.title()}".
#     Here is the data you need to summarize:
#     Top 10 Most Demanded Skills:
#     {skills_str}
#     Top Companies Hiring for Multiple Roles:
#     {companies_str}
#     Based ONLY on the data provided, write a concise, professional, 2-3 sentence summary of the key hiring trends.
#     Start with a sentence like "In the {category.title()} sector this week...".
#     Do not add any information not present in the data.
#     """

#     print("Generating LLM summary via OpenRouter...")
#     try:
#         # <<< CHANGE 4: Use the custom client and a model available on OpenRouter >>>
#         response = client.chat.completions.create(
#             # Choose a model from openrouter.ai/models. The ':free' suffix uses the free tier.
#             model="openai/gpt-oss-120b:free",
#             messages=[
#                 {"role": "system", "content": "You are a helpful data analyst."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.5,
#             max_tokens=150
#         )
#         summary = response.choices[0].message.content.strip()
#         print("LLM summary generated successfully.")
#         return summary
#     except Exception as e:
#         print(f"Error generating LLM summary via OpenRouter: {e}")
#         return "Summary could not be generated due to an error."

# def generate_report(category):
#     # This function's logic remains almost identical. It just calls the updated get_llm_summary.
#     df = _fetch_data_by_category(category)
#     if df.empty:
#         print(f"No data found for category '{category}'. Cannot generate report.")
#         return None

#     df['tags'] = df['tags'].str.split(',')
#     all_skills = df.explode('tags')['tags'].str.strip().str.lower()
#     all_skills = all_skills[all_skills != '']
#     top_10_skills = all_skills.value_counts().head(10)
#     top_hiring_companies = df['company'].value_counts().loc[lambda x: x > 1].head(10)

#     # --- Call the new OpenRouter-powered summary function ---
#     llm_summary = get_llm_summary(category, top_10_skills, top_hiring_companies)

#     report_date = datetime.now().strftime('%Y%m%d')
#     pdf_report_path = os.path.join(REPORTS_DIR, f'{category}_report_{report_date}.pdf')
#     plot_skills_path = os.path.join(REPORTS_DIR, f'{category}_top_skills.png')

#     plt.figure(figsize=(10, 6))
#     sns.barplot(x=top_10_skills.values, y=top_10_skills.index, palette='viridis')
#     plt.title(f'Top 10 Most Demanded Skills for {category.title()} Roles', fontsize=16)
#     plt.xlabel('Number of Job Postings', fontsize=12)
#     plt.tight_layout()
#     plt.savefig(plot_skills_path)
#     plt.close()
#     pdf=FPDF()

#     pdf.add_page()
    
#     # <<< CHANGE 3: Add the Unicode font to FPDF >>>
#     # This line tells FPDF where to find the font file.
#     pdf.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf', uni=True)
#     pdf.set_font('DejaVu', '', 18) # Set it as the active font

#     pdf.cell(0, 10, f'{category.title()} Jobs Report - {datetime.now().strftime("%Y-%m-%d")}', 0, 1, 'C')
#     pdf.ln(5)

#     pdf.set_font('DejaVu', '', 14) # Use 'B' for bold if you add a bold font file
#     pdf.cell(0, 10, 'Executive Summary', 0, 1)
#     pdf.set_font('DejaVu', '', 12)
    
#     # <<< CHANGE 4: Sanitize the text as a safety measure >>>
#     # This replaces any character that even DejaVu can't handle with a '?'
#     safe_summary = llm_summary.encode('latin-1', 'replace').decode('latin-1')
#     pdf.multi_cell(0, 8, safe_summary)
#     pdf.ln(10)

#     pdf.set_font('DejaVu', '', 14)
#     pdf.cell(0, 10, 'Top 10 Demanded Skills', 0, 1)
#     if os.path.exists(plot_skills_path):
#         pdf.image(plot_skills_path, x=10, y=None, w=180)
    
#     if not top_hiring_companies.empty:
#         pdf.add_page()
#         pdf.set_font('DejaVu', '', 14)
#         pdf.cell(0, 10, 'Companies Hiring for Multiple Roles', 0, 1)
#         pdf.set_font('DejaVu', '', 11)
#         for company, count in top_hiring_companies.items():
#             # Sanitize company names as well, just in case
#             safe_company = company.encode('latin-1', 'replace').decode('latin-1')
#             pdf.cell(0, 8, f"- {safe_company}: {count} positions", 0, 1)

#     pdf.output(pdf_report_path)
#     print(f"PDF report generated successfully at {pdf_report_path}")
    
#     return pdf_report_path


def _fetch_data_by_category(category):
    # This function is correct
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM jobs WHERE category = ?"
    try:
        df = pd.read_sql_query(query, conn, params=(category,))
        df['date_posted'] = pd.to_datetime(df['date_posted'])
        print(f"Fetched {len(df)} records for category '{category}'.")
        return df
    finally:
        conn.close()

def get_llm_summary(category, top_skills, top_companies):
    skills_str = "\n".join([f"- {skill}: {count} listings" for skill, count in top_skills.items()])
    companies_str = "\n".join([f"- {company}: {count} listings" for company, count in top_companies.items()])

    prompt = f"""
    You are a data analyst writing a summary for a weekly job market report. The report is for the job category: "{category.title()}".
    Based ONLY on the data provided (Top Skills: {skills_str}; Top Companies: {companies_str}), write a concise, professional, 2-3 sentence summary of the key hiring trends.
    Start with a sentence like "In the {category.title()} sector this week...". Do not add any information not present in the data.
    """

    print("Generating LLM summary via OpenRouter...")
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b:free", 
            messages=[
                {"role": "system", "content": "You are a helpful data analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            # <<< CHANGE 1: Increase the token limit to prevent truncation >>>
            max_tokens=250 
        )
        summary = response.choices[0].message.content.strip()
        print("LLM summary generated successfully.")
        return summary
    except Exception as e:
        print(f"Error generating LLM summary via OpenRouter: {e}")
        return "Summary could not be generated due to an error."

def generate_report(category):
    df = _fetch_data_by_category(category)
    if df.empty: return None

    df['tags'] = df['tags'].str.split(',')
    all_skills = df.explode('tags')['tags'].str.strip().str.lower()
    all_skills = all_skills[all_skills != '']
    top_10_skills = all_skills.value_counts().head(10)
    top_hiring_companies = df['company'].value_counts().loc[lambda x: x > 1].head(10)

    llm_summary = get_llm_summary(category, top_10_skills, top_hiring_companies)

    report_date = datetime.now().strftime('%Y%m%d')
    pdf_report_path = os.path.join(REPORTS_DIR, f'{category}_report_{report_date}.pdf')
    plot_skills_path = os.path.join(REPORTS_DIR, f'{category}_top_skills.png')

    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_10_skills.values, y=top_10_skills.index, hue=top_10_skills.index, palette='viridis', legend=False)
    plt.title(f'Top 10 Most Demanded Skills for {category.title()} Roles', fontsize=16)
    plt.xlabel('Number of Job Postings', fontsize=12)
    plt.tight_layout()
    plt.savefig(plot_skills_path)
    plt.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 18)

    pdf.cell(0, 10, f'{category.title()} Jobs Report - {datetime.now().strftime("%Y-%m-%d")}', 0, 1, 'C')
    pdf.ln(5)

    pdf.set_font('DejaVu', '', 14)
    pdf.cell(0, 10, 'Executive Summary', 0, 1)
    pdf.set_font('DejaVu', '', 12)
    
    # <<< CHANGE 2: Remove the aggressive sanitization and pass raw text >>>
    # We trust the DejaVu font to handle the Unicode characters from the LLM.
    pdf.multi_cell(0, 8, llm_summary)
    pdf.ln(10)

    pdf.set_font('DejaVu', '', 14)
    pdf.cell(0, 10, 'Top 10 Demanded Skills', 0, 1)
    if os.path.exists(plot_skills_path):
        pdf.image(plot_skills_path, x=10, y=None, w=180)
    
    if not top_hiring_companies.empty:
        pdf.add_page()
        pdf.set_font('DejaVu', '', 14)
        pdf.cell(0, 10, 'Companies Hiring for Multiple Roles', 0, 1)
        pdf.set_font('DejaVu', '', 11)
        for company, count in top_hiring_companies.items():
            # <<< CHANGE 3: Also remove sanitization from company names >>>
            pdf.cell(0, 8, f"- {company}: {count} positions", 0, 1)

    pdf.output(pdf_report_path)
    print(f"PDF report generated successfully at {pdf_report_path}")
    
    return pdf_report_path