from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, lit, udf, array, broadcast, trim, lower, avg
from pyspark.sql.types import ArrayType, FloatType, DoubleType
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from consts import DATA_PATH, QUESTIONS_PATH, MID_CALC_PATH, open_csv_file

# def topics_skills_similarity(jobs, spark):
#     jobs = jobs.fillna({'skills': ''})
#     # Explode the skills columns
#     jobs_exploded = jobs.withColumn("skill", explode(split(col("skills"), ",\\s*"))) \
#         .withColumn("skill", trim(lower(col("skill")))).cache()
#     code_questions_exploded = open_csv_file(spark, MID_CALC_PATH, "code_questions_exploded.csv") \
#         .withColumn("topic", trim(lower(col("topic")))).cache()
#     open_questions_exploded = open_csv_file(spark, MID_CALC_PATH, "open_questions_exploded.csv") \
#         .withColumn("topic", trim(lower(col("topic")))).cache()

#     # Cartesian product between job postings and questions
#     cartesian_code = jobs_exploded.crossJoin(code_questions_exploded).cache()
#     cartesian_open = jobs_exploded.crossJoin(open_questions_exploded).cache()

#     print("cartesian_code:")
#     cartesian_code.limit(10).show()
#     print("\ncartesian_open:")
#     cartesian_open.limit(10).show()

#     # Load the model globally
#     model = SentenceTransformer('all-MiniLM-L6-v2')

#     # UDF to generate embeddings
#     @udf(ArrayType(FloatType()))
#     def generate_embedding(text):
#         embedding = model.encode(text)
#         return [float(x) for x in embedding]  # Explicitly convert to float

#     # UDF to calculate cosine similarity
#     @udf(DoubleType())
#     def calculate_similarity(embedding1, embedding2):
#         if not embedding1 or not embedding2:
#             print(f"Invalid embeddings: embedding1={embedding1}, embedding2={embedding2}")
#             return None
#         if not embedding1 or not embedding2 or len(embedding1) != len(embedding2):
#             print(f"Invalid embeddings or dimensional mismatch: {embedding1}, {embedding2}")
#             return None
#         try:
#             # Convert to float explicitly
#             embedding1 = [float(x) for x in embedding1]
#             embedding2 = [float(x) for x in embedding2]
#             return float(cosine_similarity([embedding1], [embedding2])[0][0])
#         except Exception as e:
#             print(f"Error calculating similarity: {e}")
#             return None

#     # Extract unique skills
#     unique_skills = jobs_exploded.select("skill").distinct() \
#         .withColumn("skill", trim(lower(col("skill")))).cache()
#     unique_topics_code = open_csv_file(spark, MID_CALC_PATH, "unique_topics_code.csv") \
#         .withColumn("topic", trim(lower(col("topic")))).cache()
#     unique_topics_open = open_csv_file(spark, MID_CALC_PATH, "unique_topics_open.csv") \
#         .withColumn("topic", trim(lower(col("topic")))).cache()

#     # Cartesian product of unique skills and topics
#     unique_pairs_code = unique_skills.crossJoin(unique_topics_code).cache()
#     unique_pairs_open = unique_skills.crossJoin(unique_topics_open).cache()

#     # Generate embeddings for skills and topics
#     unique_pairs_code = unique_pairs_code.withColumn("skill_embedding", generate_embedding(col("skill"))).cache()
#     unique_pairs_open = unique_pairs_open.withColumn("skill_embedding", generate_embedding(col("skill"))).cache()

#     # Compute similarity for unique pairs
#     unique_pairs_code = unique_pairs_code.withColumn(
#         "similarity", calculate_similarity(col("skill_embedding"), col("topic_embedding"))
#     ).cache()
#     unique_pairs_open = unique_pairs_open.withColumn(
#         "similarity", calculate_similarity(col("skill_embedding"), col("topic_embedding"))
#     ).cache()

#     print("\nunique_pairs_code:")
#     unique_pairs_code.limit(10).show()
#     print("\nunique_pairs_open:")
#     unique_pairs_open.limit(10).show()

#     # Join similarity back to Cartesian product
#     cartesian_code_with_similarity = cartesian_code.join(
#         broadcast(unique_pairs_code.select("skill", "topic", "similarity")),
#         on=["skill", "topic"],
#         how="left"
#     ).cache()

#     cartesian_open_with_similarity = cartesian_open.join(
#         broadcast(unique_pairs_open.select("skill", "topic", "similarity")),
#         on=["skill", "topic"],
#         how="left"
#     ).cache()

#     # Aggregate similarity scores for each job-question pair
#     columns_to_group_by = [col for col in cartesian_code.columns if col not in ["skill", "topic"]]
#     aggregated_code_scores = cartesian_code_with_similarity.groupBy(*columns_to_group_by).agg(
#         {"similarity": "avg"}
#     ).withColumnRenamed("avg(similarity)", "similarity").cache()

#     columns_to_group_by = [col for col in cartesian_open.columns if col not in ["skill", "topic"]]
#     aggregated_open_scores = cartesian_open_with_similarity.groupBy(*columns_to_group_by).agg(
#         {"similarity": "avg"}
#     ).withColumnRenamed("avg(similarity)", "similarity").cache()

#     print("\naggregated_code_scores:")
#     aggregated_code_scores.limit(10).show()
#     print("\naggregated_open_scores:")
#     aggregated_open_scores.limit(10).show()

#     return aggregated_code_scores, aggregated_open_scores


import pandas as pd

def topics_skills_similarity(jobs, spark):
    jobs_exploded = jobs.withColumn(
        "skill", explode(split(col("skills"), ",\\s*"))
    )
    code_questions_exploded = open_csv_file(spark, MID_CALC_PATH, "code_questions_exploded.csv")
    open_questions_exploded = open_csv_file(spark, MID_CALC_PATH, "open_questions_exploded.csv")

    # Collect unique skills and topics for embedding
    unique_skills = [row["skill"] for row in jobs_exploded.select("skill").distinct().collect()]
    unique_code_topics = [row["topic"] for row in code_questions_exploded.select("topic").distinct().collect()]
    unique_open_topics = [row["topic"] for row in open_questions_exploded.select("topic").distinct().collect()]

    print("unique_skills:")
    print(unique_skills[:10])
    print("unique_code_topics:")
    print(unique_code_topics[:10])
    print("unique_open_topics:")
    print(unique_open_topics[:10])

    # Generate embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    skills_embeddings = model.encode(unique_skills)
    code_topics_with_embeddings = model.encode(unique_code_topics)
    open_topics_with_embeddings = model.encode(unique_open_topics)

    print("skills_embeddings:")
    skills_embeddings[:10]
    print("code_topics_with_embeddings:")
    code_topics_with_embeddings[:10]
    print("open_topics_with_embeddings:")
    open_topics_with_embeddings[:10]

    # Compute similarity
    skills_df = pd.DataFrame({"skill": unique_skills, "embedding": list(skills_embeddings)})
    code_topics_df = pd.DataFrame({"topic": unique_code_topics, "embedding": list(code_topics_with_embeddings)})
    open_topics_df = pd.DataFrame({"topic": unique_open_topics, "embedding": list(open_topics_with_embeddings)})

    print("code_topics_df:")
    code_topics_df.head(10)
    print("open_topics_df:")
    open_topics_df.head(10)

    # Calculate similarity scores
    def calculate_similarity(topics_df, skills_df):
        similarity_records = []
        for _, topic_row in topics_df.iterrows():
            for _, skill_row in skills_df.iterrows():
                score = float(cosine_similarity([topic_row["embedding"]], [skill_row["embedding"]])[0][0])
                similarity_records.append((topic_row["topic"], skill_row["skill"], score))
        return similarity_records
    code_similarity = calculate_similarity(code_topics_df, skills_df)
    open_similarity = calculate_similarity(open_topics_df, skills_df)

    print("code_similarity:")
    code_similarity[:10]
    print("open_similarity:")
    open_similarity[:10]

    code_similarity_data = spark.createDataFrame(pd.DataFrame(code_similarity, columns=["topic", "skill", "similarity_score"]))
    open_similarity_data = spark.createDataFrame(pd.DataFrame(open_similarity, columns=["topic", "skill", "similarity_score"]))

    print("code_similarity_data:")
    code_similarity_data.limit(10).show()
    print("open_similarity_data:")
    open_similarity_data.limit(10).show()

    # Aggregate scores:
    # Join similarity scores with the exploded DataFrames,
    # taking an average of the similarity scores over all skills of a job for each topic.
    jobs_cols_to_group_by = [col for col in jobs_exploded.columns if col != "skills"]
    jobs_mapping = jobs_exploded.select(*jobs_cols_to_group_by).distinct()
    topics_avg_similarity = code_similarity_data.join(
        jobs_mapping,
        code_similarity_data["skill"] == jobs_mapping["skill"]
    ).groupBy(*(jobs_cols_to_group_by + ["topic"])).agg(
        avg("similarity_score").alias("similarity_per_topic")
    )

    code_cols_to_group_by = [col for col in code_questions_exploded.columns if col != "topics"]
    code_questions_mapping = code_questions_exploded.select(*code_cols_to_group_by).distinct()
    code_avg_similarity = topics_avg_similarity.join(
    code_questions_mapping, topics_avg_similarity["topic"] == code_questions_mapping["topic"]) \
    .groupBy(*(code_cols_to_group_by + jobs_cols_to_group_by)).agg(
    avg("similarity_per_topic").alias("similarity"))

    open_cols_to_group_by = [col for col in open_questions_exploded.columns if col != "topics"]
    open_questions_mapping = open_questions_exploded.select(*open_cols_to_group_by).distinct()
    open_avg_similarity = topics_avg_similarity.join(
        open_questions_mapping, topics_avg_similarity["topic"] == open_questions_mapping["topic"]) \
    .groupBy(*(open_cols_to_group_by + jobs_cols_to_group_by)).agg(
    avg("similarity_per_topic").alias("similarity"))

    print("code_avg_similarity:")
    code_avg_similarity.limit(10).show()
    print("open_avg_similarity:")
    open_avg_similarity.limit(10).show()

    return code_avg_similarity, open_avg_similarity


def calculate_score(jobs_sample, spark):
    aggregated_code_scores, aggregated_open_scores = topics_skills_similarity(jobs_sample, spark)
    return aggregated_code_scores, aggregated_open_scores

