# Databricks notebook source
# MAGIC %md
# MAGIC #### Those are the original test website links: ⬇️
# MAGIC https://github.com/rubynor/bigfive-web <br>
# MAGIC https://bigfive-test.com/ <br>
# MAGIC (We based our personality test and its results on this MIT website)
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC #### 😊 The IPIP-NEO-120 test:

# COMMAND ----------

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime
import os
from IPython.display import display
import random
import pytz

DATA_PATH = '/Workspace/Users/amit.shirazi@campus.technion.ac.il/project/data/questions_and_answers/OCEAN_test/'

random.seed(42)

# Define choices structure
CHOICES = {
    "plus": [
        {"text": "Very Inaccurate", "score": 1},
        {"text": "Moderately Inaccurate", "score": 2},
        {"text": "Neither Accurate Nor Inaccurate", "score": 3},
        {"text": "Moderately Accurate", "score": 4},
        {"text": "Very Accurate", "score": 5}
    ],
    "minus": [
        {"text": "Very Inaccurate", "score": 5},
        {"text": "Moderately Inaccurate", "score": 4},
        {"text": "Neither Accurate Nor Inaccurate", "score": 3},
        {"text": "Moderately Accurate", "score": 2},
        {"text": "Very Accurate", "score": 1}
    ]
}

class IPIPNeoTest:
    def __init__(self):
        self.domains = {
            'N': 'Neuroticism',
            'E': 'Extraversion',
            'O': 'Openness To Experience',
            'A': 'Agreeableness',
            'C': 'Conscientiousness'
        }
        
        # Load questions and domain descriptions
        with open(f"{DATA_PATH}questions_ipip_neo_120.json", 'r') as f:
            self.questions = json.load(f)
            
        with open(f"{DATA_PATH}get-template-en.json", 'r') as f:
            self.domain_info = json.load(f)
    
    def get_score_for_response(self, response_text, keyed):
        """Get numerical score based on response text and question keying"""
        choices = CHOICES[keyed]
        for choice in choices:
            if choice["text"] == response_text:
                return choice["score"]
        return None
    
    def calculate_scores(self, responses):
        """Calculate domain and facet scores using the specified scoring system"""
        scores = {domain: {'total': 0, 'facets': {}} for domain in self.domains}
        
        for q_id, response in responses.items():
            question = next(q for q in self.questions if q['id'] == q_id)
            
            # Get score based on response text and question keying
            score = self.get_score_for_response(response, question['keyed'])
            
            domain = question['domain']
            facet = question['facet']
            
            # Initialize facet if needed
            if facet not in scores[domain]['facets']:
                scores[domain]['facets'][facet] = []
            
            # Add score to appropriate domain and facet
            scores[domain]['facets'][facet].append(score)
            scores[domain]['total'] += score
        
        # Calculate averages
        for domain in scores:
            # Average domain score
            scores[domain]['total'] /= len([q for q in self.questions if q['domain'] == domain])
            
            # Average facet scores
            for facet in scores[domain]['facets']:
                scores[domain]['facets'][facet] = sum(scores[domain]['facets'][facet]) / len(scores[domain]['facets'][facet])
        
        return scores

    def get_interpretation(self, domain_scores):
        """Get text interpretations for each domain score"""
        interpretations = {}
        
        for domain_code, score in domain_scores.items():
            domain_info = next(d for d in self.domain_info if d['domain'] == domain_code)
            
            # Determine score level
            if score['total'] < 2.7:
                level = 'low'
            elif score['total'] > 3.2:
                level = 'high'
            else:
                level = 'neutral'
            
            # Get corresponding interpretation text
            interpretation = next(r for r in domain_info['results'] if r['score'] == level)
            interpretations[domain_code] = {
                'text': interpretation['text'],
                'description': domain_info['description'],
                'facets': domain_info['facets']
            }
        
        return interpretations

    def create_visualizations(self, scores):
        """Create visualizations of the results"""
        # Radar chart of domain scores
        domain_scores = {self.domains[d]: scores[d]['total'] for d in scores}
        
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=list(domain_scores.values()),
            theta=list(domain_scores.keys()),
            fill='toself'
        ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[1, 5])),
            showlegend=False,
            title="Your Personality Profile Based on IPIP-NEO-120"
        )
        
        # Facet breakdown charts
        facet_figs = {}
        for domain in scores:
            facet_scores = scores[domain]['facets']

            # Get the facet titles
            domain_facets = next(d for d in self.domain_info if d['domain'] == domain)['facets']

            df_facets = pd.DataFrame({
                'Facet': [facet['title'] for facet in domain_facets],
                'Score': list(facet_scores.values())
            })
        
            fig_facets = px.bar(
                df_facets,
                x='Facet',
                y='Score',
                title=f"{self.domains[domain]} - Facets",
                color='Score',
                color_continuous_scale='RdYlBu'
            )

            fig_facets.update_layout(
                yaxis=dict(range=[0, 5]),
                coloraxis=dict(cmin=0, cmax=5)
                )

            facet_figs[domain] = fig_facets
        
        return fig_radar, facet_figs


# COMMAND ----------

# MAGIC %md
# MAGIC ###### The OCEAN Questionnaire - insert your answers and get your results 👇

# COMMAND ----------

# DBTITLE 1,the OCEAN questionnaire
def main():
    # Initialize the test object
    test = IPIPNeoTest()
    
    # Store responses in a dictionary
    responses = {}
    
    # Display questions
    print("Welcome to the IPIP-NEO-120 Personality Assessment!")

    # Randomize the order of all questions (shuffle the questions list)
    all_questions = test.questions
    random.shuffle(all_questions)

    for question in all_questions:
        # Get appropriate choices based on question keying
        choices = [choice["text"] for choice in CHOICES[question['keyed']]]

        # Display the question and choices
        print(f"\n{question['text']}")
        for idx, choice in enumerate(choices, 1):
            print(f"{idx}. {choice}")
        
        # Get a valid response from the user
        while True:
            try:
                choice_idx = int(input("Enter your choice (1-5): ")) - 1
                if 0 <= choice_idx < len(choices):
                    responses[question['id']] = choices[choice_idx]
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number.")
                
    """
    #### IF WE WANT THE QUESTIONS TO APPEAR IN ORDER BY DOMAIN:

    for domain_code, domain_name in test.domains.items():
        print(f"\n--- {domain_name} ---")
        domain_questions = [q for q in test.questions if q['domain'] == domain_code]
        
        for question in domain_questions:
            # Get appropriate choices based on question keying
            choices = [choice["text"] for choice in CHOICES[question['keyed']]]

            # Display the question and choices
            print(f"\n{question['text']}")
            for idx, choice in enumerate(choices, 1):
                print(f"{idx}. {choice}")
            
            # Get a valid response from the user
            while True:
                try:
                    choice_idx = int(input("Enter your choice (1-5): ")) - 1
                    if 0 <= choice_idx < len(choices):
                        responses[question['id']] = choices[choice_idx]
                        break
                    else:
                        print("Invalid choice. Please enter a number between 1 and 5.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
    """
    # Calculate scores
    scores = test.calculate_scores(responses)
    
    # Get interpretations
    interpretations = test.get_interpretation(scores)
    
    # Create visualizations
    radar_fig, facet_figs = test.create_visualizations(scores)
    
    # Display results
    print("\n--- Assessment Complete! ---")
    print("Your personality profile is as follows:")
    display(radar_fig)
    
    for domain_code, domain_name in test.domains.items():
        print(f"\n--- {domain_name} Details ---")
        display(facet_figs[domain_code])
        print(interpretations[domain_code]['text'])
        print("---")
        print("Domain Description:")
        print(interpretations[domain_code]['description'])
        print("---")
        print("Facet Details:")
        for facet in interpretations[domain_code]['facets']:
            print(f"{facet['title']}: {facet['text']}")
    
    israel_tz = pytz.timezone('Asia/Jerusalem') # modify the timezone if you are not in Israel

    # Save results as JSON
    results = {
        'timestamp': datetime.now(israel_tz).isoformat(),
        'domain_scores': {d: scores[d]['total'] for d in scores},
        'facet_scores': {d: scores[d]['facets'] for d in scores},
        'interpretations': interpretations
    }
    
    # Define the path where the results file should be saved
    results_file = os.path.join(DATA_PATH, "ipip_neo_results.json")

    # Save results as JSON
    os.makedirs(DATA_PATH, exist_ok=True)
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults have been saved to '{results_file}'.")

if __name__ == "__main__":
    main()

# COMMAND ----------

# MAGIC %md
# MAGIC ###### To the sample testing please run the main code below 👇

# COMMAND ----------

# DBTITLE 1,RANDOM SAMPLE TESTING
def main():
    # Initialize the test object
    test = IPIPNeoTest()
    
    # Store responses in a dictionary
    responses = {}
    
    # Display questions
    print("Welcome to the IPIP-NEO-120 Personality Assessment!")

    # Randomize the order of all questions (shuffle the questions list)
    all_questions = test.questions
    random.shuffle(all_questions)
    
    for question in all_questions:
        # Get appropriate choices based on question keying
        choices = [choice["text"] for choice in CHOICES[question['keyed']]]
        # ------ THE TEST CODE ------
        responses[question['id']] = random.choice(choices)

    """
    #### IF WE WANT THE QUESTIONS TO APPEAR IN ORDER BY DOMAIN:

    for domain_code, domain_name in test.domains.items():
        print(f"\n--- {domain_name} ---")
        domain_questions = [q for q in test.questions if q['domain'] == domain_code]
        
        for question in domain_questions:
            # Get appropriate choices based on question keying
            choices = [choice["text"] for choice in CHOICES[question['keyed']]]
            # ------ THE TEST CODE ------
            responses[question['id']] = random.choice(choices)
    """
    # Calculate scores
    scores = test.calculate_scores(responses)
    
    # Get interpretations
    interpretations = test.get_interpretation(scores)
    
    # Create visualizations
    radar_fig, facet_figs = test.create_visualizations(scores)
    
    # Display results
    print("\n--- Assessment Complete! ---")
    print("Your personality profile is as follows:")
    display(radar_fig)
    
    for domain_code, domain_name in test.domains.items():
        print(f"\n--- {domain_name} Details ---")
        display(facet_figs[domain_code])
        print(interpretations[domain_code]['text'])
        print("---")
        print("Domain Description:")
        print(interpretations[domain_code]['description'])
        print("---")
        print("Facet Details:")
        for facet in interpretations[domain_code]['facets']:
            print(f"{facet['title']}: {facet['text']}")
    
    israel_tz = pytz.timezone('Asia/Jerusalem') # modify the timezone if you are not in Israel

    # Save results as JSON
    results = {
        'timestamp': datetime.now(israel_tz).isoformat(),
        'domain_scores': {d: scores[d]['total'] for d in scores},
        'facet_scores': {d: scores[d]['facets'] for d in scores},
        'interpretations': interpretations
    }
    
    # Define the path where the results file should be saved
    results_file = os.path.join(DATA_PATH, "ipip_neo_results.json")

    # Save results as JSON
    os.makedirs(DATA_PATH, exist_ok=True)
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults have been saved to '{results_file}'.")

if __name__ == "__main__":
    main()

# COMMAND ----------

# MAGIC %md
# MAGIC ### optional adjustments ⏬

# COMMAND ----------

# MAGIC %md
# MAGIC #### The streamlit version for the main

# COMMAND ----------

import streamlit as st

def main():
    st.title("IPIP-NEO-120 Personality Assessment")
    
    # Initialize session state
    if 'test' not in st.session_state:
        st.session_state.test = IPIPNeoTest()
        st.session_state.current_question = 0
        st.session_state.responses = {}
        st.session_state.test_complete = False
        random.seed(42)
        st.session_state.questions = list(st.session_state.test.questions)
        random.shuffle(st.session_state.questions)

    if not st.session_state.test_complete:
        # Display progress
        progress = len(st.session_state.responses) / len(st.session_state.questions)
        st.progress(progress)
        st.write(f"Question {len(st.session_state.responses) + 1} of {len(st.session_state.questions)}")

        # Display current question
        current_q = st.session_state.questions[st.session_state.current_question]
        st.write(f"**{current_q['text']}**")
        
        # Get choices based on question keying
        choices = [choice["text"] for choice in CHOICES[current_q['keyed']]]
        
        # Create radio buttons for choices
        response = st.radio("Select your answer:", choices, key=f"q_{current_q['id']}")
        
        # Next button
        if st.button("Next"):
            st.session_state.responses[current_q['id']] = response
            
            if st.session_state.current_question < len(st.session_state.questions) - 1:
                st.session_state.current_question += 1
                st.experimental_rerun()
            else:
                st.session_state.test_complete = True
                st.experimental_rerun()

    else:
        # Calculate and display results
        scores = st.session_state.test.calculate_scores(st.session_state.responses)
        interpretations = st.session_state.test.get_interpretation(scores)
        radar_fig, facet_figs = st.session_state.test.create_visualizations(scores)

        st.write("## Your Results")
        
        # Display radar chart
        st.plotly_chart(radar_fig, use_container_width=True)
        
        # Display detailed results for each domain
        for domain_code, domain_name in st.session_state.test.domains.items():
            with st.expander(f"{domain_name} Details"):
                st.plotly_chart(facet_figs[domain_code], use_container_width=True)
                st.write("---")
                st.write("### Interpretation")
                st.write(interpretations[domain_code]['text'])
                st.write("---")
                st.write("### Domain Description")
                st.write(interpretations[domain_code]['description'])
                st.write("---")
                st.write("### Facet Details")
                for facet in interpretations[domain_code]['facets']:
                    st.write(f"**{facet['title']}:** {facet['text']}")

        # Save results
        if st.button("Save Results"):
            israel_tz = pytz.timezone('Asia/Jerusalem')
            results = {
                'timestamp': datetime.now(israel_tz).isoformat(),
                'domain_scores': {d: scores[d]['total'] for d in scores},
                'facet_scores': {d: scores[d]['facets'] for d in scores},
                'interpretations': interpretations
            }
            
            os.makedirs(DATA_PATH, exist_ok=True)
            results_file = os.path.join(DATA_PATH, "ipip_neo_results.json")
            
            with open(results_file, "w") as f:
                json.dump(results, f, indent=2)
            
            st.success(f"Results have been saved successfully!")

if __name__ == "__main__":
    main()

# COMMAND ----------

# MAGIC %md
# MAGIC #### scraping 123test 

# COMMAND ----------

pip install requests beautifulsoup4

# COMMAND ----------

import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape the webpage
def scrape_website(url, tag, class_name=None):
    # Send a request to the website
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all elements with the specified tag and class
    if class_name:
        elements = soup.find_all(tag, class_=class_name)
    else:
        elements = soup.find_all(tag)

    # Extract and return text content
    return [element.text.strip() for element in elements]

# Function to save data to a CSV file
def save_to_csv(data, filename="output.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Content"])  # Header
        for row in data:
            writer.writerow([row])



# COMMAND ----------

# URL of the website to scrape
url = "https://www.123test.com/personality-test/" 

# HTML tag and class to extract
tag = "div"  
class_name = "its123-label-text"

# Scrape the website
scraped_data = scrape_website(url, tag, class_name)

# Save the data to a CSV file
if scraped_data:
    save_to_csv(scraped_data, filename="big_5_test.csv")
    print(f"Scraped {len(scraped_data)} items and saved to big_5_test.csv")
else:
    print("Something went worng! No data scraped.")
