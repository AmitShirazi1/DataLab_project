%pip install streamlit

import streamlit as st
import pandas as pd
import random
import os
from consts import JOBS_PATH, DATA_PATH

# Load datasets
jobs_sample = pd.read_csv(os.path.join(JOBS_PATH, "jobs_sample.csv"))
code_questions_scores = pd.read_csv(os.path.join(DATA_PATH, "code_scores.csv"))
open_questions_scores = pd.read_csv(os.path.join(DATA_PATH, "open_scores.csv"))
all_jobpostings = pd.read_csv(os.path.join(JOBS_PATH, "all_jobpostings_with_skills.csv"))

def get_top_questions(job_id, dataset, top_n=20):
    """Get the top N questions for a specific job ID from a dataset."""
    filtered_questions = dataset[dataset['job_id'] == job_id]
    sorted_questions = filtered_questions.sort_values(by='score', ascending=False)
    return sorted_questions.head(top_n)

def remove_job_occurrences(job_id, datasets):
    """Remove all occurrences of a job ID from the provided datasets."""
    for dataset in datasets:
        dataset.drop(dataset[dataset['job_id'] == job_id].index, inplace=True)

def map_seniority_level(level):
    """Map level integers to seniority descriptions."""
    mapping = {
        "0": "Internship",
        "1": "Entry level/Associate",
        "2": "Mid-Senior level/Manager and above",
        None: "Unknown"
    }
    return mapping.get(level, "Unknown")

def main():
    st.title("Job Interview Simulator")

    # Job Selection Method
    st.header("Choose a Job Selection Method")
    selection_method = st.radio("How would you like to select the job?", ("Pick from List", "Random Job (10,718 options)"))

    if selection_method == "Pick from List":
        st.header("Select a Job")
        jobs_sample["seniority_level"] = jobs_sample["level"].apply(map_seniority_level)
        jobs_sample["display_info"] = jobs_sample.apply(lambda row: f"{row['job_title']} | {row['seniority_level']} | {row['company_name']}", axis=1)
        selected_job_row = st.radio("Choose a job:", jobs_sample["display_info"].index, format_func=lambda idx: jobs_sample["display_info"].iloc[idx])
        selected_job = jobs_sample.loc[selected_job_row]
    else:
        st.header("Randomly Selected Job")
        selected_job = all_jobpostings.sample(1).iloc[0]

    # Display job details
    st.header("Selected Job")
    def display_job_details(column_name, entry):
        if entry and (entry != ""):
            st.write(f"**{column_name}**: {entry}")

    display_job_details('Job Title', selected_job['job_title'])
    selected_job['seniority_level'] = map_seniority_level(selected_job['level'])
    display_job_details('Seniority Level', selected_job['seniority_level'])
    display_job_details('Company Name', selected_job['company_name'])
    display_job_details('Industry', selected_job['company_industry'])
    display_job_details('Field', selected_job['field'])
    display_job_details('Required Skills', selected_job['skills'])
    display_job_details('Job Summary', selected_job['job_summary'])
    
    st.write(f"[Apply Here]({selected_job['apply_link']})")
    st.write(f"[Job Posting Link]({selected_job['post_link']})")

    # Button to start simulation
    if st.button("Simulate Interview"):
        # Retrieve top questions
        if selection_method == "Pick from List":
            top_code_questions = get_top_questions(selected_job['job_id'], code_questions_scores)
            top_open_questions = get_top_questions(selected_job['job_id'], open_questions_scores)

        # Randomly choose 2 questions from the top 20 of each type
        code_questions_to_ask = top_code_questions.sample(min(2, len(top_code_questions)))
        open_questions_to_ask = top_open_questions.sample(min(2, len(top_open_questions)))

        st.header("Practice Interview")

        st.subheader("Coding Questions")
        for index, row in code_questions_to_ask.iterrows():
            question = row['question']
            st.write(f"**{question}**")
            st.text_area(f"Your answer to coding question {index + 1}", key=f"code_q{index}")

        st.subheader("Open-Ended Questions")
        for index, row in open_questions_to_ask.iterrows():
            question = row['question']
            st.write(f"**{question}**")
            st.text_area(f"Your answer to open question {index + 1}", key=f"open_q{index}")

        # Simulate feedback (for future development, based on AI or heuristics)
        st.header("Simulation Feedback")
        if st.button("Submit and Get Feedback"):
            st.write("Feedback feature is under development. Stay tuned!")

if __name__ == "__main__":
    main()
