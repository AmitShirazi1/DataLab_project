import streamlit as st
import pandas as pd
import random
import os
from consts import JOBS_PATH, DATA_PATH

# Caching large dataframes for better performance
@st.cache_data
def load_jobs_sample():
    return pd.read_csv(os.path.join(JOBS_PATH, "jobs_sample.csv"))

@st.cache_data
def load_code_scores():
    return pd.read_csv(os.path.join(DATA_PATH, "code_scores.csv"))

@st.cache_data
def load_open_scores():
    return pd.read_csv(os.path.join(DATA_PATH, "open_scores.csv"))

@st.cache_data
def load_all_jobpostings():
    return pd.read_csv(os.path.join(JOBS_PATH, "all_jobpostings_with_skills.csv"))

# Load datasets
jobs_sample = load_jobs_sample()
code_questions_scores = load_code_scores()
open_questions_scores = load_open_scores()
all_jobpostings = load_all_jobpostings()


def get_top_questions(job, dataset, top_n=20):
    """Get the top N questions for a specific job ID from a dataset."""
    job_cols = [col for col in job.index if col in dataset.columns and col not in ["seniority_level", "display_info"]]
    filtered_questions = dataset
    for column in job_cols:
        if not pd.isna(job[column]):
            filtered_questions = filtered_questions[filtered_questions[column] == job[column]]
    sorted_questions = filtered_questions.sort_values(by="avg(similarity)", ascending=False)
    return sorted_questions.head(top_n)


def map_seniority_level(level):
    """Map level integers to seniority descriptions, handling NaN values."""
    mapping = {
        0: "Internship",
        1: "Entry level/Associate",
        2: "Mid-Senior level/Manager and above",
    }
    return mapping.get(int(level), "") if pd.notna(level) else ""


def main():
    st.title("Job Interview Simulator")

    # Job Selection Method
    st.header("Choose a Job Selection Method")
    selection_method = st.radio(
        "How would you like to select the job?",
        ("Pick from List", f"Random Job ({all_jobpostings.shape[0]} options)"),
    )

    if selection_method == "Pick from List":
        st.header("Select a Job")
        jobs_sample["seniority_level"] = jobs_sample["level"].apply(map_seniority_level)
        jobs_sample["display_info"] = jobs_sample.apply(
            lambda row: f"{row['job_title']} | {row['seniority_level']} | {row['company_name']}", axis=1
        )
        selected_job_row = st.radio(
            "Choose a job:", jobs_sample["display_info"].index, format_func=lambda idx: jobs_sample["display_info"].iloc[idx]
        )
        selected_job = jobs_sample.loc[selected_job_row]
    else:
        st.header("Randomly Selected Job")
        selected_job = all_jobpostings.sample(1).iloc[0]

    # Display job details
    st.header("Selected Job")
    with st.expander("View Job Details"):
        def display_job_details(column_name, entry):
            if entry and entry != "":
                st.write(f"**{column_name}**: {entry}")

        display_job_details("Job Title", selected_job.get("job_title", "N/A"))
        selected_job["seniority_level"] = map_seniority_level(selected_job.get("level", None))
        display_job_details("Seniority Level", selected_job["seniority_level"])
        display_job_details("Company Name", selected_job.get("company_name", "N/A"))
        display_job_details("Industry", selected_job.get("company_industry", "N/A"))
        display_job_details("Field", selected_job.get("field", "N/A"))
        display_job_details("Required Skills", selected_job.get("skills", "N/A"))
        display_job_details("Job Summary", selected_job.get("job_summary", "N/A"))

        apply_link = selected_job.get("apply_link", "")
        post_link = selected_job.get("post_link", "")
        if apply_link:
            st.write(f"[Apply Here]({apply_link})")
        if post_link:
            st.write(f"[Job Posting Link]({post_link})")

    # Button to start simulation
    if st.button("Simulate Interview"):
        # Retrieve top questions
        if selection_method == "Pick from List":
            top_code_questions = get_top_questions(selected_job, code_questions_scores)
            top_open_questions = get_top_questions(selected_job, open_questions_scores)
        else:
            top_code_questions = code_questions_scores
            top_open_questions = open_questions_scores

        # Randomly choose 2 questions from the top 20 of each type
        num_code_questions = min(2, len(top_code_questions))
        num_open_questions = min(2, len(top_open_questions))
        code_questions_to_ask = top_code_questions.sample(num_code_questions) if num_code_questions > 0 else pd.DataFrame()
        open_questions_to_ask = top_open_questions.sample(num_open_questions) if num_open_questions > 0 else pd.DataFrame()

        st.header("Practice Interview")

        st.subheader("Coding Questions")
        for index, row in code_questions_to_ask.iterrows():
            question = row.get("question", "No question available")
            st.write(f"**{question}**")
            st.text_area(f"Your answer to coding question {index + 1}", key=f"code_q{index}")

        st.subheader("Open-Ended Questions")
        for index, row in open_questions_to_ask.iterrows():
            question = row.get("question", "No question available")
            st.write(f"**{question}**")
            st.text_area(f"Your answer to open question {index + 1}", key=f"open_q{index}")

        # Simulate feedback (for future development, based on AI or heuristics)
        st.header("Simulation Feedback")
        if st.button("Submit and Get Feedback"):
            st.write("Feedback feature is under development. Stay tuned!")


if __name__ == "__main__":
    main()
