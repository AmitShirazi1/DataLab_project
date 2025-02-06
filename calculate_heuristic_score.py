from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, lit, udf, array, broadcast, trim, lower, avg
from pyspark.sql.types import ArrayType, FloatType, DoubleType
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from consts import DATA_PATH, QUESTIONS_PATH, MID_CALC_PATH, open_csv_file


def topics_skills_similarity(jobs, spark):
    """
    Calculate the similarity between job skills and question topics using embeddings and cosine similarity.

    Args:
        jobs (DataFrame): Spark DataFrame containing job data with a 'skills' column.
        spark (SparkSession): Spark session object.

    Returns:
        tuple: Two Spark DataFrames containing the aggregated similarity scores for code and open questions.
    """
    jobs_exploded = jobs.withColumn(
        "skill", explode(split(col("skills"), ",\\s*"))
    )
    code_questions_exploded = open_csv_file(spark, MID_CALC_PATH, "code_questions_exploded.csv")
    open_questions_exploded = open_csv_file(spark, MID_CALC_PATH, "open_questions_exploded.csv")

    # Collect unique skills and topics for embedding
    unique_skills = [row["skill"] for row in jobs_exploded.select("skill").distinct().collect()]
    unique_code_topics = [row["topic"] for row in code_questions_exploded.select("topic").distinct().collect()]
    unique_open_topics = [row["topic"] for row in open_questions_exploded.select("topic").distinct().collect()]

    # Generate embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    skills_embeddings = model.encode(unique_skills)
    code_topics_with_embeddings = model.encode(unique_code_topics)
    open_topics_with_embeddings = model.encode(unique_open_topics)

    # Compute similarity
    skills_df = pd.DataFrame({"unique_skill": unique_skills, "embedding": list(skills_embeddings)})
    code_topics_df = pd.DataFrame({"unique_topic": unique_code_topics, "embedding": list(code_topics_with_embeddings)})
    open_topics_df = pd.DataFrame({"unique_topic": unique_open_topics, "embedding": list(open_topics_with_embeddings)})

    # Calculate similarity scores
    def calculate_similarity(topics_df, skills_df):
        similarity_records = []
        for _, topic_row in topics_df.iterrows():
            for _, skill_row in skills_df.iterrows():
                score = float(cosine_similarity([topic_row["embedding"]], [skill_row["embedding"]])[0][0])
                similarity_records.append((topic_row["unique_topic"], skill_row["unique_skill"], score))
        return similarity_records
    code_similarity = calculate_similarity(code_topics_df, skills_df)
    open_similarity = calculate_similarity(open_topics_df, skills_df)

    code_similarity_data = spark.createDataFrame(pd.DataFrame(code_similarity, columns=["unique_topic", "unique_skill", "similarity_score"]))
    open_similarity_data = spark.createDataFrame(pd.DataFrame(open_similarity, columns=["unique_topic", "unique_skill", "similarity_score"]))

    # Aggregate scores:
    # Join similarity scores with the exploded DataFrames,
    # taking an average of the similarity scores over all skills of a job for each topic.
    jobs_cols_to_group_by = [col for col in jobs_exploded.columns if col != "skill"]
    jobs_mapping = jobs_exploded.distinct()
    topics_avg_similarity = code_similarity_data.join(
        jobs_mapping,
        code_similarity_data["unique_skill"] == jobs_mapping["skill"]
    ).groupBy(*(jobs_cols_to_group_by + ["unique_topic"])).agg(
        avg("similarity_score").alias("similarity_per_topic")
    )

    code_cols_to_group_by = [col for col in code_questions_exploded.columns if col != "topic"]
    code_questions_mapping = code_questions_exploded.distinct()
    code_avg_similarity = topics_avg_similarity.join(
    code_questions_mapping, topics_avg_similarity["unique_topic"] == code_questions_mapping["topic"]) \
    .groupBy(*(code_cols_to_group_by + jobs_cols_to_group_by)).agg(
    avg("similarity_per_topic").alias("similarity"))

    open_cols_to_group_by = [col for col in open_questions_exploded.columns if col != "topic"]
    open_questions_mapping = open_questions_exploded.distinct()
    open_avg_similarity = topics_avg_similarity.join(
        open_questions_mapping, topics_avg_similarity["unique_topic"] == open_questions_mapping["topic"]) \
    .groupBy(*(open_cols_to_group_by + jobs_cols_to_group_by)).agg(
    avg("similarity_per_topic").alias("similarity"))

    return code_avg_similarity, open_avg_similarity


def calculate_score(jobs_sample, spark):
    aggregated_code_scores, aggregated_open_scores = topics_skills_similarity(jobs_sample, spark)
    return aggregated_code_scores, aggregated_open_scores

