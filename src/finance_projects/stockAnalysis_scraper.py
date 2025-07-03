import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

import logging
# logging.basicConfig(level=logging.DEBUG)

# Set up Chrome options
options = Options()
options.add_argument("--headless=new")  # New headless mode
options.add_argument("--no-sandbox")  # Required for Linux
options.add_argument("--disable-dev-shm-usage")  # Avoid shared memory issues
options.add_argument("--disable-gpu")  # Disable GPU
options.add_argument("--remote-debugging-port=9222")  # Avoid port conflicts
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Specify ChromeDriver path (replace with actual path or use ChromeDriverManager)
# Example manual path: "/usr/local/bin/chromedriver"
# Using ChromeDriverManager for automatic download
chromedriver_path = ChromeDriverManager().install()  # Automatically downloads correct version
# If manual path is needed, uncomment and set:
# chromedriver_path = "/path/to/chromedriver"  # e.g., "/usr/local/bin/chromedriver"

# Verify ChromeDriver exists
if not os.path.exists(chromedriver_path):
    print(f"ChromeDriver not found at {chromedriver_path}")
    exit()

# Initialize WebDriver with Service
try:
    service = Service(executable_path=chromedriver_path, port=9516)
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)
except Exception as e:
    print(f"Error initializing ChromeDriver: {e}")
    exit()


# Base URL
base_url = "https://stockanalysis.com/trending/"

# List to store all table data
all_rows = []
headers = []


def scrape_page():
    """"
    Function to scrape a single page with a single table
    Example:
    base_url = "https://stockanalysis.com/ipos/"
    driver.get(base_url)
    tb_headers, tb_rows = scrape_page()
    df = pd.DataFrame(tb_rows, columns=tb_headers)
    """
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    # Get page source after JavaScript rendering
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Find the table
    table = soup.find("table")

    if not table:
        print("No table found on the current page")
        return None, None
    
    # Extract headers (only on the first page)
    page_headers = [th.text.strip() for th in table.find_all("th")]
    
    # Extract rows
    page_rows = []
    for tr in table.find_all("tr")[1:]:  # Skip header row
        cells = [td.text.strip() for td in tr.find_all("td")]
        if cells:  # Only append non-empty rows
            page_rows.append(cells)
    
    return page_headers, page_rows


# 
def scrape_page_mtb():
    """
    Function to scrape a single page with more than one table, all have the same columns/fields.

    Example:
    # Get schedule IPO stocks in two weeks 
    base_url = "https://stockanalysis.com/ipos/calendar/"
    driver.get(base_url)
    tb_headers, tb_rows = scrape_page_mtb()
    df = pd.DataFrame(tb_rows, columns=tb_headers)
"""
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    # Get page source after JavaScript rendering
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Find all tables
    tables = soup.find_all('table')
    if not tables:
        print("No tables found on the page.")
        exit()
    
    # Function to extract headers from a table
    def get_table_headers(table):
        headers = []
        header_row = table.find('tr')  # Assume first row contains headers
        if header_row:
            headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
        return headers

    # Function to extract table data as a list of lists
    def get_table_data(table):
        data = []
        rows = table.find_all('tr')[1:]  # Skip header row
        for row in rows:
            cells = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
            if cells:  # Only add non-empty rows
                data.append(cells)
        return data


    # Get headers of the first table as reference
    reference_headers = get_table_headers(tables[0]) if tables else []
    if not reference_headers:
        print("No headers found in the first table.")
        exit()

    # Collect data from tables with matching headers
    all_data = []
    for table in tables:
        headers = get_table_headers(table)
        if headers == reference_headers:  # Check if headers match
            table_data = get_table_data(table)
            all_data.extend(table_data)
        else:
            print(f"Table skipped due to mismatched headers: {headers}")
    
    return reference_headers, all_data



# Navigate to the base URL
driver.get(base_url)
time.sleep(2)  # Wait for initial page load

# Scrape the first page
page_headers, page_rows = scrape_page()
if page_headers:
    headers = page_headers
    all_rows.extend(page_rows)
else:
    print("Failed to scrape the first page. Exiting.")
    driver.quit()
    exit()

# Loop through pages by clicking the "Next" button
page_count = 1


while True:
     try:
         # Find the "Next" button: Right click > Elements >
         # <span class="hidden sm:inline" data-svelte-h="svelte-1hxgo6f">Next</span>
         next_button = driver.find_element(By.XPATH, "//span[@class='hidden sm:inline' and text()='Next']")
     except Exception as e:
         print(e)
         break
     if (not next_button.is_enabled()) or ("disabled" in next_button.get_attribute("class")):
         print("No more pages to scrape. Stopping.")
         break
     try:    
         # Click the "Next" button
         next_button.click()
         time.sleep(random.uniform(2, 4))  # Wait for the next page to load
         page_count += 1
         print(f"Scraping page {page_count}")
         # Scrape the new page
         page_headers, page_rows = scrape_page()
         if page_rows:
             all_rows.extend(page_rows)
         else:
             print("No data found on this page. Stopping.")
             break
     except Exception as e:
         print(f"No more pages or Error occurred: {e}")
         break


# Close the driver
driver.quit()

# Create a DataFrame
df = pd.DataFrame(all_rows, columns=headers)

# Save to CSV
df.to_csv("stock_gainers_all_pages.csv", index=False)
print(f"Scraped {page_count} pages and saved as stock_gainers_all_pages.csv")





"""
https://finnhub.io/docs/api/library
https://github.com/darkshloser/stockanalysis-scraper/tree/master


soup = BeautifulSoup(driver.page_source, "html.parser")
# Find the table
table = soup.find("table")
# Find all the tables
tables = soup.find_all('table')
print(table.prettify())  # Pretty-print the table HTML


import finnhub
import json
import pandas as pd
import sys

# Setup client
finnhub_client = finnhub.Client(api_key="...")
"""