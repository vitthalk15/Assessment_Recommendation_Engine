import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from src.preprocessing import run_preprocess
from src.features import create_text_features, vectorize_new_text
import difflib

class AssessmentEngine:
    def __init__(self, catalogue_df):
        self.catalogue = catalogue_df
        
        # Prepare text fields for vectorization
        self.catalogue['clean_desc'] = self.catalogue['Description'].astype(str).apply(run_preprocess)
        self.catalogue['clean_skills'] = self.catalogue['Skills_Tested'].astype(str).apply(run_preprocess)
        
        # Create a combined corpus for a richer vocabulary
        full_text_corpus = self.catalogue['clean_desc'] + " " + self.catalogue['clean_skills']
        
        # Initialize the NLP Core (TF-IDF + LSA)
        self.tfidf, self.lsa, self.vectors = create_text_features(full_text_corpus, n_components=15)
        
    def _compute_fuzzy_overlap(self, job_skills_str, prod_skills_str):
        """
        Internal helper: Computes skill overlap using fuzzy matching to handle typos.
        """
        if pd.isna(job_skills_str) or pd.isna(prod_skills_str):
            return 0.0
            
        required = [s.strip().lower() for s in str(job_skills_str).split(',') if s.strip()]
        offered = [s.strip().lower() for s in str(prod_skills_str).split(',') if s.strip()]
        
        if not required or not offered:
            return 0.0
            
        matched = set()
        for r_skill in required:
            # Direct match?
            if r_skill in offered:
                matched.add(r_skill)
                continue
            
            # Fuzzy match? (allowing for slight spelling variations)
            close = difflib.get_close_matches(r_skill, offered, n=1, cutoff=0.85)
            if close:
                matched.add(r_skill)
        
        # Jaccard Index approximation
        intersect = len(matched)
        union = len(set(required)) + len(set(offered)) - intersect
        
        return intersect / union if union > 0 else 0.0

    def generate_recommendations(self, job_desc, skills_required='', k=5, weights=(0.5, 0.5)):
        """
        Main entry point. Uses a hybrid approach:
        1. Semantic Search (LSA) on descriptions.
        2. Skill Overlap (Exact + Fuzzy).
        3. Business Rules (Role-based boosting).
        """
        # 1. Semantic Similarity
        processed_input = run_preprocess(job_desc + " " + skills_required)
        query_vec = vectorize_new_text(self.tfidf, self.lsa, processed_input)
        semantic_scores = cosine_similarity(query_vec, self.vectors)[0]
        
        final_scores = []
        job_lower = job_desc.lower()
        
        # Determine Role Context for Boosting
        is_mgr_role = any(kw in job_lower for kw in ['manager', 'lead', 'head', 'director', 'leadership'])
        is_tech_role = any(kw in job_lower for kw in ['engineer', 'developer', 'coding', 'software', 'tech'])
        
        for idx, row in self.catalogue.iterrows():
            # Base Score
            base_sim = semantic_scores[idx] * weights[0]
            
            # Skill Score
            skill_sim = self._compute_fuzzy_overlap(skills_required, row.get('Skills_Tested', ''))
            total_score = base_sim + (skill_sim * weights[1])
            
            # Apply Boosting Shortcuts
            a_type = row['Assessment_Type']
            a_name = row['Assessment_Name'].lower()
            
            # Logic: Managers need behavioral assessments
            if is_mgr_role:
                if a_type in ['Behavioral', 'Personality', 'Simulation'] or 'management' in a_name:
                    total_score += 0.20
                    
            # Logic: Tech roles need coding assessments
            if is_tech_role and ('coding' in a_name or 'systems' in a_name):
                total_score += 0.20
            
            final_scores.append(total_score)
            
        # Compile Results
        output = self.catalogue.copy()
        output['match_score'] = final_scores
        
        return output.sort_values(by='match_score', ascending=False).head(k)[
            ['Assessment_Name', 'Assessment_Type', 'Skills_Tested', 'match_score', 'Description']
        ]
