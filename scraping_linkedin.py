# Databricks notebook source
# MAGIC %pip install requests beautifulsoup4

# COMMAND ----------

# MAGIC %pip install selenium

# COMMAND ----------

from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Enter your credentials - the zone name and password
AUTH = 'brd-customer-hl_80709a30-zone-hadar_tomer_amit:i53s9wkm3hgu'

SBR_WEBDRIVER = f'https://{AUTH}@zproxy.lum-superproxy.io:9515'

# LinkedIn credentials
LINKEDIN_EMAIL = "your_email@example.com"  # Replace with your LinkedIn email
LINKEDIN_PASSWORD = "your_password"  # Replace with your LinkedIn password

# Target LinkedIn jobs URL
url = "https://www.linkedin.com/company/continental-resources-2/jobs/"

def main():
    print("Connecting to Scraping Browser...")
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
    options = ChromeOptions()
    options.add_argument("--headless")  # Run browser in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Connect to the remote browser
    with Remote(command_executor=sbr_connection, options=options) as driver:
        print("Connected! Navigating to LinkedIn login page...")
        
        # Open LinkedIn login page
        driver.get("https://www.linkedin.com/login")
        
        # Wait for the email input to be visible
        wait = WebDriverWait(driver, 10)
        
        try:
            email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#username")))  # Using CSS selector
            password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#password")))  # Using CSS selector

            # Enter email and password
            email_input.send_keys(LINKEDIN_EMAIL)
            password_input.send_keys(LINKEDIN_PASSWORD)
            password_input.send_keys(Keys.RETURN)

            # Wait for the login to complete
            time.sleep(5)

            # Navigate to the target jobs page
            print("Navigating to the target jobs page...")
            driver.get(url)
            time.sleep(5)  # Wait for the page to load

            # Take a screenshot for verification
            driver.get_screenshot_as_file('./linkedin_jobs_page.png')
            print("Screenshot saved as linkedin_jobs_page.png")

            # Extract the 'Recently Posted Jobs' section
            try:
                job_section = driver.find_element(By.CLASS_NAME, 'artdeco-carousel__slider')
                job_items = job_section.find_elements(By.CLASS_NAME, 'artdeco-carousel__item')
                
                for job in job_items:
                    # Extract job details (adjust based on actual LinkedIn structure)
                    job_title = job.find_element(By.TAG_NAME, 'h3').text.strip()
                    company_name = job.find_element(By.TAG_NAME, 'h4').text.strip()
                    print(f"Job Title: {job_title}, Company: {company_name}")
            except Exception as e:
                print(f"An error occurred while scraping job items: {e}")
        except Exception as e:
            print(f"An error occurred during login or page navigation: {e}")

        print("Finished scraping!")

if __name__ == "__main__":
    main()

# COMMAND ----------

from selenium.webdriver import Remote, ChromeOptions  
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection  
from selenium.webdriver.common.by import By  

# Enter your credentials - the zone name and password  
AUTH = 'brd-customer-hl_80709a30-zone-hadar_tomer_amit:i53s9wkm3hgu'  

SBR_WEBDRIVER = f'https://{AUTH}@zproxy.lum-superproxy.io:9515'  
  
def main():  
    print('Connecting to Scraping Browser...')  
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')  
    with Remote(sbr_connection, options=ChromeOptions()) as driver:  
        print('Connected! Navigating...')  
        driver.get('https://example.com')  # use this, or replace with URL of your choice
        print('Taking page screenshot to file page.png')  
        driver.get_screenshot_as_file('./page.png')  
        print('Navigated! Scraping page content...')  
        html = driver.page_source  
        print(html)  
  
if __name__ == '__main__':  
   main()

# COMMAND ----------

import requests
from bs4 import BeautifulSoup

# Set your headers and cookies
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )
}

# Replace this with your actual `li_at` cookie from LinkedIn after logging in
COOKIES = {
    "li_at": "your_li_at_cookie_value",  # Replace with your session cookie value
}

# Target URL (LinkedIn jobs page or company jobs URL)
url = "https://www.linkedin.com/company/continental-resources-2/jobs/"

try:
    # Fetch the page
    response = requests.get(url, headers=HEADERS, cookies=COOKIES, allow_redirects=True, timeout=10)
    
    # Raise an exception for HTTP errors
    response.raise_for_status()

    # Print final URL after redirects
    print(f"Final URL: {response.url}")
    print(f"HTTP Status Code: {response.status_code}")

    # Check if the content is successfully retrieved
    if response.status_code == 200:
        # Parse the page content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate the "Recently Posted Jobs" section by its unique class or ID
        job_section = soup.find('ul', {'class': 'artdeco-carousel__slider'})
        if job_section:
            # Extract job items
            job_items = job_section.find_all('li', {'class': 'artdeco-carousel__item'})
            for job in job_items:
                # Extract specific job details (adjust based on actual LinkedIn structure)
                job_title = job.find('h3')  # Replace 'h3' with the actual HTML tag for job title
                company_name = job.find('h4')  # Replace 'h4' with the actual HTML tag for company name
                if job_title and company_name:
                    print(f"Job Title: {job_title.text.strip()}, Company: {company_name.text.strip()}")
        else:
            print("Could not find the 'Recently Posted Jobs' section.")
    else:
        print(f"Failed to fetch the content. HTTP Status: {response.status_code}")

except requests.TooManyRedirects:
    print("Error: Too many redirects. Check the URL or your cookies.")
except requests.RequestException as e:
    print(f"An error occurred: {e}")

# COMMAND ----------

import requests
from bs4 import BeautifulSoup

# Define headers and cookies for authentication
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Replace these with your actual cookies
COOKIES = {
    "li_at": "your_li_at_cookie_value",  # Replace with your LinkedIn session cookie
}

# LinkedIn jobs URL (adjust as needed)
url = "https://www.linkedin.com/company/continental-resources-2/jobs/"

# Make the request with allow_redirects set to False
response = requests.get(url, headers=HEADERS, cookies=COOKIES, allow_redirects=False)

# Check response status
if response.status_code == 200:
    # Parse HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the 'Recently Posted Jobs' section
    job_section = soup.find('ul', {'class': 'artdeco-carousel__slider'})
    if job_section:
        job_items = job_section.find_all('li', {'class': 'artdeco-carousel__item'})
        for job in job_items:
            # Extract job details
            job_title = job.find('h3')  # Adjust based on the actual tag structure
            company_name = job.find('h4')  # Adjust as needed
            if job_title and company_name:
                print(f"Job Title: {job_title.text.strip()}, Company: {company_name.text.strip()}")
    else:
        print("Could not find 'Recently Posted Jobs' section.")
else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")
    if response.status_code in [301, 302]:
        print(f"Redirected to: {response.headers['Location']}")

# COMMAND ----------

# DBTITLE 1,Amit and Claude
import requests
from linkedin import linkedin
import os
from datetime import datetime

def setup_linkedin_client():
    """
    Initialize LinkedIn API client with OAuth 2.0
    """
    # Your LinkedIn API credentials
    CLIENT_ID = "YOUR_CLIENT_ID"
    CLIENT_SECRET = "YOUR_CLIENT_SECRET"
    RETURN_URL = "http://localhost:8000/callback"
    
    authentication = linkedin.LinkedInAuthentication(
        CLIENT_ID,
        CLIENT_SECRET,
        RETURN_URL,
        linkedin.PERMISSIONS.enums.values()
    )
    
    return authentication

def get_company_jobs(company_id, limit=10):
    """
    Get jobs for a specific company using LinkedIn's Jobs API
    """
    BASE_URL = "https://api.linkedin.com/v2"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    
    params = {
        'companyId': company_id,
        'count': limit
    }
    
    endpoint = f"{BASE_URL}/jobs"
    response = requests.get(endpoint, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")

def process_jobs_data(jobs_data):
    """
    Process and format the jobs data returned from LinkedIn
    """
    processed_jobs = []
    
    for job in jobs_data.get('elements', []):
        processed_job = {
            'id': job.get('id'),
            'title': job.get('title', {}).get('text', ''),
            'company_name': job.get('companyName', ''),
            'location': job.get('locationName', ''),
            'description': job.get('description', {}).get('text', ''),
            'posted_date': job.get('postedDate', ''),
            'application_url': job.get('applicationUrl', ''),
            'employment_type': job.get('employmentType', {}).get('name', ''),
        }
        processed_jobs.append(processed_job)
    
    return processed_jobs

def save_jobs_to_file(jobs, filename):
    """
    Save processed jobs data to a JSON file
    """
    import json
    from datetime import datetime
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{filename}_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(jobs, f, indent=2)
    
    return filename

def main():
    try:
        # Initialize LinkedIn client
        auth = setup_linkedin_client()
        
        # Get authorization URL
        print("Please visit this URL to authorize the application:")
        print(auth.authorization_url)
        
        # After authorization, get the access token
        auth.authorization_code = input("Enter the authorization code: ")
        access_token = auth.get_access_token()
        
        # Set the company ID for Continental Resources
        COMPANY_ID = "continental-resources-2"  # This should be the actual LinkedIn company ID
        
        # Get jobs data
        jobs_data = get_company_jobs(COMPANY_ID)
        
        # Process the jobs data
        processed_jobs = process_jobs_data(jobs_data)
        
        # Save to file
        output_file = save_jobs_to_file(processed_jobs, "continental_jobs")
        
        print(f"Successfully retrieved and saved {len(processed_jobs)} jobs to {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
