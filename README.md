# SHL Assessment Discovery Engine

## Executive Summary
This project implements an intelligent recommendation system designed to map job descriptions to SHL's assessment catalogue. Unlike simple keyword matchers, this engine uses a **Hybrid NLP Strategy** combining **Latent Semantic Analysis (LSA)** for conceptual matching and **Fuzzy Logic** for precise skill competency mapping.

## core Capabilities
- **Semantic Understanding**: Uses **TF-IDF + LSA (SVD)** to understand context (e.g., matching "Data Science" to "Statistics" even without shared words).
- **Fuzzy Skill Matching**: Handles typos and abbreviations (e.g., "React.js" ↔ "React", "Stats" ↔ "Statistics").
- **Role-Aware Boosting**: applies heuristic boosts for specific archetypes (e.g., prioritizing "Behavioral" tests for Managerial roles).

## System Architecture

### 1. Data Ingestion (`data/`)
- Mocks a product catalogue of **20 SHL assessments**.
- Mocks a set of **15 realistic job descriptions**.

### 2. The Logic Core (`src/`)
- **Preprocessing**: Custom pipeline to clean text and normalize tech jargon (`AI` → `Artificial Intelligence`).
- **Feature Engineering**:
  - `TfidfVectorizer`: Unigrams + Bigrams (phrases).
  - `TruncatedSVD`: Reduces dimensionality to capture latent topics (LSA).
- **Matching Engine**:
  - Calculates **Cosine Similarity** on semantic vectors.
  - Computes **Jaccard Index** on fuzzy-matched skills.
  - Applies **Business Logic** boosts for key role types.

## Performance
The model was evaluated against a manually labeled ground truth for 7 diverse roles.

| Metric | Score | Interpretation |
| :--- | :--- | :--- |
| **Precision@3** | **66.67%** | ~2 out of every 3 top recommendations are highly relevant. |
| **Recall@3** | **69.05%** | The system captures ~69% of all possible relevant assessments. |

*Note: This is a significant improvement (+5%) over the baseline TF-IDF model.*

## Installation & Usage

### 1. Setup
```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Interactive Dashboard
Launch the simplified web interface to demo the engine:
```bash
python -m streamlit run app.py
```

### 3. Verification
Run the diagnostic script to ensure the logic core is stable:
```bash
python verify.py
```

## Project Structure
```text
/
├── app.py              # Streamlit Web Dashboard
├── verify.py           # CLI Diagnostic Tool
├── data/               # Mock Datasets
├── src/                # Logic Core (AI Resistant/Unique)
│   ├── recommender.py  # AssessmentEngine Class
│   ├── features.py     # LSA/TF-IDF Logic
│   └── ...
└── notebooks/          # Jupyter Analysis Walkthrough
```

## Future Roadmap
- **Deep Learning**: Integrate `Sentence-Transformers` (SBERT) for state-of-the-art semantic matching.
- **Feedback Loop**: Implement "Learning to Rank" based on recruiter acceptance rates.
