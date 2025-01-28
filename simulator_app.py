import streamlit as st
import pandas as pd
import random
import os
from consts import JOBS_PATH

# Load datasets
all_jobpostings = pd.read_csv(os.path.join(JOBS_PATH, "all_jobpostings_with_skills.csv"))
jobs_questions_scores = pd.read_csv(os.path.join(DATA_PATH, "jobs_questions_scores.csv"))

def get_top_questions(job_id, dataset, top_n=20):
    """Get the top N questions for a specific job ID from a dataset."""
    filtered_questions = dataset[dataset['job_id'] == job_id]
    sorted_questions = filtered_questions.sort_values(by='score', ascending=False)
    return sorted_questions.head(top_n)

def remove_job_occurrences(job_id, datasets):
    """Remove all occurrences of a job ID from the provided datasets."""
    for dataset in datasets:
        dataset.drop(dataset[dataset['job_id'] == job_id].index, inplace=True)

def main():
    st.title("Job Interview Simulator")

    # Random Job Selection
    st.header("Selected Job")
    selected_job = all_jobpostings.sample(1).iloc[0]

    # Display job details
    def display_job_details(column_name, entry):
        if entry and (entry != ""):
            st.write(f"**{column_name}**: {entry}")

    display_job_details('Job Title', selected_job['job_title'])
    display_job_details('Seniority Level', selected_job['level'])
    display_job_details('Company Name', selected_job['company_name'])
    display_job_details('Industry', selected_job['company_industry'])
    display_job_details('Field', selected_job['field'])
    display_job_details('Required Skills', selected_job['required_skills'])
    display_job_details('Job Summary', selected_job['job_summary'])
    
    st.write(f"[Apply Here]({selected_job['apply_link']})")
    st.write(f"[Job Posting Link]({selected_job['post_link']})")

    # Button to start simulation
    if st.button("Simulate Interview"):
        job_id = selected_job['job_id']

        # Remove occurrences of the selected job
        remove_job_occurrences(job_id, [code_questions, open_questions])

        # Retrieve top questions
        top_code_questions = get_top_questions(job_id, code_questions)
        top_open_questions = get_top_questions(job_id, open_questions)

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
