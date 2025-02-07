# Job Interview Simulator for LinkedIn Users

## Overview
The Job Interview Simulator is an intelligent system designed to enhance interview preparation by optimally matching interview questions to job positions. It provides:
- A **job interview simulator** that selects tailored open-ended and coding questions.
- A **personality test simulator** that evaluates the user's personality traits.
- AI-driven scoring and feedback on user responses.

## Table of Contents
1. [Features](#features)
2. [Project Structure](#project-structure)
   - [Folder descriptions](#folder-descriptions)
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
- **Job Interview Simulation**: Selects a job, presents relevant interview questions, evaluates responses, and provides feedback.
- **Personality Test Simulation**: 120-question assessment based on the OCEAN model, with graphical and textual results.
- **AI-Based Evaluation**: Uses the Gemini API to assess answer quality and job-question relevance.
- **Data-Driven Question Selection**: Heuristic scoring for optimal job-question matching.

## Project Structure
The root directory contains the following files and folders:

### Folder descriptions
- **`data/`**: Contains all datasets, including collected and created ones (see the folder's separate README).
- **`requirements/`**: Contains dependency files:
  - `app_requirements.txt`: Requirements for running the app as a user.
  - `requirements.txt`: Requirements for running all project files as a developer.

### File Descriptions
- **`answer_questions.ipynb`**: Uses Gemini API to simulate user responses to interview questions, evaluates the model, and compares predicted scores to Gemini’s true labels.
- **`calculate_heuristic_score.py`**: Computes topics-skills similarity scores for each question-job pair.
- **`consts.py`**: Stores constant values used throughout the project.
- **`evaluate_answers.ipynb`**: Uses a different version of Gemini to evaluate user answers, providing scores and feedback.
- **`home_page_app.py`**: The main homepage application that links to the job simulator and personality test apps.
- **`job_interview_simulator_app.py`**: Implements the job interview simulator, guiding users through job selection, answering interview questions, and receiving feedback.
- **`personality_test_app.py`**: Implements the personality test simulator, presenting users with 120 personality questions and generating a graphical and textual personality assessment.
- **`personality_test_nb.py`**: Provides an example personality test.
- **`scraping_websites.py`**: Scrapes LeetCode for interview questions, including attributes like topics and acceptance rates.
- **`select_interview_questions.ipynb`**: Processes datasets by filling missing values using Gemini API, calculating heuristic scores, and selecting the top 20 question-job pairs.
- **`unify_datasets.ipynb`**: Merges collected datasets into three unified datasets: job postings, coding questions with solutions, and open questions.
- **`visualizations.ipynb`**: Conducts exploratory data analysis (EDA) and visualizes the datasets.
- **`visualize_similarities&heuristics.ipynb`**: Visualizes and analyzes heuristic scores, exploring transformations for better distribution and representation.

## Installation
### Prerequisites
- Python 3.8+
- Required libraries (install using pip):
  ```sh
  pip install -r requirements/app_requirements.txt  # For running the app
  pip install -r requirements/requirements.txt  # For development
  ```

## Usage
### Running the Application
1. Start the homepage app:
   ```sh
   streamlit run home_page_app.py
   ```
2. Navigate to the Job Interview or Personality Test app.
3. Follow the instructions to complete the simulation and receive feedback.

## Data Collection
We compiled datasets from various sources:
- **Coding Questions**: Scraped from LeetCode.
- **Job Postings**: Collected from Kaggle and contributions from our peers.
- **Open Questions**: Gathered from Glassdoor articles.
- **Personality Test**: Based on the IPIP-NEO-120 dataset.

## Methodology
The project uses AI-based methodologies, including:
- **Sentence embeddings** with `SentenceTransformer` for job-question matching.
- **Cosine similarity** to compute skill-topic relevance.
- **Weighted heuristic scoring** to rank questions for each job.
- **Data imputation** via Gemini API to fill missing values.
- **Personality evaluation** using the `IPIP-NEO-120` model.
- **AI-assisted answer scoring** using Gemini API.

## Evaluation
Our heuristic scores were compared to Gemini’s evaluations:
| Metric    | Code Questions | Open Questions |
|-----------|---------------|---------------|
| **MSE**  | 0.0259        | 0.0398        |
| **MAE**  | 0.115         | 0.1571        |
| **RMSE** | 0.161         | 0.1994        |
| **Spearman** | 0.3953  | 0.3825  |
| **Pearson**  | 0.2882  | 0.3898  |

Additionally, we validated the interview simulation by having Gemini generate and evaluate answers.

## Limitations & Future Work
- **Data Quality**: Some job postings lacked details.
- **Resource Constraints**: Running advanced models required significant computational resources.
- **Model Limitations**: AI-generated scores occasionally lacked precision.

Future improvements include expanding datasets, refining heuristics, and optimizing computational efficiency.

---
### Contributors
- **Amit Shirazi**
- **Hadar Etzion**
- **Tomer Baruch**


