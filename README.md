
# Remote Job Market Analyzer & Reporter

![Status](https://img.shields.io/badge/Status-Maintained-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-black?style=for-the-badge&logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Turn chaotic job boards into actionable intelligence.**

A full-stack data application that performs on-demand scraping of live RemoteOK listings, utilizes LLMs to generate executive summaries, and compiles everything into a professional PDF report.

---

## ⚡ Key Features

| Feature | Description |
| :--- | :--- |
| **🤖 Dynamic Scraping** | Uses **Selenium** to navigate headless browsers, handling infinite scrolls and JavaScript rendering to capture 100% of available listings. |
| **🧠 AI-Powered Insights** | Integrates with **OpenRouter/Mistral 7B** to read raw job descriptions and generate a human-readable "Executive Summary" of market trends. |
| **📊 Auto-Visualization** | Automatically cleans data with **Pandas** and generates distribution charts for salaries and top skills using **Matplotlib/Seaborn**. |
| **📄 PDF Generation** | Compiles charts, summaries, and top company lists into a downloadable, professionally formatted PDF report. |
| **💾 SQL Persistence** | Stores every scrape in a **SQLite** database for historical tracking and future analysis. |

---

## 🏗️ System Architecture

The application follows a sequential ETL (Extract, Transform, Load) pipeline triggered via a web frontend.
[![](https://mermaid.ink/img/pako:eNp1U11v2jAU_SuWnzaJIkhIgDxMArJ21UBlkG7SQh8u5DZYc-zIcdQC4b_v5qOaNnWRYvv6nnM_ju0LP-gEecBTA_mRReFOMfoeCzRxPTyxm5tP1RYlHmzBFmAx1eZUscf7-FZC8Yv9wD0ZTx3tvoFHRqQpmqJiszy_rEAottDKGi0lmmsLbcei3LeJd_xztGRrkaMUCne8dRO9CTjss-2BcFh1s4nrkpQoMzbXtsveuRrGHVr2JVotq7rAeIOZtvjw9R3gBl5YCBYqtpAIiiKvQSVQtKZQacfpvK0c1pQHWxpMOmo4jz9svy2FxWZjDwV-7Hiokv80vMFcG0sZ_u3W6bOZAnk6U7vL5Sp-yFFtdGkp-2z9JnU4b7C1rvhquzoI3Xpp0VZaZhmYE4sIU7F1eBvTz-6QOgGrzd-xthYsndl3cY5XYHOprRT7DkKbbb4jmBpEYd7trw5f40L9oqSGpGquEu_R_RIJD0g47PEMTQa1yS81a8ftETM69ICWCT5DKW2tyZVoOaifWmdvTKPL9MiDZ5AFWWWe0IUMBZCkfyBUEZqFLpXlgTtsQvDgwl954Eycvj_03ZHrjceO509HPX7igd93XdcZea7ne87Ucd1rj5-bpIP-ZOAOpmPfG_vOwJsM_B7HRJByq_bVNI_n-hv1mwjr?type=png)](https://mermaid.live/edit#pako:eNp1U11v2jAU_SuWnzaJIkhIgDxMArJ21UBlkG7SQh8u5DZYc-zIcdQC4b_v5qOaNnWRYvv6nnM_ju0LP-gEecBTA_mRReFOMfoeCzRxPTyxm5tP1RYlHmzBFmAx1eZUscf7-FZC8Yv9wD0ZTx3tvoFHRqQpmqJiszy_rEAottDKGi0lmmsLbcei3LeJd_xztGRrkaMUCne8dRO9CTjss-2BcFh1s4nrkpQoMzbXtsveuRrGHVr2JVotq7rAeIOZtvjw9R3gBl5YCBYqtpAIiiKvQSVQtKZQacfpvK0c1pQHWxpMOmo4jz9svy2FxWZjDwV-7Hiokv80vMFcG0sZ_u3W6bOZAnk6U7vL5Sp-yFFtdGkp-2z9JnU4b7C1rvhquzoI3Xpp0VZaZhmYE4sIU7F1eBvTz-6QOgGrzd-xthYsndl3cY5XYHOprRT7DkKbbb4jmBpEYd7trw5f40L9oqSGpGquEu_R_RIJD0g47PEMTQa1yS81a8ftETM69ICWCT5DKW2tyZVoOaifWmdvTKPL9MiDZ5AFWWWe0IUMBZCkfyBUEZqFLpXlgTtsQvDgwl954Eycvj_03ZHrjceO509HPX7igd93XdcZea7ne87Ucd1rj5-bpIP-ZOAOpmPfG_vOwJsM_B7HRJByq_bVNI_n-hv1mwjr)


---

## 📂 Project Structure

```text
job-scraper/
├── app.py                 # Flask entry point and route handlers
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API Keys)
├── database/
│   └── jobs.db            # SQLite database (auto-created)
├── static/
│   ├── css/               # Stylesheets
│   └── reports/           # Generated PDFs reside here
├── templates/
│   └── index.html         # Frontend interface
└── utils/
    ├── scraper.py         # Selenium logic
    ├── cleaner.py         # Pandas data cleaning
    ├── db_manager.py      # Database interactions
    └── reporter.py        # PDF generation & AI integration
```

---

## 🚀 Setup and Installation

### Prerequisites
*   Python 3.9+
*   Google Chrome (installed on the host machine)

### 1. Clone the Repository
```bash
git clone https://github.com/Krasper707/job-scraper.git
cd job-scraper
```

### 2. Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*(If `requirements.txt` is missing, install manually: `pip install flask selenium beautifulsoup4 pandas matplotlib seaborn fpdf2 openai python-dotenv webdriver-manager`)*

### 4. Configuration (Security)
Create a file named `.env` in the root directory. Add your OpenRouter API key here. **Never commit this file to GitHub.**

```ini
# .env file
OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY_HERE
```

### 5. Run the Application
```bash
python app.py
```
Access the application at `http://127.0.0.1:5000`.

---

## 🛠️ Troubleshooting

**Issue: `ChromeDriver` version mismatch**
*   **Fix:** This project uses `webdriver-manager` to handle this automatically. If it fails, try running `pip install --upgrade webdriver-manager`.

**Issue: Infinite Scroll not working / 0 Jobs found**
*   **Fix:** RemoteOK changes their DOM structure frequently. Check `scraper.py` and ensure the CSS Selectors match the current website structure.

**Issue: PDF generation fails**
*   **Fix:** Ensure the `static/reports` directory exists. The script should create it, but permissions can sometimes block write access.

---

## 🔮 Future Roadmap

*   [ ] **Dashboard:** Replace static PDF with a live React/Plotly dashboard.
*   [ ] **Multi-Source:** Add adapters for LinkedIn and Indeed.
*   [ ] **Celery/Redis:** Move scraping to a background worker to prevent browser timeouts during long scrapes.
*   [ ] **Email Alerts:** Schedule weekly scrapes and email the PDF automatically.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue first to discuss the change you wish to make.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
