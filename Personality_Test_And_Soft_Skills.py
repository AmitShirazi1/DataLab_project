# Databricks notebook source
# DBTITLE 1,hadar and claude
import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

const PersonalityTest = () => {
  const [answers, setAnswers] = useState({});
  const [isSubmitted, setIsSubmitted] = useState(false);

  const questions = [
    { id: 1, text: "I enjoy meeting new people" },
    { id: 2, text: "I like helping others" },
    { id: 3, text: "I adapt well to change" },
    { id: 4, text: "I prefer working in teams" },
    { id: 5, text: "I enjoy learning new skills" }
  ];

  const options = [
    { value: 1, label: "Strongly Disagree" },
    { value: 2, label: "Disagree" },
    { value: 3, label: "Unsure" },
    { value: 4, label: "Agree" },
    { value: 5, label: "Strongly Agree" }
  ];

  const handleAnswer = (questionId, value) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: value
    }));
  };

  const handleSubmit = () => {
    setIsSubmitted(true);
    // Here you can add logic to send the results to your backend
    console.log(answers);
  };

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>Personality Assessment</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {questions.map((question) => (
            <div key={question.id} className="space-y-2">
              <div className="flex items-center gap-4">
                <span className="min-w-8">{question.id}</span>
                <span className="flex-grow">{question.text}</span>
              </div>
              <div className="grid grid-cols-5 gap-2">
                {options.map((option) => (
                  <button
                    key={option.value}
                    onClick={() => handleAnswer(question.id, option.value)}
                    className={`p-2 rounded-full w-6 h-6 flex items-center justify-center border ${
                      answers[question.id] === option.value
                        ? 'bg-blue-500 border-blue-500 text-white'
                        : 'border-gray-300'
                    }`}
                  >
                  </button>
                ))}
              </div>
            </div>
          ))}
          <Button 
            onClick={handleSubmit}
            className="w-full mt-4"
            disabled={Object.keys(answers).length !== questions.length}
          >
            Submit
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default PersonalityTest;

# COMMAND ----------

# DBTITLE 1,scraping
import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd

def scrape_personality_test():
    url = "https://www.123test.com/personality-test/"
    
    # Add headers to avoid being blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract questions (this is a placeholder - you'll need to adjust selectors based on actual HTML structure)
    questions = soup.find_all('div', class_='question-text')  
    return [q.text.strip() for q in questions]

# COMMAND ----------

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

# MAGIC %md
# MAGIC big 5 (OCEAN)

# COMMAND ----------

pip install streamlit pandas google-generativeai

# COMMAND ----------

API_KEY = 'AIzaSyBEV89GjyAbAUgTunqeyHNlPvHuTR7K3X8'

# COMMAND ----------

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
