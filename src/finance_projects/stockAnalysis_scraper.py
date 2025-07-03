import os
import random

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
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Base URL
base_url = "https://stockanalysis.com/trending/"
# The page at https://stockanalysis.com/trending/ likely uses JavaScript to load the pagination element dynamically, which is common for modern web applications.


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



# List to store all table data
all_rows = []
headers = []


# Navigate to the base URL
driver.get(base_url)
time.sleep(2)  # Wait for initial page load

# Scrape the first page
page_count = 1

try:
    page_headers, page_rows = scrape_page()
except Exception as e:
    print(e)
    driver.quit()
    exit()
else:
    if page_headers and page_rows:
        headers = page_headers
        all_rows.extend(page_rows)
        print(f"{len(page_rows)} rows found on page: {page_count}, starting with {page_rows[0][1]}")

# Extract pagination information

# page info HTML element
# <span class="whitespace-nowrap"><span class="hidden sm:inline">Page</span> 1 of 110</span>
# Next page click HTML elemet:
# <button class="controls-btn xs:pl-1 xs:pr-1.5 bp:text-sm sm:pl-3 sm:pr-1"><span class="hidden sm:inline">Next</span> <svg class="-mb-px bp:ml-1" viewBox="0 0 20 20" fill="currentColor" style="max-width:40px" aria-hidden="true"><path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"></path></svg></button>
while True:
    page_count += 1

    ## Find the clickable "Next" element
    try:
        #next_button = WebDriverWait(driver, 10).until(
        #    EC.element_to_be_clickable((By.XPATH, '//span[@class="hidden sm:inline" and contains(text(), "Next")]'))
        #    )
        # If the hidden sm:inline classes change dynamically, consider using the data-svelte-h attribute for the "Next" button: Confirmed by Grok
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-svelte-h="svelte-1hxgo6f"]'))
            )
    except Exception as e:
        print(e)
        break
    
    if (not next_button.is_enabled()) or ("disabled" in next_button.get_attribute("class")):
        print("No more pages to scrape. Stopping.")
        break
     
    time.sleep(random.uniform(2, 4))  # Wait for the next page to load

    ## Click and Scrap
    # Attempt standard click
    try:
        next_button.click()
        print("Clicked the Next button (standard click).")
    except Exception:
        print("Standard click intercepted. Trying JavaScript click...")
            
        # Fallback to JavaScript click
        try:
            driver.execute_script("arguments[0].click();", next_button)
            print("Clicked the Next button (JavaScript click).")
            time.sleep(2)  # Wait for page to load after click
        except Exception as e:
            print(e)
            break
    finally:
        # Scrape the new page
        page_headers, page_rows = scrape_page()

        if page_rows:
            all_rows.extend(page_rows)
            print(f"{len(page_rows)} rows found on page: {page_count}, starting with {page_rows[0][1]}")

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


from selenium.common.exceptions import TimeoutException, NoSuchElementException
# Try to find the page number element
try:
        page_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[contains(text(), "Page ") and contains(text(), " of ")] | //span[contains(text(), "Page ") and contains(text(), " of ")]')
            )
        )
        page_text = page_element.text
        print(f"Found page element text: {page_text}")

        # Extract current and total page numbers
        page_info = page_text.split(" of ")
        current_page = int(page_info[0].replace("Page ", "").strip())
        total_pages = int(page_info[1].strip())
        print(f"Current Page: {current_page}")
        print(f"Total Pages: {total_pages}")

except TimeoutException:
        print("Timeout: Could not find page number element.")
        print("Current page source snippet:")
        print(driver.page_source[:1000])  # Print first 1000 characters
        try:
            # Fallback: Broader search for any element with " of "
            page_element = driver.find_element(By.XPATH, '//*[contains(text(), " of ")]')
            page_text = page_element.text
            print(f"Fallback found page element text: {page_text}")
            page_info = page_text.split(" of ")
            current_page = int(page_info[0].replace("Page ", "").strip())
            total_pages = int(page_info[1].strip())
            print(f"Current Page: {current_page}")
            print(f"Total Pages: {total_pages}")
        except (NoSuchElementException, ValueError):
            print("Fallback XPath also failed. Element not found or text format incorrect.")

    # Try to find and click the Next button
try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(), "Next")] | //span[contains(text(), "Next")]')
            )
        )
        next_button.click()
        print("Clicked the Next button.")
except TimeoutException:
        print("Timeout: Could not find or click the Next button.")





try:

    # Check for iframes
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    if iframes:
        print(f"Found {len(iframes)} iframe(s). Trying first iframe...")
        driver.switch_to.frame(iframes[0])

    # Try to find the page number element
    try:
        page_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[contains(text(), "Page ") and contains(text(), " of ")]')
            )
        )
        page_text = page_element.text
        print(f"Found page element text: '{page_text}'")

        # Extract current and total page numbers
        try:
            page_info = page_text.split(" of ")
            current_page = int(page_info[0].replace("Page ", "").strip())
            total_pages = int(page_info[1].strip())
            print(f"Current Page: {current_page}")
            print(f"Total Pages: {total_pages}")
        except (IndexError, ValueError) as e:
            print(f"Error parsing page text '{page_text}': {e}")

    except TimeoutException:
        print("Timeout: Could not find page number element.")
        print("Current page source snippet:")
        print(driver.page_source[:1000])
        try:
            # Fallback: Even broader search
            page_element = driver.find_element(By.XPATH, '//*[contains(text(), " of ")]')
            page_text = page_element.text
            print(f"Fallback found page element text: '{page_text}'")
            page_info = page_text.split(" of ")
            current_page = int(page_info[0].replace("Page ", "").strip())
            total_pages = int(page_info[1].strip())
            print(f"Current Page: {current_page}")
            print(f"Total Pages: {total_pages}")
        except (NoSuchElementException, ValueError) as e:
            print(f"Fallback failed: Element not found or text format incorrect. Error: {e}")

    # Switch back to main content if iframe was used
    if iframes:
        driver.switch_to.default_content()

    # Try to find and click the Next button
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//span[@data-svelte-h="svelte-1hxgo6f" and contains(text(), "Next")] | //button[contains(text(), "Next")] | //a[contains(text(), "Next")]')
            )
        )
        next_button.click()
        print("Clicked the Next button.")
        time.sleep(2)  # Wait for page to load after click
    except TimeoutException:
        print("Timeout: Could not find or click the Next button.")

finally:
    # Close the browser
    driver.quit()


try:
        # Wait for the page number element to be present
        page_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[@class="whitespace-nowrap" and contains(text(), " of ")]'))
        )

        # Extract the text (e.g., "Page 1 of 110")
        page_text = page_element.text

        # Split the text to get current and total page numbers
        # Assuming format is "Page X of Y" or "X of Y"
        page_info = page_text.split(" of ")
        current_page = int(page_info[0].replace("Page ", "").strip())
        total_pages = int(page_info[1].strip())

        # Print the results
        print(f"Current Page: {current_page} / {total_pages}")
except Exception as e:
        print(e)









# Try to find and click the Next button
try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//span[@data-svelte-h="svelte-1hxgo6f" and contains(text(), "Next")]')
            )
        )
        # Scroll to the button to ensure it's in view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
        time.sleep(0.5)  # Brief wait for scroll to settle

        # Attempt standard click
        try:
            next_button.click()
            print("Clicked the Next button (standard click).")
        except Exception:
            print("Standard click intercepted. Trying JavaScript click...")

            # Fallback to JavaScript click
            driver.execute_script("arguments[0].click();", next_button)
            print("Clicked the Next button (JavaScript click).")
        time.sleep(2)  # Wait for page to load after click

except TimeoutException:
        print("Timeout: Could not find the Next button.")
except Exception as e:
        print(f"Click intercepted even after scroll: {e}")
        # Check for overlay
        try:
            overlay = driver.find_element(By.XPATH, '//div[contains(@class, "px-5 py-6 xs:px-8 xs:py-8 md:px-28 md:py-20")]')
            print("Found potential overlay. Attempting to hide it...")
            driver.execute_script("arguments[0].style.display = 'none';", overlay)
            # Retry click
            next_button.click()
            print("Clicked the Next button after hiding overlay.")
            time.sleep(2)
        except NoSuchElementException:
            print("No overlay found or unable to hide it.")


"""