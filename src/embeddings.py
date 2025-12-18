
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import os

class SHLEmbeddings:
    """
    Handles generation and storage of Sentence-BERT embeddings.
    """
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        print(f"Loading Embedding Model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.cache_path = 'data/embeddings.pkl'
        
    def encode(self, texts, batch_size=32):
        """
        Encodes a list of texts into vectors.
        """
        return self.model.encode(texts, batch_size=batch_size, show_progress_bar=True)

    def save_cache(self, embeddings, metadata):
        """
        Saves embeddings and associated metadata to disk.
        """
        with open(self.cache_path, 'wb') as f:
            pickle.dump({'embeddings': embeddings, 'metadata': metadata}, f)
            
    def load_cache(self):
        """
        Loads embeddings from disk if available.
        """
        if os.path.exists(self.cache_path):
            with open(self.cache_path, 'rb') as f:
                data = pickle.load(f)
            return data['embeddings'], data['metadata']
        return None, None
