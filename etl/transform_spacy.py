import re
import pandas as pd
from datetime import datetime
import spacy

# load English model
nlp = spacy.load("en_core_web_sm")

def clean_text(text:str) -> str:
    # remove  URLs
    text = re.sub(r"http\S+|wwww\S+|https\S+", "", text)
    # remove mentions and hashtags
    text = re.sub(r"@\w+|#\w+", "", text)
    
    return text.lower().strip()


def tokenize_text(text: str) -> list:
    doc = nlp(text)
    
    res = [
        token.text for token in doc
        if (not token.is_stop and 
            not token.is_punct and 
            not token.is_space and
            len(token.text) > 2) 
        ]

    return res

def normalize_date(date_str: str) -> str:
    try:
        norm_date = datetime.strptime(date_str,
                                      '%a %b %d %H:%M:%S +0000 %Y')\
                                          .isoformat()
        return norm_date
    
    except Exception:
        return None
    
def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df['text'].str.len() > 0]  # Remove empty tweets
    df['clean_text'] = df['text'].apply(clean_text)
    df['tokens'] = df['clean_text'].apply(tokenize_text)
    df['created_at'] = df['created_at'].apply(normalize_date)
    df = df.dropna(subset=['created_at'])
    
    cols_select = ['id', 'created_at', 'cleaned_text', 'tokens']
    
    return df[cols_select]
