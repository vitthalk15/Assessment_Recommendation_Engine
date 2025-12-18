from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import pandas as pd
import numpy as np

def create_text_features(corpus, stop_words='english', max_vocab=2000, apply_lsa=True, n_components=10):
    """
    Generates numerical features from text using TF-IDF and SVD (LSA).
    
    Args:
        corpus: List of text strings.
        max_vocab: Max features for TF-IDF.
        apply_lsa: Whether to reduce dimensions using LSA.
        
    Returns:
        vectorizer, lsa_model, transformed_matrix
    """
    # Use bigrams to capture phrases like "machine learning"
    tfidf = TfidfVectorizer(stop_words=stop_words, max_features=max_vocab, ngram_range=(1, 2))
    tfidf_matrix = tfidf.fit_transform(corpus)
    
    reducer = None
    final_features = tfidf_matrix
    
    # Apply LSA if dimensionality allows
    if apply_lsa and tfidf_matrix.shape[1] > n_components:
        reducer = TruncatedSVD(n_components=n_components, random_state=42)
        final_features = reducer.fit_transform(tfidf_matrix)
        
    return tfidf, reducer, final_features

def vectorize_new_text(vectorizer, reducer, text_input):
    """
    Converts new text input into the existing feature space.
    """
    if isinstance(text_input, str):
        text_input = [text_input]
    
    # Text -> TF-IDF
    vectors = vectorizer.transform(text_input)
    
    # TF-IDF -> LSA (if model exists)
    if reducer:
        vectors = reducer.transform(vectors)
        
    return vectors
