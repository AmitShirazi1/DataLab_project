import streamlit as st
import pandas as pd
import random
import os
import google.generativeai as genai
from api_keys import API_KEYS
from consts import JOBS_PATH, DATA_PATH

if __name__ == "__main__":
    st.set_page_config(page_title="Job Interview Simulator", page_icon="🧑‍💼", layout="wide")

# Custom CSS
st.markdown("""
<style>
    /* Global Styling */
    :root {
        --primary-color: #2c3e50;      /* Deep navy blue */
        --secondary-color: #3498db;    /* Bright blue */
        --accent-color: #2ecc71;       /* Soft green */
        --background-color: #f4f6f8;   /* Light gray-blue */
        --text-color: #2c3e50;         /* Dark gray */
    }

    /* Base App Styling */
    .stApp {
        background-color: var(--background-color);
        font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    }

    /* Title Styling */
    .stTitle {
        color: var(--primary-color);
        font-weight: 700;
        text-align: center;
        margin-bottom: 30px;
    }

    /* Button Styling */
    .stButton > button {
        background-color: var(--secondary-color);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .stButton > button:hover {
        background-color: var(--primary-color);
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }

    /* Card-like Containers */
    .stContainer {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }

    .stContainer:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 25px rgba(0,0,0,0.12);
    }

    /* Radio Button Styling */
    .stRadio > div {
        background-color: white;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Caching large dataframes for better performance
@st.cache_data
def load_jobs_sample():
    return pd.read_csv(os.path.join(JOBS_PATH, "jobs_sample.csv"))

@st.cache_data
def load_code_scores():
    return pd.read_csv(os.path.join(DATA_PATH, "top_code_questions.csv"))

@st.cache_data
def load_open_scores():
    return pd.read_csv(os.path.join(DATA_PATH, "top_open_questions.csv"))

@st.cache_data
def load_all_jobpostings():
    return pd.read_csv(os.path.join(JOBS_PATH, "all_jobpostings_with_skills.csv"))

# Load datasets
jobs_sample = load_jobs_sample()
code_questions_scores = load_code_scores()
open_questions_scores = load_open_scores()
all_jobpostings = load_all_jobpostings()

# Initialize session state variables
if "stage" not in st.session_state:
    st.session_state.stage = "selection_method"
if "selection_method" not in st.session_state:
    st.session_state.selection_method = None
if "selected_job" not in st.session_state:
    st.session_state.selected_job = None

# Callback functions for navigation
def next_stage(new_stage):
    st.session_state.stage = new_stage
    st.rerun()


def choose_selection_method():
    st.header("Choose a Job Selection Method")
        
    selection = st.radio(
        "How would you like to select the job?",
        ("Pick from List", f"Random Job ({all_jobpostings.shape[0]} options)"),
        key="selection_method"
    )

    if st.button("Next"):
        if st.session_state.selection_method == "Pick from List":
            next_stage("pick_from_list")
        elif st.session_state.selection_method == f"Random Job ({all_jobpostings.shape[0]} options)":
            next_stage("random_job")


def pick_from_list_of_jobs():
    st.header("Select a Job")

    # Ensure display_info column is correctly formatted
    jobs_sample["display_info"] = jobs_sample.apply(
        lambda row: f"{row['job_title'] if pd.notna(row['job_title']) else ''} | {row['company_name'] if pd.notna(row['company_name']) else ''}", axis=1
    )

    selected_index = st.radio(
        "Choose a job:", 
        list(jobs_sample.index),  # Ensure it's a list of indices
        format_func=lambda idx: jobs_sample["display_info"].iloc[idx],
        key="selected_job_index"
    )

    # Show selected job information but do not proceed automatically
    if "selected_job_index" in st.session_state and st.session_state.selected_job_index is not None:
        # Store job in session state but do not proceed yet
        st.session_state.selected_job = jobs_sample.loc[st.session_state.selected_job_index].copy()  # Use .copy() to avoid reference issues
    else:
        st.write("No valid job selected.")

    # Only proceed when user confirms
    if st.button("Confirm Selection"):
        if "selected_job" in st.session_state and st.session_state.selected_job_index is not None:
            next_stage("job_details")
        else:
            st.write("Please select a job before confirming.")


def pick_random_job():  
    # Randomly sample a job from all job postings
    st.session_state.selected_job = all_jobpostings.sample(1).iloc[0].copy()

    if st.button("Choose Random Job"):
        # TODO: Pick a random job from the dataset
        next_stage("job_details")


def display_job_details():
    """Displays selected job details and a button to proceed to the interview simulation."""
    st.header("Selected Job")
    selected_job = st.session_state.selected_job

    with st.expander("View Job Details"):
        for col in ["job_title", "company_name", "company_industry", "field", "skills", "job_summary"]:
            if col in selected_job and pd.notna(selected_job[col]):
                st.write(f"**{col.replace('_', ' ').title()}**: {selected_job[col]}")

    if st.button("Simulate Interview"):
        next_stage("simulation")


def map_seniority_level(level):
    mapping = {
        0: "Internship",
        1: "Entry level/Associate",
        2: "Mid-Senior level/Manager and above",
    }
    return mapping.get(int(level), "") if pd.notna(level) else ""


def get_open_questions(job):
    """Retrieve 3 random interview questions, ensuring at least one is 'General'."""
    
    # Initialize asked questions if not present in session state
    if "asked_open_questions" not in st.session_state:
        st.session_state.asked_open_questions = set()

    # Filter relevant questions for the selected job
    relevant_questions = open_questions_scores[
        open_questions_scores["job_id"] == job["job_id"]
    ]    
    # Remove already asked questions
    relevant_questions = relevant_questions[
        ~relevant_questions["question"].isin(st.session_state.asked_open_questions)
    ]
    
    if relevant_questions.empty:
        st.warning("No more available questions for this job.")
        return []

    # Ensure at least one question from 'General' category
    general_questions = relevant_questions[relevant_questions["category"] == "General"]
    selected_questions = []

    # Pick one 'General' question if available
    if not general_questions.empty:
        general_sample = general_questions.sample(1)
        selected_questions.append(general_sample.iloc[0])
        st.session_state.asked_open_questions.add(general_sample.iloc[0]["question"])  # Mark as used

    # Select remaining questions
    remaining_count = 3 - len(selected_questions)
    
    # Filter again to exclude already chosen questions
    remaining_questions = relevant_questions[
        ~relevant_questions["question"].isin(st.session_state.asked_open_questions)
    ]
    # If there are not enough remaining questions, take as many as possible
    remaining_questions_sample = remaining_questions.sample(min(remaining_count, len(remaining_questions)))

    for _, question in remaining_questions_sample.iterrows():
        selected_questions.append(question)
        st.session_state.asked_open_questions.add(question["question"])  # Mark as used

    return selected_questions


def get_code_questions(job):
    """Retrieve 2 random coding questions for the selected job."""
    
    if "asked_code_questions" not in st.session_state:
        st.session_state.asked_code_questions = set()

    # Filter relevant questions for the selected job
    relevant_code_questions = code_questions_scores[
        code_questions_scores["job_id"] == job["job_id"]
    ]
    # Remove already asked questions
    relevant_code_questions = relevant_code_questions[
        ~relevant_code_questions["question"].isin(st.session_state.asked_code_questions)
    ]
    
    if relevant_code_questions.empty:
        st.warning("No more coding questions available for this job.")
        return []

    # Randomly sample two coding questions
    selected_code_questions = relevant_code_questions.sample(min(2, len(relevant_code_questions)))

    for _, question in selected_code_questions.iterrows():
        st.session_state.asked_code_questions.add(question["question"])  # Mark as used

    return selected_code_questions.to_dict(orient="records")


def simulate_interview():
    """Displays one interview question at a time and progresses through open and coding questions."""
    st.header("Practice Interview")

    if "questions" not in st.session_state:
        st.session_state.questions = get_open_questions(st.session_state.selected_job)
        st.session_state.questions += get_code_questions(st.session_state.selected_job)  # Append coding questions
        st.session_state.current_question = 0
    
    questions = st.session_state.questions
    if "answers" not in st.session_state:
        st.session_state.answers = dict()

    if st.session_state.current_question < len(questions):
        question = questions[st.session_state.current_question]
        st.subheader(f"Question {st.session_state.current_question + 1}")

        # Check if it's a coding question (coding questions have a 'solution' field)
        is_coding_question = "solution" in question

        st.write(question["question"])        
        user_answer = st.text_area("Your Answer", key=f"answer_{st.session_state.current_question}")
        st.session_state.answers[st.session_state.current_question] = user_answer

        if st.button("Next"):
            st.session_state.current_question += 1
            st.rerun()

    else:
        st.success("Interview completed! Click below to evaluate your answers.")
        if st.button("Evaluate Answers"):
            next_stage("evaluation")


def gemini_evaluation(question, is_coding, user_answer):
    success = False  # Flag to indicate if evaluation was successful or the APIs are exhausted
    for api_key in API_KEYS.values():
        os.environ['GOOGLE_API_KEY'] = api_key
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
        model = genai.GenerativeModel('gemini-1.5-flash')

        if is_coding:
            solution = question["solution"]
            prompt = f"""
                The user has submitted a code solution to a programming question. Your task is to analyze and evaluate the code, considering both correctness and the quality of the approach. Even if the code has syntax errors or does not compile, partial credit should be awarded if the logic or idea is sound. 

                Evaluation Criteria:
                - Correctness - Does the code produce the expected output for all cases? Is it written in the required programming language (if specified)?
                - Functionality - Does the code correctly solve the problem?
                - Efficiency - If there are complexity constraints, is the code optimized in terms of time and space complexity?
                - Readability & Best Practices - Is the code well-structured, using meaningful variable names and following coding standards?
                - Edge Case Handling - Does the solution consider different edge cases, such as empty inputs, extreme values, or invalid data?
                - Logical Soundness (For Non-Compiling Code/Pseudocode) - Even if the code contains syntax errors or is in pseudocode, does it show a clear and correct approach to solving the problem?

                Scoring Guidelines:
                Assign a score between 0 and 100 based on the above criteria. 0 = An entirely incorrect or non-functional solution with no meaningful approach. 100 = A fully correct, efficient (if needed), and well-structured solution. Provide the feedback in the following format: The score in a 'x/100' format, where 'x' is a number between 0 and 100 that represents the score, then a newline, then the feedback message.

                Example Evaluations:
                Example 1: Fully Correct Code.
                Question: Write a Python function that returns the factorial of a number.
                User's Code: 
                    def factorial(n):
                        if not isinstance(n, int) or n < 0:
                            raise ValueError('Input must be a non-negative integer')
                        result = 1
                        for i in range(2, n + 1):
                            result *= i
                        return result
                Output: 100/100\nCorrect, handles all cases including invalid input. Efficient (iterative approach avoids recursion depth issues). Readable and follows best practices.

                Now, evaluate the following coding solution:

                Question: {question}
                User's Code: 
                {user_answer}

                Java Solution: {solution if solution else 'Not provided'}

                If the Java solution is provided, check if the user's solution is correct by comparing it to the Java solution. Provide feedback based on correctness, efficiency, readability, edge cases, and logical soundness. Assign a score accordingly, giving partial credit for a good idea even if the code does not compile.
            """
        else:
            prompt = f"""
                The user has provided an answer to an open-ended question. Your task is to evaluate their response based on the following criteria:
                - Relevance & Completeness - Does the answer directly address the question and cover all key aspects?
                - Clarity & Coherence - Is the response well-structured, logically presented, and easy to understand?
                - Accuracy (for factual questions) or Depth & Justification (for subjective questions). If the question is factual, does the answer provide correct and well-supported information?, If the question is subjective, does the response demonstrate thoughtful reasoning, realistic insights, and a well-supported argument?
                - Balance & Perspective (for subjective questions) - Does the response consider different viewpoints or provide a well-rounded perspective?.
                
                Scoring: Assign a score between 0 and 100 based on the criteria above. 0 means the answer is entirely incorrect, off-topic, or lacks coherence. 100 means the response is fully relevant, well-articulated, and appropriately detailed.
                Provide the feedback in the following format: The score in a 'x/100' format, where 'x' is a number between 0 and 100 that represents the score, then a newline, then the feedback message.
                
                Examples:
                Example 1: Factual Question.
                Question: What are the key benefits of cloud computing?.
                User's Answer: Cloud computing makes things faster and better.
                Ideal Answer: Cloud computing provides scalability, cost efficiency, remote accessibility, and security improvements. Businesses benefit from reduced infrastructure costs and improved collaboration.
                Feedback:
                50/100
                Strengths: The answer hints at benefits but lacks specifics.
                Improvements: More details on specific advantages like scalability and cost savings would improve clarity.
                
                Example 2: Subjective Question.
                Question: Where do you see yourself in 5 years professionally?.
                User's Answer: I want to have a good job and be successful.
                Ideal Answer: In five years, I aim to become a project manager in the tech industry, leading cross-functional teams. To prepare, I plan to gain experience in team management, obtain a PMP certification, and refine my leadership skills.
                Feedback:
                60/100
                Strengths: The answer shows ambition.
                Improvements: It lacks specificity regarding career path and steps to achieve success.
                
                Now, evaluate the following response:
                Question:
                {question}

                User's Answer:
                {user_answer}
                
                Provide constructive feedback and assign a score based on clarity, completeness, reasoning, and relevance.
                """
        try:
            response = model.generate_content(prompt)
            evaluation = response.text.strip()
            if not evaluation[0].isdigit():
                raise Exception("Invalid response.")
            st.write(f"**Evaluation:** {evaluation}")
            success = True
            break
        except Exception as e:
            print(f"Error: {e}")
            success = False
            continue

    return success


def evaluate_answers():
    """Evaluates user answers using direct matching for code and Gemini API for open-ended responses."""
    st.subheader("Evaluation Results")
    
    questions = st.session_state.questions
    answers = st.session_state.answers
    prompt = ""

    for idx, question in enumerate(questions):
        user_answer = answers.get(idx, "").strip()
        is_coding = "solution" in question
        st.write(f"**Question {idx+1}:** {question['question']}")
        st.write(f"**Your Answer:** {user_answer}")

        success = False
        while not success:
            success = gemini_evaluation(question, is_coding, user_answer)

    st.subheader("Would you like to give us feedback?")
    if st.button("Feedback form"):
        next_stage("feedback")
        st.rerun()


def feedback_form():
    st.subheader("Feedback Form")
    st.write("We appreciate your feedback! Please answer the following questions:")
    
    quality = st.radio("How would you rate the overall quality of the interview simulation?", ["Excellent", "Good", "Average", "Poor"], index=1)
    relevance = st.radio("How relevant were the questions to the job posting? (1-5)", ["1", "2", "3", "4", "5"], index=2)
    alignment = st.radio("How well did the AI-based simulator align with the real-world interview process?", ["Not aligned", "Somewhat aligned", "Well aligned", "Perfectly aligned"], index=1)
    evaluation_quality = st.radio("How would you rate the quality of the AI's evaluation on your answers?", ["Excellent", "Good", "Average", "Poor"], index=1)
    feedback_accuracy = st.radio("Did the AI feedback provide valuable insights for improvement?", ["Yes", "No", "Somewhat"], index=2)
    use_again = st.radio("Would you use this simulator again for future job interviews?", ["Yes", "No", "Maybe"], index=2)
    suggestions = st.text_area("Do you have any additional comments or suggestions for improving the interview simulator?")
    
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")
        st.session_state.stage = "completed"
        st.rerun()


def main():
    st.title("Job Interview Simulator")

    if "selected_job" not in st.session_state:
        st.session_state.selected_job = None  # or a default value like {}
    
    if st.session_state.stage == "selection_method":
        choose_selection_method()

    if st.session_state.stage == "pick_from_list":
        pick_from_list_of_jobs()

    if st.session_state.stage == "random_job":
        pick_random_job()

    if st.session_state.stage == "job_details":
        display_job_details()

    if st.session_state.stage == "simulation":
        simulate_interview()
    
    if st.session_state.stage == "evaluation":
        evaluate_answers()
    
    if st.session_state.stage == "feedback":
        feedback_form()

    if st.session_state.stage == "completed":
        st.write("Interview process completed. Thank you for participating!")


if __name__ == "__main__":
    main()
