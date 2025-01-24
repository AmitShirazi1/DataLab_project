# Databricks notebook source
import requests
import pandas as pd
import json
import time
from datetime import datetime
import os

## checking on all problems with no solution_URL

def fetch_leetcode_problems(question_names_df):
    # Convert question names to slugs
    question_names = question_names_df['title'].tolist()
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
    current_path = os.getcwd()
    data_path = os.path.join(current_path, 'data/questions_and_answers/leetcode_problems_data.csv')
    question_names_df = pd.read_csv(data_path)
    # question_names_df = pd.read_csv('/Workspace/Users/amit.shirazi@campus.technion.ac.il/project/data/questions_and_answers/leetcode_problems_data.csv')
    problems_df = fetch_leetcode_problems(question_names_df)

# COMMAND ----------

import requests
import pandas as pd
import json
import time
from datetime import datetime
import os

current_path = os.getcwd()
data_path = os.path.join(current_path, 'data/questions_and_answers/leetcode_problems_metadata.csv')
leetcode_problems_metadata = pd.read_csv(data_path)


# COMMAND ----------

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function to extract all URLs from a page
def extract_all_urls(base_url):
    try:
        # Send a GET request to the URL
        print('here')
        response = requests.get(base_url)
        # response.raise_for_status()  # Raise an exception for HTTP errors
        print('here2')
        print(response.status_code)

        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <a> tags
        links = soup.find_all('a', href=True)

        # Build full URLs and store them in a list
        urls = [urljoin(base_url, link['href']) for link in links]

        return urls
    except Exception as e:
        return [f"Error: {e}"]

# Example LeetCode solutions page URL
url = "https://leetcode.com/problems/add-two-numbers/solutions/"

# Extract all URLs from the page
all_urls = extract_all_urls(url)

# Print the extracted URLs
for i, extracted_url in enumerate(all_urls, 1):
    print(f"{i}. {extracted_url}")
