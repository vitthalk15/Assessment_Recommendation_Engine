import streamlit as st
import pandas as pd
from src.engine import RecommendationEngine

# Page Config
st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")

# Title and Subs
st.title("SHL Assessment Recommendation Engine")
st.markdown("""
This tool uses **Semantic Search (RAG)** to map your job description to the best SHL assessments.
""")

# Initialize Engine (Cached)
@st.cache_resource
def load_engine():
    return RecommendationEngine()

try:
    with st.spinner("Loading AI Engine..."):
        engine = load_engine()
    st.success("Engine Ready!")
except Exception as e:
    st.error(f"Failed to load engine: {e}")
    st.stop()

# Input
query = st.text_area("Enter Job Description or Role Requirement:", height=150, 
                    value="I need a test for a Senior Java Developer with Spring Boot experience.")

if st.button("Recommend Assessments", type="primary"):
    if not query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("Searching Catalogue..."):
            results = engine.search(query, top_k=10)
        
        # Display
        st.subheader(f"Top {len(results)} Recommendations")
        
        for i, res in enumerate(results):
            with st.expander(f"#{i+1} {res['Assessment_Name']} (Score: {res['Score']:.4f})", expanded=(i==0)):
                st.markdown(f"**URL:** [{res['Assessment_url']}]({res['Assessment_url']})")
                st.write(res['Description'])
