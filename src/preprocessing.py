
import pandas as pd
import re

def clean_text(text):
    """
    Basic text cleaning: lowercase, remove special chars.
    """
    if pd.isna(text): return ""
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    return " ".join(text.split())

def prepare_catalogue_features(df):
    """
    Creates the 'combined_text' column for embedding.
    Format: Name + Test Type + Description + Duration
    """
    df = df.fillna("")
    
    # Ensure Test_Type is a string (it might be a JSON list string)
    # We just want keywords.
    
    df['combined_text'] = (
        "Assessment Name: " + df['Assessment_Name'] + ". " +
        "Type: " + df['Test_Type'] + ". " +
        "Duration: " + df['Duration'] + ". " +
        "Description: " + df['Description']
    )
    
    return df['combined_text'].tolist()
