
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from src.embeddings import SHLEmbeddings
from src.preprocessing import prepare_catalogue_features, clean_text
import os

class RecommendationEngine:
    def __init__(self, catalogue_path='data/shl_catalogue.csv'):
        self.catalogue_path = catalogue_path
        self.df = None
        self.vectors = None
        self.embedder = SHLEmbeddings()
        self._load_data()
        
    def _load_data(self):
        """
        Loads catalogue and ensures vectors are ready.
        """
        if not os.path.exists(self.catalogue_path):
            print("Catalogue not found. Please run crawler first.")
            return

        print("Loading catalogue...")
        self.df = pd.read_csv(self.catalogue_path)
        
        # Check cache
        vecs, meta = self.embedder.load_cache()
        
        # If cache invalid or size mismatch, re-compute
        if vecs is None or len(vecs) != len(self.df):
            print("Computing embeddings (this may take a moment)...")
            texts = prepare_catalogue_features(self.df)
            self.vectors = self.embedder.encode(texts)
            self.embedder.save_cache(self.vectors, texts)
        else:
            print("Loaded embeddings from cache.")
            self.vectors = vecs
            
    def search(self, query, top_k=10):
        """
        Semantic search with cosine similarity.
        """
        if self.df is None: return []
        
        # Embed query
        query_text = clean_text(query)
        query_vec = self.embedder.encode([query_text], batch_size=1)[0]
        
        # Compute similarity
        scores = cosine_similarity([query_vec], self.vectors)[0]
        
        # Boost based on role heuristics (optional layer)
        # self._apply_heuristics(query_text, scores)
        
        # Get top K
        top_indices = scores.argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            row = self.df.iloc[idx]
            results.append({
                "Assessment_Name": row['Assessment_Name'],
                "Assessment_url": row['Assessment_url'],
                "Description": row['Description'],
                "Score": float(scores[idx])
            })
            
        return results

    def _apply_heuristics(self, query, scores):
        # Implementation of "Manager" boost etc. 
        # For now we stick to pure semantic search as baseline.
        pass
