# Data Folder README

## Overview
The `data` folder contains all datasets used in the **Job Interview Simulator** project. It includes raw data collected from external sources, processed datasets, and intermediate calculation files for analysis. This document provides an overview of the folder structure and the contents of each subfolder.

---

## Folder Structure

### 1. `gemini_simulation/`
Contains datasets generated when simulating user interactions with the **Gemini API**. The AI was used to generate responses to questions, evaluate answers, and assign scores to question-job pairs.

- **`code_answers_evaluation.csv`** – Evaluations of coding question answers.
- **`open_answers_evaluation.csv`** – Evaluations of open-ended question answers.
- **`code_questions_answers.csv`** – AI-generated answers to coding questions.
- **`open_questions_answers.csv`** – AI-generated answers to open-ended questions.
- **`code_questions_feedback.csv`** – Ground truth scores assigned by Gemini to coding question-job pairs.
- **`open_questions_feedback.csv`** – Ground truth scores assigned by Gemini to open-ended question-job pairs.

---

### 2. `jobs/`
Contains datasets related to job postings. It includes raw job postings from various sources and unified datasets.

#### **Raw Job Postings:**
- **`job_descriptions_and_skills.csv`** – Jobs with required skills (Source: [Kaggle](https://www.kaggle.com/datasets/batuhanmutlu/job-skill-set)).
- **`linkedin_hightech_jobs.csv`** – Job postings collected by Itamar Shashar.
- **`indeed_jobs.csv`** – Job postings collected by Itamar Shashar.
- **`glassdoor_data_jobs_and_company_info.csv`** – Job postings related to the data field (Source: collected by Sergiy Horef from [GitHub](https://github.com/Deff-ux/Scrapping-Glassdoor-Job-Posting-)).
- **`linkedin_data_jobs.csv`** – Job postings for data and software fields (Source: collected by Sergiy Horef from [GitHub](https://github.com/Mlawrence95/LinkedIn-Tech-Job-Data)).

#### **Processed Job Postings:**
- **`all_jobpostings.csv`** – Unified dataset of job postings with key attributes.
- **`all_jobpostings_with_skills.csv`** – Same as above, but missing skill values were inferred using Gemini.

---

### 3. `mid_calculation/`
Stores intermediate datasets used for computations and analysis.

- **`code_questions_exploded.csv`** – Coding questions with their topics column exploded.
- **`open_questions_exploded.csv`** – Open-ended questions with their topics column exploded.
- **`code_questions_similarity.csv`** – Similarity scores for coding question-job pairs.
- **`open_questions_similarity.csv`** – Similarity scores for open-ended question-job pairs.
- **`code_questions_transformed_similarity.csv`** – Transformed similarity scores for coding questions.
- **`open_questions_transformed_similarity.csv`** – Transformed similarity scores for open-ended questions.
- **`unique_topics_code.csv`** – Unique topic-skill pairs for coding questions.
- **`unique_topics_open.csv`** – Unique topic-skill pairs for open-ended questions.

---

### 4. `questions_and_answers/`
Contains datasets of interview questions and answers, including coding questions, open-ended questions, and personality test data.

#### **Personality Test Data:**
- **`OCEAN_test/`** – Big Five Personality Test data (Sources: [GitHub](https://github.com/rubynor/bigfive-web) and [123Test](https://www.123test.com/personality-test/)).

#### **Raw Coding Questions:**
- **`leetcode_problems&solutions_links.csv`** – LeetCode problems with links (Source: [GitHub](https://github.com/hxu296/leetcode-company-wise-problems-2022/blob/main/data/leetcode_problems.csv)).
- **`leetcode_problems_data.csv`** – LeetCode problem details and content (Source: scraped by us).
- **`leetcode_problems_metadata.csv`** – Metadata about LeetCode problems (Source: [Kaggle](https://www.kaggle.com/datasets/jaydeepagravat94583/leetcode?resource=download)).

#### **Raw Open-Ended Questions:**
- **`open_questions_data_science.csv`** – Data science interview questions (Source: [Kaggle](https://www.kaggle.com/datasets/sandy1811/data-science-interview-questions)).
- **`general_open_questions.csv`** – Common interview questions (Source: [Glassdoor](https://www.glassdoor.com/blog/common-interview-questions/)).

#### **Processed Questions and Answers:**
- **`all_code_problems_with_solutions.csv`** – Unified dataset of coding problems and solutions (Solutions source:[GitHub](https://github.com/fishercoder1534/Leetcode/tree/master/src/main/java/com/fishercoder/solutions).
- **`all_open_questions.csv`** – Unified dataset of open-ended questions.
- **`all_code_questions_with_topics.csv`** – Coding questions with topics inferred using Gemini to replace missing topics values.
- **`all_open_questions_with_topics.csv`** – Open-ended questions with topic assignments inferred using Gemini.

---

### 5. **Top Scoring Questions**
- **`top_code_questions.csv`** – Top 50 jobs with their 20 best-scoring coding questions, according to the heuristic.
- **`top_open_questions.csv`** – Top 50 jobs with their 20 best-scoring open-ended questions, according to the heuristic.

These files are used in the simulator app to present a job selection interface where users pick a job, and relevant questions are randomly chosen from these datasets.

---

## Notes
- The datasets have been collected from publicly available sources and proprietary scraping efforts.
- Processed datasets were enriched using **Gemini API** for skills and topics inference and heuristic scoring.
- Intermediate calculation files provide transparency for debugging and improving the model.

This README serves as a reference for understanding the data used in the **Job Interview Simulator** project. If you have any questions, please refer to the source links or contact the project contributors.

---
