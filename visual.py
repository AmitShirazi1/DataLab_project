import streamlit as st
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split, count, round as spark_round
import plotly.express as px
import plotly.graph_objects as go

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Job Analysis Dashboard") \
    .getOrCreate()

# Load Data with Spark
@st.cache_data
def load_data_spark():
    job_data = spark.read.csv("/FileStore/tables/amit_tomer_hadar/all_jobpostings_with_skills.csv", header=True, inferSchema=True)
    code_questions_data = spark.read.csv("/FileStore/tables/amit_tomer_hadar/all_code_questions_with_topics.csv", header=True, inferSchema=True)
    open_questions_data = spark.read.csv("/FileStore/tables/amit_tomer_hadar/all_open_questions_with_topics.csv", header=True, inferSchema=True)
    return job_data, code_questions_data, open_questions_data

job_data, code_questions_data, open_questions_data = load_data_spark()

# Dashboard
st.title("Spark-Powered Job and Interview Analysis Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
industries = [row["industry"] for row in job_data.select("industry").distinct().collect()]
levels = [row["level"] for row in job_data.select("level").distinct().collect()]
difficulties = [row["difficulty"] for row in code_questions_data.select("difficulty").distinct().collect()]

selected_industry = st.sidebar.selectbox("Select Industry", options=industries)
selected_level = st.sidebar.selectbox("Select Job Level", options=levels)
selected_difficulty = st.sidebar.selectbox("Select Question Difficulty", options=difficulties)

# Filter Data with Spark
filtered_job_data = job_data.filter((col("industry") == selected_industry) & (col("level") == selected_level))
filtered_code_questions = code_questions_data.filter(col("difficulty") == selected_difficulty)

# Skills Analysis: Most In-Demand Skills
st.subheader("Skills Analysis")
skills_df = (
    filtered_job_data
    .select(explode(split(col("skills"), ", ")).alias("skill"))
    .groupBy("skill")
    .agg(count("skill").alias("count"))
    .orderBy(col("count").desc())
)

skills_plot = px.bar(
    skills_df.toPandas(),  # Plotly does not yet support Spark directly; this is an exception
    x="skill",
    y="count",
    title="Most In-Demand Skills",
    labels={"skill": "Skills", "count": "Count"},
)
st.plotly_chart(skills_plot)

# Technical Interview Questions Analysis: Donut Chart for Question Difficulty
st.subheader("Technical Interview Questions Analysis")
difficulty_counts = (
    code_questions_data
    .groupBy("difficulty")
    .count()
    .withColumnRenamed("count", "Difficulty Count")
)
difficulty_plot = px.pie(
    difficulty_counts.toPandas(),
    values="Difficulty Count",
    names="difficulty",
    title="Question Difficulty Distribution",
    color_discrete_map={"easy": "green", "medium": "yellow", "hard": "red"}
)
st.plotly_chart(difficulty_plot)

# Industry Distribution: Treemap
st.subheader("Industry Distribution")
industry_counts = (
    job_data
    .groupBy("industry")
    .count()
    .withColumnRenamed("count", "Job Postings")
    .orderBy(col("Job Postings").desc())
)

industry_plot = px.treemap(
    industry_counts.toPandas(),
    path=["industry"],
    values="Job Postings",
    title="Job Distribution Across Industries"
)
st.plotly_chart(industry_plot)

# Experience Level Distribution: Stacked Bar Chart
st.subheader("Experience Level Distribution")
level_distribution = (
    job_data
    .groupBy("level", "industry")
    .count()
    .orderBy("level", "industry")
)

pivoted_data = (
    level_distribution
    .groupBy("level")
    .pivot("industry")
    .sum("count")
    .fillna(0)
)

plot_data = pivoted_data.toPandas()
level_plot = px.bar(
    plot_data,
    x="level",
    y=[col for col in plot_data.columns if col != "level"],
    title="Experience Level Distribution",
    labels={"value": "Count", "variable": "Industry"},
    barmode="stack"
)
st.plotly_chart(level_plot)

# Skills Correlation Network
st.subheader("Skills Correlation Network")
skills_network_df = (
    filtered_job_data
    .select(explode(split(col("skills"), ", ")).alias("skill"))
    .crossJoin(filtered_job_data.select(explode(split(col("skills"), ", ")).alias("skill2")))
    .filter(col("skill") != col("skill2"))
)

skills_edges = skills_network_df.limit(100).toPandas()
fig = go.Figure(
    data=[
        go.Scatter(
            x=skills_edges["skill"],
            y=skills_edges["skill2"],
            mode="markers+lines",
        )
    ]
)
fig.update_layout(title="Skills Correlation Network", showlegend=False)
st.plotly_chart(fig)

# Interview Topics Heatmap
st.subheader("Interview Topics Heatmap")
heatmap_data = (
    code_questions_data
    .groupBy("topics", "difficulty")
    .count()
    .withColumnRenamed("count", "Frequency")
)

heatmap_pandas = heatmap_data.toPandas()
heatmap_plot = px.imshow(
    heatmap_pandas.pivot(index="topics", columns="difficulty", values="Frequency"),
    title="Interview Topics Heatmap",
    color_continuous_scale="coolwarm"
)
st.plotly_chart(heatmap_plot)

# Show Raw Data Option
st.sidebar.header("Explore Data")
if st.sidebar.checkbox("Show Raw Job Data"):
    st.write(filtered_job_data.show(truncate=False))

if st.sidebar.checkbox("Show Raw Technical Questions Data"):
    st.write(filtered_code_questions.show(truncate=False))

if st.sidebar.checkbox("Show Raw Open Questions Data"):
    st.write(open_questions_data.show(truncate=False))
