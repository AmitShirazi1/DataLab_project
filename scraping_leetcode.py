# Databricks notebook source
import requests
import pandas as pd
import json
import time
from datetime import datetime

## checking on 1 problem with solution_URL
def fetch_leetcode_problems():
    # Convert question names to slugs
    # question_names = question_names_df['name'].tolist()
    # title_slugs = [name.replace(" ", "-").lower() for name in question_names]  # Lowercase to match LeetCode URL format
    title_slugs = ["Two-Sum"]
    
    # Define headers
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'application/json',
    }

    # GraphQL query
    graphql_query = """
    query getQuestion($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
            title
            content
            difficulty
            likes
            dislikes
        }
    }
    """

    # List to store all problem data
    all_problems_data = []

    # Loop through the titleSlugs and fetch data
    for title_slug in title_slugs:
        variables = {"titleSlug": title_slug}
        
        try:
            # Send request to LeetCode GraphQL endpoint
            response = requests.post(
                "https://leetcode.com/graphql/",
                json={"query": graphql_query, "variables": variables},
                headers=headers
            )
            
            if response.status_code == 200:
                question_data = response.json()
                if 'data' in question_data and 'question' in question_data['data']:
                    problem = question_data['data']['question']
                    
                    # Generate the solution URL
                    solution_url = f"https://leetcode.com/problems/{title_slug}/solutions/"
                    
                    # Append problem data
                    all_problems_data.append({
                        'question_id': problem['questionId'],
                        'title': problem['title'],
                        'content': problem['content'],
                        'difficulty': problem['difficulty'],
                        'likes': problem['likes'],
                        'dislikes': problem['dislikes'],
                        'slug': title_slug,
                        'solution_URL': solution_url  # Add solution URL
                    })
                    print(f"Successfully fetched data for: {title_slug}")
                else:
                    print(f"Invalid response format for {title_slug}")
            else:
                print(f"Failed to fetch data for {title_slug}: {response.status_code}")
                
            # Add a small delay to avoid rate limiting
            time.sleep(1)
            
        except Exception as e:
            print(f"Error processing {title_slug}: {str(e)}")
            continue

    # Create DataFrame from collected data
    problems_df = pd.DataFrame(all_problems_data)
    
    # Generate timestamp for filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save to CSV
    csv_filename = f'leetcode_problems_data_{timestamp}.csv'
    problems_df.to_csv(csv_filename, index=False, encoding='utf-8')
    
    # Save raw data to JSON (for backup)
    json_filename = f'leetcode_problems_raw_{timestamp}.json'
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(all_problems_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nData saved to {csv_filename} and {json_filename}")
    return problems_df

# Usage
if __name__ == "__main__":
    # question_names_df = pd.read_csv('leetcode_problems.csv')
    # problems_df = fetch_leetcode_problems(question_names_df)
    problems_df = fetch_leetcode_problems()


# COMMAND ----------

import pandas as pd

question_names_df = pd.read_csv('leetcode_problems.csv')
question_names = question_names_df['name'].tolist()
len(question_names)
question_names = [name.replace(" ", "-") for name in question_names]
question_names

# COMMAND ----------

import requests
import pandas as pd
import json
import time
from datetime import datetime

## checking on all problems with no solution_URL

def fetch_leetcode_problems(question_names_df):
    # Convert question names to slugs
    question_names = question_names_df['name'].tolist()
    title_slugs = [name.replace(" ", "-") for name in question_names]

    # Define headers
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'application/json',
    }

    # GraphQL query
    graphql_query = """
    query getQuestion($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
            title
            content
            difficulty
            likes
            dislikes
        }
    }
    """

    # List to store all problem data
    all_problems_data = []

    # Loop through the titleSlugs and fetch data
    for title_slug in title_slugs:
        variables = {"titleSlug": title_slug}
        
        try:
            # Send request to LeetCode GraphQL endpoint
            response = requests.post(
                "https://leetcode.com/graphql/",
                json={"query": graphql_query, "variables": variables},
                headers=headers
            )
            
            if response.status_code == 200:
                question_data = response.json()
                if 'data' in question_data and 'question' in question_data['data']:
                    problem = question_data['data']['question']
                    all_problems_data.append({
                        'question_id': problem['questionId'],
                        'title': problem['title'],
                        'content': problem['content'],
                        'difficulty': problem['difficulty'],
                        'likes': problem['likes'],
                        'dislikes': problem['dislikes'],
                        'slug': title_slug
                    })
                    print(f"Successfully fetched data for: {title_slug}")
                else:
                    print(f"Invalid response format for {title_slug}")
            else:
                print(f"Failed to fetch data for {title_slug}: {response.status_code}")
                
            # Add a small delay to avoid rate limiting
            time.sleep(1)
            
        except Exception as e:
            print(f"Error processing {title_slug}: {str(e)}")
            continue

    # Create DataFrame from collected data
    problems_df = pd.DataFrame(all_problems_data)
    
    # Generate timestamp for filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save to CSV
    csv_filename = f'leetcode_problems_data_{timestamp}.csv'
    problems_df.to_csv(csv_filename, index=False, encoding='utf-8')
    
    # Save raw data to JSON (for backup)
    json_filename = f'leetcode_problems_raw_{timestamp}.json'
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(all_problems_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nData saved to {csv_filename} and {json_filename}")
    return problems_df

# Usage
if __name__ == "__main__":
    question_names_df = pd.read_csv('/Workspace/Users/amit.shirazi@campus.technion.ac.il/project/data/questions_and_answers/leetcode_problems_data.csv')
    problems_df = fetch_leetcode_problems(question_names_df)

# COMMAND ----------



# COMMAND ----------

import time
import json
import logging
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

# Configure logging
logging.basicConfig(filename='scraping.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Enter your credentials - the zone name and password
AUTH = 'brd-customer-hl_80709a30-zone-hadar_tomer_amit:i53s9wkm3hgu'

SBR_WEBDRIVER = f'https://{AUTH}@zproxy.lum-superproxy.io:9515'

def safe_find_elements(driver, by, value, retries=3):
    """
    Attempts to find multiple elements up to a certain number of retries to avoid stale element reference.
    """
    while retries > 0:
        try:
            elements = driver.find_elements(by, value)
            return elements
        except StaleElementReferenceException:
            retries -= 1
            if retries == 0:
                print(f"Failed to find elements after multiple retries: {value}")
                return []
            print(f"Retrying to find elements: {value}")

def scrape_leetcode(driver):
    logging.info("Starting to scrape LeetCode questions and topics...")
    
    # Navigate to the problems page
    driver.get('https://leetcode.com/problemset/all/')
    time.sleep(1)  # Add delay between page requests

    # Wait for the questions to load
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="rowgroup"]'))
        )
    except Exception as e:
        logging.error("Error: Problems table did not load.")
        logging.error(driver.page_source)  # Debugging: Log the HTML of the page
        raise e

    questions = []
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Infinite scrolling to load all questions
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    while True:
        # Locate the question table
        question_rows = driver.find_elements(By.CSS_SELECTOR, 'div[role="rowgroup"] div[role="row"]')
        if not question_rows:
            logging.warning("No question rows found. The layout may have changed.")
            break
        
        for row in question_rows:
            # Use safe_find_elements to avoid stale element issues and get all columns
            cols = safe_find_elements(driver, By.CSS_SELECTOR, 'div[role="cell"]')

            if cols and len(cols) >= 2:  # Ensure there are enough columns
                try:
                    question_title = cols[1].text.strip()
                    question_url = cols[1].find_element(By.TAG_NAME, 'a').get_attribute('href')
                    question_difficulty = cols[-1].text.strip()

                    # Navigate to the question's description page
                    driver.get(f"{question_url}/description/")
                    time.sleep(1)  # Add delay between page requests

                except Exception as e:
                    print(f"Error extracting data for a row: {e}")
                    continue

                try:
                    # Wait for the question description content to load
                    WebDriverWait(driver, 60).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'description__24sA'))
                    )

                    # Retry mechanism for stale elements
                    retries = 3
                    while retries > 0:
                        try:
                            # Extract the question content
                            question_content = driver.find_element(By.CLASS_NAME, 'description__24sA').text.strip()

                            # Extract example answer (handling stale element error)
                            try:
                                example_answer = driver.find_element(By.CLASS_NAME, 'CodeMirror').text.strip()
                            except Exception:
                                example_answer = "No example answer found"

                            question_details = {
                                "title": question_title,
                                "difficulty": question_difficulty,
                                "url": f"{question_url}/description/",
                                "content": question_content,
                                "example_answer": example_answer
                            }

                            logging.info(f"Scraped question: {question_title}")
                            questions.append(question_details)
                            break  # Exit retry loop on success

                        except StaleElementReferenceException:
                            retries -= 1
                            if retries == 0:
                                logging.error(f"Failed to extract details for {question_title} after retries.")
                            else:
                                logging.warning(f"Stale element reference error for {question_title}. Retrying...")

                except Exception as e:
                    logging.error(f"Error loading details for {question_title}: {e}")
                    logging.error(driver.page_source)  # Log the HTML of the page

        # Check for a "next" button and navigate to the next page if it exists
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Next"]')
            next_button.click()
            WebDriverWait(driver, 10).until(EC.staleness_of(next_button))  # Wait for the page to load
        except Exception as e:
            print("No more pages or failed to click 'Next'.")

    logging.info(f"Scraped {len(questions)} questions.")
    return questions

def main():
    logging.info('Connecting to Scraping Browser...')
    try:
        sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
        with Remote(sbr_connection, options=ChromeOptions()) as driver:
            logging.info('Connected! Navigating to LeetCode...')
            try:
                questions = scrape_leetcode(driver)

                # Save results to a file
                with open('leetcode_questions.json', 'w') as f:
                    json.dump(questions, f, indent=4)

                logging.info("Scraping completed. Results saved to 'leetcode_questions.json'.")
            except Exception as e:
                logging.error(f"Scraping failed: {e}")
    except Exception as e:
        logging.error(f"Failed to connect to Scraping Browser: {e}")

if __name__ == '__main__':
    main()


# COMMAND ----------

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By

# Configure logging
logging.basicConfig(filename='scraping.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Enter your credentials for Bright Data proxy
AUTH = 'brd-customer-hl_80709a30-zone-hadar_tomer_amit:i53s9wkm3hgu'
SBR_WEBDRIVER = f'https://{AUTH}@zproxy.lum-superproxy.io:9515'

# Scrape LeetCode problems with BeautifulSoup
def scrape_leetcode():
    print("Scraping LeetCode questions and topics...")

    # Set up the browser to use Bright Data proxy
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Uncomment this if you don't need a browser window
    chrome_options.add_argument(f'--proxy-server=zproxy.lum-superproxy.io:9515')

    # Set up the webdriver with options
    driver = webdriver.Chrome(service=Service(SBR_WEBDRIVER), options=chrome_options)

    # Send request to the problem set page
    driver.get('https://leetcode.com/problemset/all/')

    # Wait for page to load fully
    time.sleep(3)  # Adjust as necessary for loading time

    # Get the page content
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    questions = []

    # Find the question rows in the table
    question_rows = soup.select('div[role="rowgroup"] div[role="row"]')

    for row in question_rows:
        cols = row.find_all('div', {'role': 'cell'})
        if len(cols) >= 2:
            question_title = cols[1].get_text(strip=True)
            question_url = cols[1].find('a')['href']
            question_difficulty = cols[-1].get_text(strip=True)

            # Navigate to the question's description page
            question_page_url = f"https://leetcode.com{question_url}/description/"
            question_content = get_question_content(question_page_url)

            question_details = {
                "title": question_title,
                "difficulty": question_difficulty,
                "url": question_page_url,
                "content": question_content
            }

            print(question_details)  # Print the question details
            questions.append(question_details)

            time.sleep(1)  # Add a delay between requests

    print(f"Scraped {len(questions)} questions.")
    driver.quit()  # Close the browser
    return questions

# Get the question content from the description page
def get_question_content(url):
    session = requests.Session()
    session.proxies = {
        'http': f'http://{AUTH}@zproxy.lum-superproxy.io:9515',
        'https': f'http://{AUTH}@zproxy.lum-superproxy.io:9515'
    }

    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        content = soup.find('div', {'class': 'description__24sA'}).get_text(strip=True)
        return content
    except AttributeError:
        return "Description not available"

def main():
    try:
        questions = scrape_leetcode()

        # Save results to a file
        with open('leetcode_questions.json', 'w') as f:
            json.dump(questions, f, indent=4)

        print("Scraping completed. Results saved to 'leetcode_questions.json'.")
    except Exception as e:
        logging.error(f"Scraping failed: {e}")
        print(f"Scraping failed: {e}")

if __name__ == '__main__':
    main()


# COMMAND ----------



# COMMAND ----------

import requests

# Define headers (update with your own credentials if necessary)
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/json',
}

# GraphQL query for problem data
graphql_query = {
    "query": """
    query getQuestion($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
            title
            content
            difficulty
            likes
            dislikes
        }
    }
    """,
    "variables": {"titleSlug": "Add-Two-Numbers"}  # Replace with the slug of your desired question
}

# Send request to LeetCode GraphQL endpoint
response = requests.post(
    "https://leetcode.com/graphql/",
    json=graphql_query,
    headers=headers
)

# Parse and print response
if response.status_code == 200:
    question_data = response.json()
    print(question_data)
else:
    print(f"Failed to fetch data: {response.status_code}")

# COMMAND ----------

import re

# Define the topics and their corresponding keywords
topics_keywords = {
    "Arrays": ["array", "subarray", "sliding window", "sorted array", "matrix"],
    "Linked Lists": ["linked list", "node", "reverse linked list", "merge lists", "cycle in linked list"],
    "Trees": ["binary tree", "binary search tree", "root", "leaf", "preorder", "inorder", "postorder", "level order"],
    "Graphs": ["graph", "bfs", "dfs", "connected", "adjacency", "cycle", "topological sort"],
    "Dynamic Programming": ["dp", "dynamic programming", "memoization", "bottom-up", "top-down", "longest subsequence", "knapsack"],
    "Sorting and Searching": ["sort", "quick sort", "merge sort", "binary search", "search", "sorting"],
    "Recursion": ["recursion", "backtracking", "divide and conquer", "depth-first search", "recursive"],
    "Backtracking": ["backtracking", "subset", "permutation", "combination", "n-queens", "sum"],
    "Greedy Algorithms": ["greedy", "interval", "minimum", "maximum", "optimal", "greedy choice"],
    "Mathematics": ["gcd", "lcm", "factorial", "prime", "combinatorics", "fibonacci", "puzzle", "math"],
    "Bit Manipulation": ["bit", "xor", "and", "or", "shift", "binary", "mask"],
    "String Manipulation": ["string", "substring", "anagram", "pattern", "palindrome", "reverse", "match"],
}

# Function to classify a list of problems into topics
def classify_problems(problems):
    classified_problems = {topic: [] for topic in topics_keywords}

    for problem in problems:
        title = problem['title'].lower()  # Convert the title to lowercase for case-insensitive comparison
        classified = False

        # Check each topic and see if any of its keywords appear in the title
        for topic, keywords in topics_keywords.items():
            for keyword in keywords:
                if re.search(r"\b" + re.escape(keyword) + r"\b", title):  # Use word boundaries for exact match
                    classified_problems[topic].append(problem['title'])
                    classified = True
                    break
            if classified:
                break

        # If no match found, categorize it under 'Unclassified'
        if not classified:
            if "Unclassified" not in classified_problems:
                classified_problems["Unclassified"] = []
            classified_problems["Unclassified"].append(problem['title'])

    return classified_problems

# Example list of problems
problems = [
    {"title": "Add Two Numbers"},
    {"title": "Binary Tree Inorder Traversal"},
    {"title": "Merge Sorted Array"},
    {"title": "Find Minimum in Rotated Sorted Array"},
    {"title": "Longest Substring Without Repeating Characters"},
    {"title": "Generate Parentheses"},
    {"title": "Reverse Linked List"},
    {"title": "Knapsack Problem"},
    {"title": "Word Search"},
]

# Classify the problems into topics
classified = classify_problems(problems)

# Print the results
for topic, problems in classified.items():
    print(f"{topic}:")
    for problem in problems:
        print(f" - {problem}")
    print()

# COMMAND ----------

from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
import torch

# Define the topics (labels)
topics = [
    "Arrays", "Linked Lists", "Trees", "Graphs", "Dynamic Programming", 
    "Sorting and Searching", "Recursion", "Backtracking", 
    "Greedy Algorithms", "Mathematics", "Bit Manipulation", "String Manipulation"
]

# Sample problems with titles (no description needed for this example)
problems = [
    {"title": "Add Two Numbers"},
    {"title": "Binary Tree Inorder Traversal"},
    {"title": "Merge Sorted Array"},
    {"title": "Find Minimum in Rotated Sorted Array"},
    {"title": "Longest Substring Without Repeating Characters"},
    {"title": "Generate Parentheses"},
    {"title": "Reverse Linked List"},
    {"title": "Knapsack Problem"},
    {"title": "Word Search"}
]

# Define Dataset for loading problems
class ProblemDataset(Dataset):
    def __init__(self, problems, tokenizer, max_length=128):
        self.problems = problems
        self.tokenizer = tokenizer
        self.max_length = max_length
        
    def __len__(self):
        return len(self.problems)
    
    def __getitem__(self, idx):
        problem = self.problems[idx]
        title = problem['title']
        
        encoding = self.tokenizer.encode_plus(
            title, 
            add_special_tokens=True, 
            max_length=self.max_length, 
            padding='max_length', 
            truncation=True, 
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten()
        }

# Load pre-trained BERT tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Prepare the dataset
dataset = ProblemDataset(problems, tokenizer)
data_loader = DataLoader(dataset, batch_size=2)

# Load pre-trained BERT model for sequence classification
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(topics))

# Move the model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Define the classifier function
def classify_problem(problem):
    inputs = tokenizer(problem['title'], return_tensors='pt', padding=True, truncation=True, max_length=128).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=-1).item()
    return topics[predicted_class]

# Classify each problem
for problem in problems:
    topic = classify_problem(problem)
    print(f"Problem: {problem['title']} | Classified Topic: {topic}")

# COMMAND ----------

# DBTITLE 1,Amit copies from github
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm
import time
import pandas as pd

options = Options()
options.headless = True
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--remote-debugging-port=9222')  # Add this line
driver = webdriver.Chrome(options=options)
driver.set_window_size(1920, 1080)
driver.maximize_window()

# click helper, wait until page source changed
def click(button, timeout=3):
        prev_src = driver.page_source
        elapsed = 0
        unit_time = timeout / 10
        button.click()
        while prev_src == driver.page_source and elapsed <= timeout:
            time.sleep(unit_time)
            timeout -= unit_time
            elapsed += unit_time
            
# login to leetcode
def login(username, password):
    login_url = 'https://leetcode.com/accounts/login/'
    driver.get(login_url)
    time.sleep(2)
    username_field = driver.find_element_by_xpath('//input[@id="id_login"]')
    password_field = driver.find_element_by_xpath('//input[@id="id_password"]')
    signin_button = driver.find_element_by_xpath('//button[@id="signin_btn"]')
    username_field.send_keys(username)
    password_field.send_keys(password)
    click(signin_button)
    print('successfully logged in!') 

# get company info from a problem URL
def get_problem_companies_info(problem_url, debug=False):
    companies_info = dict()  # key: company name, value: number of occurances
    driver.get(problem_url)
    time.sleep(2)
    # locate and click on the 'Companies' <div>
    try:
        companies_div = driver.find_element_by_xpath("//div[text()='Companies']")
        click(companies_div)
    except NoSuchElementException as e:
        print('company not found')
        return companies_info
    # if there exists a 'More' <span>, click on it to show all companies
    try:
        show_more_span = driver.find_element_by_xpath("//span[text()='More']")
        click(show_more_span)
    except NoSuchElementException as e:
        pass
    # locate the <div> that leetcode places all its little "company tags"
    company_tag_wrapper = driver.find_element_by_xpath("//div[starts-with(@class, 'company-tag-wrapper')]")
    companies_info_raw = company_tag_wrapper.text.replace('\n|\n', '|').split('\n')
    if debug: print(companies_info_raw)
    for company in companies_info_raw:
        if company == '|': continue
        company_info = company.split('|')
        if len(company_info) == 1:
            company_name = company_info[0]
            companies_info[company_name] = 1
        else:
            company_name = company_info[0]
            num_occur = company_info[1]
            companies_info[company_name] = num_occur
    return companies_info

# iterate through leetcode_problems to collect their company info
def get_problems_companies_info(leetcode_problems, debug=False):
    problems_companies_info = []  # list of tuples
    for _, problem in leetcode_problems.iterrows():
        problem_link = problem['link']
        problem_name = problem['name']
        print('handling', problem_link)
        try:
            companies_info = get_problem_companies_info(problem_link, debug)
            # pivot longer
            for company_name, num_occur in companies_info.items():
                new_row = (problem_link, problem_name, company_name, num_occur,)
                problems_companies_info.append(new_row)
                if debug: print(new_row)
        except Exception as e:
            # log the error
            print('error:', e)
    return pd.DataFrame(problems_companies_info, 
                        columns = ['problem_link', 'problem_name', 'company_name', 'num_occur'])

# COMMAND ----------

# note: this cell takes around 1 hour to finish
# go through questions in the leetcode question list
leetcode_problems = pd.read_csv('../data/leetcode_problems.csv')
problems_companies_info = get_problems_companies_info(leetcode_problems)
problems_companies_info.to_csv('../data/leetcode_problems_and_companies.csv', index=False)
