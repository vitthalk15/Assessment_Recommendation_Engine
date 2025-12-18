import numpy as np

def calculate_precision(recommended_list, truth_set, k):
    """
    Computes Precision@K: Fraction of retrieved items that are relevant.
    """
    if not truth_set:
        return 0.0
    
    top_k_preds = recommended_list[:k]
    hits = [x for x in top_k_preds if x in truth_set]
    
    return len(hits) / k

def calculate_recall(recommended_list, truth_set, k):
    """
    Computes Recall@K: Fraction of relevant items that were retrieved.
    """
    if not truth_set:
        return 0.0
        
    top_k_preds = recommended_list[:k]
    hits = [x for x in top_k_preds if x in truth_set]
    
    return len(hits) / len(truth_set)
