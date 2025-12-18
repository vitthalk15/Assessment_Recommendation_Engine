import re

# Extended list of stopwords to filter out common noise
STOPWORDS = set([
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
])

# Normalize tech terms to their full standard forms
SKILL_ALIASES = {
    'stats': 'statistics',
    'ml': 'machine learning',
    'ai': 'artificial intelligence',
    'js': 'javascript',
    'reactjs': 'react',
    'db': 'database',
    'algo': 'algorithms',
    'comm': 'communication',
    'py': 'python',
    'cpp': 'c++',
    'ds': 'data science',
    'nlp': 'natural language processing',
    'dl': 'deep learning',
    'ux': 'user experience',
    'ui': 'user interface',
    'be': 'backend',
    'fe': 'frontend',
    'mgmt': 'management',
    'hr': 'human resources'
}

def clean_input_text(raw_text):
    """
    Standardizes input text: lowercasing, removing noise, and stripping stopwords.
    """
    if not isinstance(raw_text, str):
        return ""
    
    # 1. Lowercase
    cleaned = raw_text.lower()
    
    # 2. Keep only alphanumeric and whitespace
    cleaned = re.sub(r'[^a-z0-9\s]', ' ', cleaned)
    
    # 3. Filter stopwords
    tokens = [t for t in cleaned.split() if t not in STOPWORDS]
    
    return " ".join(tokens)

def expand_skill_terms(text):
    """
    Maps abbreviations (e.g., 'ML') to full terms ('Machine Learning').
    """
    if not isinstance(text, str):
        return ""
    
    tokens = text.lower().split()
    # Replace alias if exists, else keep original
    normalized = [SKILL_ALIASES.get(t, t) for t in tokens]
    return " ".join(normalized)

def run_preprocess(text):
    """
    Execution pipeline for text preprocessing.
    """
    text = expand_skill_terms(text)
    text = clean_input_text(text)
    return text
