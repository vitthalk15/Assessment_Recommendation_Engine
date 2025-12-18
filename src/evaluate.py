
import pandas as pd
from src.engine import RecommendationEngine

def compute_metrics():
    # Load Train Data
    try:
        train_df = pd.read_excel('data/Gen_AI Dataset.xlsx', sheet_name='Train-Set')
    except Exception as e:
        print(f"Error loading Excel: {e}")
        return

    print(f"Evaluating on {len(train_df)} queries...")
    
    engine = RecommendationEngine()
    
    hits = 0
    
    for idx, row in train_df.iterrows():
        query = row['Query']
        target_url = row['Assessment_url']
        
        # Clean target url (strip trailing /)
        if hasattr(target_url, 'strip'):
            target_slug = target_url.strip().rstrip('/').split('/')[-1]
            
        results = engine.search(query, top_k=10)
        
        # Check hit
        found = False
        top_slugs = []
        for res in results:
            res_url = res['Assessment_url'].strip().rstrip('/')
            res_slug = res_url.split('/')[-1]
            top_slugs.append(res_slug)
            
            if res_slug == target_slug:
                found = True
                break
        
        if found:
            hits += 1
        else:
            if idx < 5:
                # Debug to file to avoid console issues
                with open('mismatches.txt', 'a') as f:
                    f.write(f"\nQUERY: {query}\n")
                    f.write(f"TARGET: {target_url} (Slug: {target_slug})\n")
                    f.write(f"TOP 3 FOUND: {top_slugs[:3]}\n")
            
    recall = (hits / len(train_df)) * 100
    print(f"\nFinal Result: Recall@10 = {recall:.2f}%")
    
if __name__ == "__main__":
    compute_metrics()
