# # scraper_logic.py

# import time
# from datetime import datetime
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup

# def _parse_single_job(job_html):
#     """Helper function to parse one job <tr> element. Not exported."""
#     if not job_html.has_attr('data-slug'):
#         return None
#     try:
#         title_tag = job_html.find('h2', itemprop='title')
#         job_title = title_tag.text.strip() if title_tag else "N/A"

#         company_tag = job_html.find('h3', itemprop='name')
#         company = company_tag.text.strip() if company_tag else "N/A"

#         date_posted = datetime.fromtimestamp(int(job_html['data-epoch'])) if job_html.has_attr('data-epoch') else None

#         location_tags = job_html.find_all('div', class_='location')
#         location = "No Location"
#         for loc in location_tags:
#             if '💰' not in loc.get_text(strip=True):
#                 location = loc.get_text(strip=True)
#                 break
        
#         tags_container = job_html.find('td', class_='tags')
#         tags = [tag.text.strip() for tag in tags_container.find_all('h3')] if tags_container else []

#         if job_title == "N/A" or company == "N/A":
#             return None
            
#         return {'job_title': job_title, 'company': company, 'location': location, 'date_posted': date_posted, 'tags': tags}
#     except Exception:
#         return None

# def run_scraper(url):
#     """
#     Takes a URL, scrapes all job listings by handling infinite scroll,
#     and returns a pandas DataFrame with the raw data.
#     """
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")
#     options.add_argument("--log-level=3")
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=options)
    
#     all_jobs_data = []
#     print(f"Fetching job listings from {url}...")
    
#     try:
#         driver.get(url)
#         WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr[data-slug]")))
#         print("Initial page content loaded.")

#         last_height = driver.execute_script("return document.body.scrollHeight")
#         print("Scrolling down to load all job listings...")
#         while True:
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(2)
#             new_height = driver.execute_script("return document.body.scrollHeight")
#             if new_height == last_height:
#                 print("Reached the bottom of the page. All jobs loaded.")
#                 break
#             last_height = new_height

#         page_source = driver.page_source
#         soup = BeautifulSoup(page_source, 'lxml')
#         job_listings = soup.select('tr.job')
#         print(f"Found {len(job_listings)} potential job rows on the fully loaded page.")

#         for job_html in job_listings:
#             job_info = _parse_single_job(job_html)
#             if job_info:
#                 all_jobs_data.append(job_info)
        
#         print(f"Successfully parsed {len(all_jobs_data)} jobs.")
        
#         if not all_jobs_data:
#             return pd.DataFrame() # Return empty DataFrame if no jobs found

#         return pd.DataFrame(all_jobs_data)

#     except Exception as e:
#         print(f"An error occurred during scraping: {e}")
#         return None # Return None to indicate failure
#     finally:
#         driver.quit()
#         print("Browser closed.")

# scraper_logic.py (Updated for Stability and Better Error Handling)

import time
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# <<< CHANGE 1: Import Selenium's TimeoutException for better error handling >>>
from selenium.common.exceptions import TimeoutException

def _parse_single_job(job_html):
    # This helper function is fine and doesn't need changes.
    if not job_html.has_attr('data-slug'):
        return None
    try:
        title_tag = job_html.find('h2', itemprop='title')
        job_title = title_tag.text.strip() if title_tag else "N/A"
        company_tag = job_html.find('h3', itemprop='name')
        company = company_tag.text.strip() if company_tag else "N/A"
        date_posted = datetime.fromtimestamp(int(job_html['data-epoch'])) if job_html.has_attr('data-epoch') else None
        location_tags = job_html.find_all('div', class_='location')
        location = "No Location"
        for loc in location_tags:
            if '💰' not in loc.get_text(strip=True):
                location = loc.get_text(strip=True)
                break
        tags_container = job_html.find('td', class_='tags')
        tags = [tag.text.strip() for tag in tags_container.find_all('h3')] if tags_container else []
        if job_title == "N/A" or company == "N/A": return None
        return {'job_title': job_title, 'company': company, 'location': location, 'date_posted': date_posted, 'tags': tags}
    except Exception:
        return None

def run_scraper(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    
    # <<< CHANGE 2: Add browser options known to improve stability >>>
    options.add_argument("--no-sandbox") # Bypass OS security model, required for some environments
    options.add_argument("--disable-dev-shm-usage") # Overcome limited resource problems
    options.add_argument("--disable-gpu") # Applicable to windows os only
    options.add_argument("start-maximized") # Open browser in maximized mode
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    all_jobs_data = []
    print(f"Fetching job listings from {url}...")
    
    try:
        driver.get(url)
        # <<< CHANGE 3: Increase wait time slightly for slower pages >>>
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr[data-slug]")))
        print("Initial page content loaded.")

        last_height = driver.execute_script("return document.body.scrollHeight")
        print("Scrolling down to load all job listings...")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("Reached the bottom of the page. All jobs loaded.")
                break
            last_height = new_height

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        job_listings = soup.select('tr.job')
        print(f"Found {len(job_listings)} potential job rows on the fully loaded page.")

        for job_html in job_listings:
            job_info = _parse_single_job(job_html)
            if job_info:
                all_jobs_data.append(job_info)
        
        print(f"Successfully parsed {len(all_jobs_data)} jobs.")
        
        if not all_jobs_data:
            return pd.DataFrame()

        return pd.DataFrame(all_jobs_data)

    # <<< CHANGE 4: Add specific error handling for timeouts >>>
    except TimeoutException:
        print(f"Error: Timed out waiting for job listings to load on {url}.")
        print("This could mean the page has no jobs or the structure has changed.")
        return None # Return None to indicate failure
    except Exception as e:
        print(f"An unexpected error occurred during scraping: {e}")
        return None
    finally:
        driver.quit()
        print("Browser closed.")