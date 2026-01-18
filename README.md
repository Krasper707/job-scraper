# Remote Job Market Analyzer & Reporter

![Project Status](https://img.shields.io/badge/status-complete-brightgreen)![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)![Framework](https://img.shields.io/badge/framework-Flask-black.svg)

An interactive web application that performs on-demand scraping of live job listings from RemoteOK, cleans and stores the data, and generates a comprehensive PDF hiring report with AI-powered trend analysis.

## Key Features

- **On-Demand Dynamic Scraping**: Utilizes Selenium to control a headless browser, handling JavaScript-driven content and infinite scrolling to capture all job listings for a selected category.
- **Interactive Web Interface**: A clean frontend built with Flask and HTML/CSS allows any user to initiate a report for various job categories.
- **AI-Powered Summaries**: Integrates with OpenRouter to leverage powerful LLMs (like Mistral 7B) that generate a natural language "Executive Summary" of the hiring trends.
- **Automated Data Pipeline**: A complete, end-to-end pipeline that scrapes, cleans (using Pandas), and stores data (in SQLite) with a single click.
- **Professional PDF Reporting**: Generates a multi-page PDF report containing AI summaries, Matplotlib/Seaborn visualizations of top skills, and lists of top hiring companies.

## Why This Project is Valuable

This project isn't just a script; it's a full-fledged data application that proves a wide range of job-ready skills. It demonstrates the ability to:

- **Pull Live Data**: Overcome modern web scraping challenges like dynamic content and browser automation.
- **Deal with Messiness**: Clean, validate, normalize, and structure raw, inconsistent web data.
- **Automate a Recurring Task**: Build an on-demand system that abstracts away a complex, multi-step process.
- **Deliver Something Useful**: Produce a tangible, professional, and insightful report that non-technical users can understand.
- **Integrate Modern AI**: Enhance a data product with generative AI to provide qualitative insights.

## System Architecture

The application follows a modular, sequential data flow, orchestrated by the Flask backend.

```mermaid
graph TD
    A[User] -->|Selects Job Category| B(Flask Web UI);
    B -->|POST Request| C{Flask Backend (app.py)};
    C -->|Runs Pipeline| D(Scraper Logic);
    D -->|Fetches HTML| E[RemoteOK Website];
    D -->|Raw DataFrame| F(Cleaner Logic);
    F -->|Cleaned DataFrame| G(Database Logic);
    G -->|Stores Data| H[(SQLite Database)];
    C -->|Generates Report| I(Reporter Logic);
    I -->|Queries Data| H;
    I -->|Sends Data for Summary| J{OpenRouter LLM API};
    J -->|Returns Summary| I;
    I -->|Generates PDF| K([PDF Report]);
    C -->|Sends File for Download| A;
```

## Tech Stack

- **Backend**: Python, Flask
- **Web Scraping**: Selenium, BeautifulSoup4
- **Data Manipulation**: Pandas
- **Database**: SQLite
- **AI Integration**: OpenRouter API, OpenAI Python Client
- **PDF Generation**: FPDF2
- **Data Visualization**: Matplotlib, Seaborn

## Setup and Installation

Follow these steps to get the application running locally.

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/Krasper707/job-scraper.git
    cd job-scraper
    ```

2.  **Create and Activate a Virtual Environment**

    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    _(It is best practice to create a `requirements.txt` file by running `pip freeze > requirements.txt` and then users can install with `pip install -r requirements.txt`. For now, installing manually is fine.)_

    ```bash
    pip install flask selenium beautifulsoup4 pandas matplotlib seaborn fpdf2 openai webdriver-manager
    ```

4.  **Set Up Your API Key**
    - Get a free API key from [OpenRouter.ai](https://openrouter.ai/).
    - Open the `reporter_logic.py` file.
    - Find the line `OPENROUTER_API_KEY = "sk-or-v1-YOUR_OPENROUTER_API_KEY_HERE"` and paste your key.
    - **Warning:** Do not commit your API key to a public GitHub repository.

5.  **Run the Application**
    ```bash
    python app.py
    ```

## How to Use

1.  Once the server is running, open your web browser and navigate to `http://127.0.0.1:5000`.
2.  Select a job category from the dropdown menu.
3.  Click the "Generate Report" button.
4.  Wait for the process to complete (it can take 30-60 seconds). Your browser will automatically prompt you to download the finished PDF report.

## Future Improvements

- [ ] **Historical Dashboard**: Create a new page to visualize trends over time by querying the historical data in the SQLite database.
- [ ] **Add More Job Sites**: Abstract the scraper logic further to allow for multiple data sources (e.g., LinkedIn, Indeed).
- [ ] **Asynchronous Task Queue**: For long-running scrapes, implement a task queue like Celery or Redis Queue so the user doesn't have to wait for the download.
- [ ] **User Accounts**: Allow users to save their generated reports.
