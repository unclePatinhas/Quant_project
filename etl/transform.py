import re
import pandas as pd
from datetime import datetime
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk


# nltk.download('punkt')
# nltk.download('punkt_tab')
# nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def clean_text(text:str) -> str:
    # remove  URLs
    text = re.sub(r"http\S+|wwww\S+|https\S+", "", text)
    # remove mentions and hashtags
    text = re.sub(r"@\w+|#\w+", "", text)
    # remove punctuation
    text = re.sub(r"[^A-Za-z0-9\s]+", '', text)
    
    return text.lower().strip()


def tokenize_text(text: str) -> list:
    tokens = word_tokenize(text)
    
    res = [
        word for word in tokens
        if word not in stop_words and len(word) > 2
        ]

    return res


def normalize_date(date_str: str) -> str:
    try:
        norm_date = datetime.strptime(date_str,\
            '%a %b %d %H:%M:%S +0000 %Y').isoformat()
        return norm_date
    
    except Exception:
        return None
    
    
def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df['text'].str.len() > 0]  # Remove empty tweets
    df['clean_text'] = df['text'].apply(clean_text)
    df['tokens'] = df['clean_text'].apply(tokenize_text)
    # df['created_at'] = df['created_at'].apply(normalize_date)
    # df = df.dropna(subset=['created_at'])
    
    cols_select = ['id', 'clean_text', 'tokens'] #'created_at',
    
    return df[cols_select]
