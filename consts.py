import os
import pandas as pd

# Define paths
PROJECT_PATH = os.getcwd()
DATA_PATH = os.path.join(PROJECT_PATH, "data/")
QUESTIONS_PATH = os.path.join(DATA_PATH, "questions_and_answers/")
JOBS_PATH = os.path.join(DATA_PATH, "jobs/")

# Using pandas and spark to open and read csv files.
def open_csv_file(spark, file_dir, file_name):
    file_path = os.path.join(file_dir, file_name)
    df = pd.read_csv(file_path)
    df = spark.createDataFrame(df)
    return df