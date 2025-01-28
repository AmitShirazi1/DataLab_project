from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, lit, udf, array, broadcast
from pyspark.sql.types import ArrayType, FloatType, DoubleType
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from consts import DATA_PATH, QUESTIONS_PATH, MID_CALC_PATH, open_csv_file

def topics_skills_similarity(jobs):
    # Start Spark session
    spark = SparkSession.builder.appName("JobQuestionScoring").getOrCreate()

    jobs = jobs.fillna({'skills': ''})
    # Explode the skills columns
    jobs_exploded = jobs.withColumn("skill", explode(split("skills", ",")))
    code_questions_exploded = open_csv_file(MID_CALC_PATH, "code_questions_exploded.csv")
    open_questions_exploded = open_csv_file(QUESTIONS_PATH, "open_questions_exploded.csv")

    # Cartesian product between job postings and questions
    cartesian_code = jobs_exploded.crossJoin(code_questions_exploded)
    cartesian_open = jobs_exploded.crossJoin(open_questions_exploded)

    print("cartesian_code:")
    cartesian_code.limit(10).show()
    print("\ncartesian_open:")
    cartesian_open.limit(10).show()

    # Load the model globally
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # UDF to generate embeddings
    @udf(ArrayType(FloatType()))
    def generate_embedding(text):
        return model.encode(text).tolist()

    # UDF to calculate cosine similarity
    @udf(DoubleType())
    def calculate_similarity(embedding1, embedding2):
        return float(cosine_similarity([embedding1], [embedding2])[0][0])

    # Extract unique skills
    unique_skills = jobs_exploded.select("skill").distinct()
    unique_topics_code = open_csv_file(MID_CALC_PATH, "unique_topics_code.csv")
    unique_topics_open = open_csv_file(MID_CALC_PATH, "unique_topics_open.csv")

    # Cartesian product of unique skills and topics
    unique_pairs_code = unique_skills.crossJoin(unique_topics_code)
    unique_pairs_open = unique_skills.crossJoin(unique_topics_open)

    # Generate embeddings for skills and topics
    unique_pairs_code = unique_pairs_code.withColumn("skill_embedding", generate_embedding(col("skill")))
    unique_pairs_open = unique_pairs_open.withColumn("skill_embedding", generate_embedding(col("skill")))

    # Compute similarity for unique pairs
    unique_pairs_code = unique_pairs_code.withColumn(
        "similarity", calculate_similarity(col("skill_embedding"), col("topic_embedding"))
    )
    unique_pairs_open = unique_pairs_open.withColumn(
        "similarity", calculate_similarity(col("skill_embedding"), col("topic_embedding"))
    )

    print("\nunique_pairs_code:")
    unique_pairs_code.limit(10).show()
    print("\nunique_pairs_open:")
    unique_pairs_open.limit(10).show()

    # Join similarity back to Cartesian product
    cartesian_code_with_similarity = cartesian_code.join(
        broadcast(unique_pairs_code.select("skill", "topic", "similarity")),
        on=["skill", "topic"],
        how="left"
    )

    cartesian_open_with_similarity = cartesian_open.join(
        broadcast(unique_pairs_open.select("skill", "topic", "similarity")),
        on=["skill", "topic"],
        how="left"
    )

    # Aggregate similarity scores for each job-question pair
    columns_to_group_by = [col for col in cartesian_code.columns if col not in ["skill", "topic"]]
    aggregated_code_scores = cartesian_code_with_similarity.groupBy(*columns_to_group_by).agg(
        {"similarity": "avg"}
    )

    columns_to_group_by = [col for col in cartesian_open.columns if col not in ["skill", "topic"]]
    aggregated_open_scores = cartesian_open_with_similarity.groupBy(*columns_to_group_by).agg(
        {"similarity": "avg"}
    )

    print("\naggregated_code_scores:")
    aggregated_code_scores.limit(10).show()
    print("\naggregated_open_scores:")
    aggregated_open_scores.limit(10).show()

    return aggregated_code_scores, aggregated_open_scores


def calculate_score(jobs_sample):
    aggregated_code_scores, aggregated_open_scores = topics_skills_similarity(jobs_sample)
    return aggregated_code_scores, aggregated_open_scores