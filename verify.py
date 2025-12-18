
import sys
import os
import pandas as pd

# Add local directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

try:
    from src.recommender import AssessmentEngine
    print("✅ Core Engine Module Imported")
except ImportError as e:
    print(f"❌ Module Import Error: {e}")
    sys.exit(1)

def run_diagnostics():
    try:
        # Load mock artifacts
        df_products = pd.read_csv('data/shl_products.csv')
        df_jobs = pd.read_csv('data/job_roles.csv')
        
        # Init System
        print("Initializing Logic Core...")
        system = AssessmentEngine(df_products)
        
        # Sample Test Case
        test_case = df_jobs.iloc[0]
        desc = test_case['Role_Description']
        skills = test_case['Required_Skills']
        
        print(f"Diagnosing Recommender with Role: {test_case['Role_Title']}")
        results = system.generate_recommendations(desc, skills, k=3)
        
        if not results.empty:
            print("\n✅ Diagnosis Successful. Top Recommendations:")
            print(results[['Assessment_Name', 'match_score']])
        else:
            print("❌ Warning: Engine returned no results.")
            
    except Exception as error:
        print(f"❌ Runtime Error: {error}")
        sys.exit(1)

if __name__ == "__main__":
    run_diagnostics()
