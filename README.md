# Job Interview Simulator for LinkedIn Users

## Overview
The Job Interview Simulator is an intelligent system designed to enhance interview preparation by optimally matching interview questions to job positions. It provides:
- A **job interview simulator** that selects tailored open-ended and coding questions.
- A **personality test simulator** that evaluates the user's personality traits.
- AI-driven scoring and feedback on user responses.

## Table of Contents
1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Project Structure](#project-structure)
5. [Data Collection](#data-collection)
6. [Methodologies](#methodologies)
7. [Evaluation](#evaluation)
8. [Limitations & Future Work](#limitations--future-work)

---

## Features
- **Job Interview Simulation**: Selects a job, presents relevant interview questions, evaluates responses, and provides feedback.
- **Personality Test Simulation**: 120-question assessment based on the OCEAN model, with graphical and textual results.
- **AI-Based Evaluation**: Uses the Gemini API to assess answer quality and job-question relevance.
- **Data-Driven Question Selection**: Heuristic scoring for optimal job-question matching.

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
   python home_page_app.py
   ```
2. Navigate to the Job Interview or Personality Test app.
3. Follow the instructions to complete the simulation and receive feedback.

## Project Structure
```
📂 job-interview-simulator
├── 📂 data                      # Contains all datasets (collected and generated)
├── 📂 requirements              # Requirement files for installation
│   ├── app_requirements.txt     # Dependencies for running the app
│   ├── requirements.txt         # Dependencies for full development
├── answer_questions.ipynb       # Uses Gemini API for simulated user responses & evaluation
├── calculate_heuristic_score.py # Calculates similarity scores for question-job pairs
├── consts.py                    # Project constants
├── evaluate_answers.ipynb       # AI evaluation of user responses
├── home_page_app.py             # Homepage for navigating between apps
├── job_interview_simulator_app.py # Interview simulator app
├── personality_test_app.py      # Personality test app
├── personality_test_nb.py       # Example personality test
├── scraping_websites.py         # Scrapes LeetCode for interview questions
├── select_interview_questions.ipynb # Preprocesses data & selects best questions
├── unify_datasets.ipynb         # Unifies datasets from multiple sources
├── visualizations.ipynb         # Exploratory data analysis (EDA) visualizations
└── visualize_similarities&heuristics.ipynb # Heuristic score analysis
```

## Data Collection
We compiled datasets from various sources:
- **Coding Questions**: Scraped from LeetCode.
- **Job Postings**: Collected from Kaggle and contributions from our peers.
- **Open Questions**: Gathered from Glassdoor articles.
- **Personality Test**: Based on the IPIP-NEO-120 dataset.

## Methodologies
### Question-Job Matching
- **Topics-Skills Similarity**: Used SentenceTransformer embeddings and cosine similarity.
- **Difficulty Alignment**: Mapped job seniority to coding question difficulty.
- **Acceptance Normalization**: Normalized question popularity to prioritize widely used questions.

### AI-Driven Evaluation
- **Gemini API**: Scores job-question relevance and evaluates user responses.
- **Embedding Transformations**: Applied transformations for better differentiation.
- **Personality Assessment**: Evaluates responses based on OCEAN model.

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
- **[Your Team Name]**


