import streamlit as st
import pandas as pd
from src.recommender import AssessmentEngine

# Configuration
st.set_page_config(page_title="SHL Intelligent Recommender", page_icon="", layout="wide")

# Header
st.title(" SHL Assessment Discovery Engine")
st.markdown("""
**Intelligent matching system** designed to align job requirements with the optimal SHL assessments.
Powered by NLP and semantic analysis.
""")

# Data Loading
@st.cache_data
def get_catalogue():
    return pd.read_csv('data/shl_products.csv')

catalogue_df = get_catalogue()

# Engine Initialization
@st.cache_resource
def init_engine(df):
    return AssessmentEngine(df)

engine = init_engine(catalogue_df)

# Sidebar Config
st.sidebar.header("Tuning Parameters")
result_count = st.sidebar.slider("Results to Display", 1, 10, 5)
weight_sem = st.sidebar.slider("Semantic Weight", 0.0, 1.0, 0.5, help="Importance of description matching")
weight_skill = st.sidebar.slider("Skill Weight", 0.0, 1.0, 0.5, help="Importance of exact/fuzzy skill matching")

# Main Interface
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Position Profile")
    raw_desc = st.text_area("Job Description", height=200, placeholder="Paste role description here (e.g., Senior Backend Engineer with Python experience...)")
    raw_skills = st.text_input("Key Skills (Optional, comma-separated)", placeholder="Python, Django, AWS, Leaderhip")
    
    run_search = st.button("Find Best Assessments", type="primary")

with right_col:
    st.subheader("Recommended Assessments")
    if run_search:
        if not raw_desc:
            st.info("Please provide a job description to begin.")
        else:
            with st.spinner("Analyzing semantics and competencies..."):
                results = engine.generate_recommendations(
                    raw_desc, 
                    raw_skills, 
                    k=result_count, 
                    weights=(weight_sem, weight_skill)
                )
            
            st.success(f"Identified {len(results)} optimal matches.")
            
            for rank, row in results.iterrows():
                score_pct = row['match_score']
                with st.expander(f"#{rank+1}: {row['Assessment_Name']} (Match: {score_pct:.2f})"):
                    st.caption(f"Category: {row['Assessment_Type']}")
                    st.write(f"**Competencies:** {row['Skills_Tested']}")
                    st.markdown(f"_{row['Description']}_")

# Footer
st.markdown("---")
st.caption("Advanced AI Recommender System")
