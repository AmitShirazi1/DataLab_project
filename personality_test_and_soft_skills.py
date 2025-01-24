# Databricks notebook source
# MAGIC %md
# MAGIC scraping 123test

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

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC soft skills

# COMMAND ----------

# DBTITLE 1,GPT first attempt
import pandas as pd
import random
from typing import List

class JobInterviewSimulator:
    def __init__(self, csv_file: str):
        self.questions_df = pd.read_csv(csv_file)  # Load common questions
        self.cv_info = {}

    def parse_cv(self, cv_text: str):
        # Dummy parser (replace with an actual parsing logic for structured data)
        self.cv_info = {
            "skills": ["Python", "Machine Learning"],
            "experience": ["Data Scientist at XYZ", "Intern at ABC"],
            "education": ["BSc in Computer Science"],
        }
        print("CV Parsed:", self.cv_info)

    def generate_questions(self, job_post: str) -> List[str]:
        # Generate tailored questions based on CV and job post
        tailored_questions = [
            f"Can you explain how you used {skill} in your previous role?" for skill in self.cv_info.get("skills", [])
        ]
        tailored_questions.append(f"How does your experience at {self.cv_info.get('experience', [''])[0]} prepare you for this {job_post} position?")
        
        # Add some general questions from CSV
        common_questions = self.questions_df.sample(n=5)["question"].tolist()
        
        return tailored_questions + common_questions

    def ask_questions(self, questions: List[str]):
        print("\n--- Interview Questions ---")
        user_responses = {}
        for i, question in enumerate(questions, start=1):
            print(f"Q{i}: {question}")
            response = input(f"Your Answer: ")  # Replace with a GUI text box for real applications
            user_responses[f"Q{i}"] = response
        
        return user_responses

    def provide_feedback(self, responses: dict):
        print("\n--- Feedback ---")
        for q, answer in responses.items():
            # Dummy feedback logic (replace with NLP-powered analysis for structure, tone, etc.)
            feedback = "Great answer!" if len(answer) > 10 else "Try to elaborate more."
            print(f"{q}: {feedback}")

# Example usage:
simulator = JobInterviewSimulator(csv_file="common_questions.csv")

# 1. Parse CV
cv_text = """Sample CV text here..."""  # Replace with text extraction logic
simulator.parse_cv(cv_text)

# 2. Generate Questions
job_post = "Data Scientist"
questions = simulator.generate_questions(job_post)

# 3. Ask Questions
responses = simulator.ask_questions(questions)

# 4. Provide Feedback
simulator.provide_feedback(responses)


# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC trying to create the IPIP-120 test (from the csv files)

# COMMAND ----------

# Those are the test website links
https://github.com/rubynor/bigfive-web
https://bigfive-test.com/

# COMMAND ----------

pip install streamlit pandas google-generativeai
API_KEY = 'AIzaSyBEV89GjyAbAUgTunqeyHNlPvHuTR7K3X8'

# COMMAND ----------

import csv
from tabulate import tabulate

def load_questions(filename):
    """Load questions from a CSV file."""
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        questions = [row[0] for row in reader]
    return questions

def conduct_test(questions):
    """Conduct the test by presenting questions and collecting responses."""
    data = [
    [1, "Very Inaccurate", "If you strongly disagree or if the statement is definitely false"],
    [2, "Moderately Inaccurate", "If you disagree or if the statement is mostly false"],
    [3, "Neither Accurate Nor Inaccurate", "If you are neutral about the statement, if you cannot decide, or if the statement is about equally true and false"],
    [4, "Moderately Accurate", "If you agree or if the statement is mostly true"],
    [5, "Very Accurate", "If you strongly agree or if the statement is definitely true"]
    ]

    print("This will be a simulation of a personality test.")
    print("In this test you will be required to answer the following questions on a scale from 1 to 5.")
    print(tabulate(data, headers=["Scale", "Rating", "Description"], tablefmt="grid"))
    print("Please enter a number between 1 and 5 for each question:\n")
    
    responses = []
    for i, question in enumerate(questions, start=1):
        print(f"{i}. {question}")
        while True:
            try:
                response = int(input("Your response (1-5): "))
                if response in range(1, 6):
                    responses.append(response)
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 5.")
    
    return responses

def save_responses(responses, filename="responses.csv"):
    """Save user responses to a CSV file."""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Question Number", "Response"])
        for i, response in enumerate(responses, start=1):
            writer.writerow([i, response])


# COMMAND ----------

# Load the questions from the CSV file
questions = load_questions("big_5_test.csv")

# Conduct the test and collect responses
if questions:
    responses = conduct_test(questions)
    
    # Save responses
    save_responses(responses)
    print("\nThank you for completing the test! Your responses have been saved to 'responses.csv'.")
else:
    print("No questions found in the CSV file.")


# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC codes i need to delete later

# COMMAND ----------

# DBTITLE 1,example with streamlit
import streamlit as st
import google.generativeai as genai

def create_personality_test():
    st.title("Personality Test")
    
    # Store responses
    if 'responses' not in st.session_state:
        st.session_state.responses = {}

    # Questions (you can either hardcode or get from scraping)
    questions = [
        "I enjoy meeting new people",
        "I like helping others",
        "I sometimes make mistakes",
        "I'm easily disappointed",
        "I enjoy repairing things"
        # Add more questions from your scraping
    ]

    # Create form
    with st.form("personality_test"):
        for i, question in enumerate(questions, 1):
            st.write(f"\n{i}. {question}")
            response = st.radio(
                "Select your answer:",
                ["Strongly Disagree", "Disagree", "Unsure", "Agree", "Strongly Agree"],
                key=f"q_{i}",
                horizontal=True,
                label_visibility="collapsed"
            )
            st.session_state.responses[question] = response
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            analyze_results()

def analyze_results():
    # Configure Gemini
    genai.configure(api_key='YOUR_GEMINI_API_KEY')
    model = genai.GenerativeModel('gemini-pro')

    # Prepare results for analysis
    responses_text = "\n".join([f"Question: {q}\nResponse: {r}" 
                              for q, r in st.session_state.responses.items()])
    
    prompt = f"""
    Based on these personality test responses:
    {responses_text}
    
    Please provide:
    1. A personality analysis
    2. Key strengths
    3. Potential areas for growth
    4. Career suggestions that might match this personality profile
    """
    
    response = model.generate_content(prompt)
    
    st.write("### Your Personality Analysis")
    st.write(response.text)

# Run the app
if __name__ == "__main__":
    create_personality_test()

# COMMAND ----------

# DBTITLE 1,big 5 (OCEAN)
import streamlit as st
import google.generativeai as genai
import pandas as pd

def create_big_five_test():
    st.title("Big Five Personality Test")
    
    # Define questions based on Big Five traits
    questions = {
        "Openness": [
            "I enjoy trying new experiences",
            "I am curious about many different things",
            "I enjoy abstract or theoretical discussions"
        ],
        "Conscientiousness": [
            "I am always prepared",
            "I pay attention to details",
            "I follow a schedule"
        ],
        "Extraversion": [
            "I start conversations with others",
            "I enjoy being the center of attention",
            "I feel comfortable around people"
        ],
        "Agreeableness": [
            "I sympathize with others' feelings",
            "I take time out for others",
            "I make people feel at ease"
        ],
        "Neuroticism": [
            "I get stressed out easily",
            "I worry about things",
            "I change my mood often"
        ]
    }
    
    if 'responses' not in st.session_state:
        st.session_state.responses = {}

    with st.form("personality_test"):
        for trait, trait_questions in questions.items():
            st.subheader(trait)
            for i, question in enumerate(trait_questions):
                response = st.radio(
                    f"{question}",
                    ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"],
                    key=f"{trait}_{i}",
                    horizontal=True
                )
                st.session_state.responses[f"{trait}_{question}"] = response
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            analyze_big_five_results()

def analyze_big_five_results():
    # Convert responses to scores (1-5)
    score_mapping = {
        "Strongly Disagree": 1,
        "Disagree": 2,
        "Neutral": 3,
        "Agree": 4,
        "Strongly Agree": 5
    }
    
    # Calculate trait scores
    trait_scores = {}
    for key, value in st.session_state.responses.items():
        trait = key.split('_')[0]
        if trait not in trait_scores:
            trait_scores[trait] = []
        trait_scores[trait].append(score_mapping[value])

    # Calculate averages
    trait_averages = {trait: sum(scores)/len(scores) 
                     for trait, scores in trait_scores.items()}

    # Send to Gemini for analysis
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-flash')

    analysis_prompt = f"""
    Based on these Big Five personality trait scores (out of 5):
    {trait_averages}
    
    Please provide:
    1. A comprehensive personality analysis
    2. Key strengths and potential challenges
    3. Career suggestions that match this profile
    4. Personal development recommendations
    
    Base your analysis on established psychological research about the Big Five personality traits.
    """
    
    response = model.generate_content(analysis_prompt)
    
    # Display results
    st.write("### Your Personality Analysis")
    st.write(response.text)
    
    # Show scores visualization
    scores_df = pd.DataFrame(list(trait_averages.items()), 
                           columns=['Trait', 'Score'])
    st.bar_chart(scores_df.set_index('Trait'))

if __name__ == "__main__":
    create_big_five_test() 
