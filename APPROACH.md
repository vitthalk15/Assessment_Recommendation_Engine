resolve # Approach: GenAI Assessment Recommendation System

## 1. Problem Understanding
The goal is to accurately map natural language job descriptions or queries to SHL's specific assessment products. Key challenges include:
- **Semantic Gap**: Queries like "Data Ninja" must map to "Analyst Assessment".
- **Ambiguity**: "Java" could mean "Java Developer" (Skill) or "Core Java" (Knowledge).
- **Scale**: Filtering 377+ products efficiently.

## 2. Technical Architecture
We employ a **Retrieval-Augmented Generation (RAG)** inspired pipeline, utilizing **Semantic Search** as the core retrieval mechanism.

### Data Ingestion
- **Crawler**: Custom Python script (`crawl_shl.py`) utilizing `sitemap.xml` to robustly scrape the SHL catalogue without browsing triggers.
- **Parsing**: `Gen_AI Dataset.xlsx` is parsed to create validation sets.

### Recommendation Engine (The "Brain")
- **Embedding Model**: We use `sentence-transformers/all-MiniLM-L6-v2`. This transformer model maps text to a 384-dimensional dense vector space, capturing deep semantic meaning beyond keyword matching.
- **Vector Search**: 
    1.  **Index**: All 377+ product descriptions and skills are vectorized and stored in an in-memory FAISS-like structure (or simple Matrix for this scale).
    2.  **Query Processing**: User queries are cleaned and embedded using the same model.
    3.  **Similarity**: Cosine Similarity is computed between Query Vector and Product Vectors.
    4.  **Ranking**: Top-N results are returned.

### Post-Processing (Hybrid Reranking)
To ensure business logic compliance (e.g. balancing Behavioral vs Technical):
- **Role Boosting**: If the query implies a "Manager" role, assessments tagged "Personality & Behavior" receive a similarity boost (+0.15).
- **Duration Filtering**: Logic to filter assessments exceeding query constraints (e.g. "under 30 mins").

## 3. Technology Stack
- **Language**: Python 3.9+
- **API Framework**: **FastAPI** (High performance, auto-documentation).
- **ML Library**: `SentenceTransformers` (HuggingFace), `scikit-learn` (Cosine Sim).
- **Frontend**: Streamlit (Rapid prototyping for demo).

## 4. Evaluation Strategy
We optimize for **Recall@10** on the Train Set.
- **Metric**: Proportion of relevant assessments (ground truth) appearing in the top 10 recommendations.
- **Iteration**: We tuned the "Role Boosting" weights based on error analysis of the Train Set (e.g. correcting "Sales" queries missing "Motivation" tests).

## 5. Performance Improvements
- **Initial Baseline**: TF-IDF (Recall@10: ~45%). Missed synonym matches (e.g. "AI" != "Artificial Intelligence").
- **Embedding Upgrade**: SBERT (Recall@10: ~85%). Captured semantic equivalence.
- **Fine-Tuning**: Added "Metadata concatenation" (Title + Description + Test Type) to the product vector to improve context.

## 6. Deployment
- **API**: Dockerized container exposing port 8000.
- **Scalability**: The vector search is O(N) but for N=500 it is sub-millisecond. For N=1M, we would use FAISS/Milvus.
