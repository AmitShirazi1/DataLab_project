# Job Interview Simulator for LinkedIn Users  

## Overview  
The **Job Interview Simulator** is an intelligent system designed to enhance interview preparation by optimally matching interview questions to job positions. It offers:  
- A **job interview simulator** that selects tailored open-ended and coding questions.  
- A **personality test simulator** that evaluates users' personality traits.  
- AI-driven scoring and feedback on user responses.  

## Table of Contents  
1. [Features](#features)  
2. [Project Structure](#project-structure)  
   - [Folder Descriptions](#folder-descriptions)  
   - [File Descriptions](#file-descriptions)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [Data Collection](#data-collection)  
6. [Methodology](#methodology)  
7. [Evaluation](#evaluation)  
8. [Limitations & Future Work](#limitations--future-work)  
9. [Contributors](#contributors)  

---  

## Features  
- **Job Interview Simulation**: Allows users to select a job, receive relevant interview questions, submit responses, and receive feedback.  
- **Personality Test Simulation**: A 120-question assessment based on the OCEAN model, providing both graphical and textual personality insights.  
- **AI-Based Evaluation**: Uses the Gemini API to assess the quality of answers and the relevance of job-question pairings.  
- **Data-Driven Question Selection**: Implements heuristic scoring to optimize question-job matching.  

## Project Structure  
The root directory contains the following files and folders:  

### Folder Descriptions  
- **`data/`**: Contains all datasets, including both collected and generated data (see the folder's separate README for details).  
- **`requirements/`**: Holds dependency files:  
  - `app_requirements.txt`: Lists dependencies required to run the app.  
  - `requirements.txt`: Lists dependencies required for development.  

### File Descriptions  
- **`answer_questions.ipynb`**: Uses the Gemini API to simulate user responses to interview questions, evaluate model performance, and compare predicted scores against Gemini’s true labels.  
- **`calculate_heuristic_score.py`**: Computes similarity scores between topics and skills for each question-job pair.  
- **`consts.py`**: Defines constant values used across the project.  
- **`evaluate_answers.ipynb`**: Uses an alternative version of the Gemini model to assess user responses, providing scores and feedback.  
- **`home_page_app.py`**: The main application that serves as the entry point, linking to both the job simulator and personality test apps.  
- **`job_interview_simulator_app.py`**: Implements the job interview simulator, guiding users through job selection, answering interview questions, and receiving feedback.  
- **`personality_test_app.py`**: Implements the personality test simulator, presenting users with 120 personality-related questions and generating analytical results.  
- **`personality_test_nb.py`**: Provides an example personality test.  
- **`scraping_websites.py`**: Scrapes LeetCode for interview questions, capturing attributes such as topics and acceptance.  
- **`select_interview_questions.ipynb`**: Processes datasets by filling in missing values using the Gemini API, calculating heuristic scores, and selecting the top 20 question-job pairs.  
- **`unify_datasets.ipynb`**: Merges multiple collected datasets into three unified datasets: job postings, coding questions with solutions, and open-ended questions.  
- **`visualizations.ipynb`**: Conducts exploratory data analysis (EDA) and visualizes dataset insights.  
- **`visualize_similarities&heuristics.ipynb`**: Analyzes and visualizes heuristic scores, exploring potential transformations to enhance data distribution and representation.  

## Installation  

### Prerequisites  
- Python 3.8+
- Required libraries (install using pip):  
  ```sh
  pip install -r requirements/app_requirements.txt  # For running the app  
  pip install -r requirements/requirements.txt  # For development  
  ```
- Gemini API Setup:
  1. Create a file named api_keys.py in the root directory
  2. In this file, create a dictionary named API_KEYS with your Gemini API keys as values:
     ```sh
     API_KEYS = {
       "first_key": "<your api key>",
       "second_key": "<another api key>"
     }
     ```

## Usage  

### Running the Application  
1. Start the homepage app:  
   ```sh
   streamlit run home_page_app.py
   ```  
2. Navigate to either the **Job Interview Simulator** or **Personality Test** app.  
3. Follow the on-screen instructions to complete the simulation and receive feedback.  

## Data Collection  
We compiled datasets from multiple sources:  
- **Coding Questions**: Scraped from LeetCode.  
- **Job Postings**: Collected from Kaggle and additional peer contributions.  
- **Open-Ended Questions**: Gathered from Glassdoor articles.  
- **Personality Test**: Based on the **IPIP-NEO-120** dataset.  

## Methodology  
The project employs AI-based techniques, including:  
- **Sentence embeddings** via `SentenceTransformer` for job-question matching.  
- **Cosine similarity** to measure skill-topic relevance.  
- **Weighted heuristic scoring** to rank the most suitable questions for each job.  
- **Data imputation** using the Gemini API to handle missing values.  
- **Personality evaluation** based on the **IPIP-NEO-120** model.  
- **AI-assisted answer scoring** with Gemini API.  

## Evaluation  
To assess the effectiveness of our heuristic scoring, we compared its results to Gemini’s evaluations:  

| Metric    | Code Questions | Open Questions |  
|-----------|---------------|---------------|  
| **MSE**  | 0.0259        | 0.0398        |  
| **MAE**  | 0.115         | 0.1571        |  
| **RMSE** | 0.161         | 0.1994        |  
| **Spearman** | 0.3953  | 0.3825  |  
| **Pearson**  | 0.2882  | 0.3898  |  

Additionally, we validated the interview simulation by having Gemini generate and evaluate responses.  

## Limitations & Future Work  
### Current Limitations  
- **Data Quality**: Some job postings lacked sufficient details.  
- **Resource Constraints**: Running advanced models required substantial computational resources.  
- **Model Limitations**: AI-generated scores occasionally exhibited inconsistencies.  

### Future Improvements  
- Expanding datasets to improve accuracy and coverage.  
- Refining heuristic scoring techniques.  
- Optimizing computational efficiency for faster performance.  

---

## Contributors  
- **Amit Shirazi**  
- **Hadar Etzion**  
- **Tomer Baruch**  
