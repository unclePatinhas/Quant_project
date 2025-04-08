import re
import pandas as pd
from datetime import datetime

from .data_model import TweetModel
from utils.logger import setup_logger

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
    
    # remove the old style retweet text "RT"
    text = re.sub(r'^RT[\s]+', '', text)
    
    # remove mentions and hashtags
    text = re.sub(r"@\w+|#\w+", "", text)
    
    # remove hashtags # from the word
    text = re.sub(r'#', '', text)

    # # remove punctuation - do not do this otherwise loose percent numbers
    # text = re.sub(r"[^A-Za-z0-9\s]+", '', text)
    
    # # remove single numeric terms in the text
    # tweet = re.sub(r'[0-9]', '', tweet)
    
    # lower case and remove spaces at beggining and end
    text = text.lower().strip()
    
    return text

def tokenize_text(text: str) -> list:
    tokens = word_tokenize(text)
    
    res = [word for word in tokens 
           if word not in stop_words and len(word) > 2]

    return res

def normalize_date(date_str: str) -> str:
    try:
        
        norm_date = datetime.fromtimestamp(date_str).isoformat() 
        # '%a %b %d %H:%M:%S +0000 %Y' 
        return norm_date
    
    except Exception:
        return None
    
def validate_tweets_data(df: pd.DataFrame) -> pd.DataFrame:
    """
        Validate data structure and types
    """
    logger = setup_logger("app.log")
    
    valid_records = []
    for idx, row in df.iterrows():
        try:
            tweet = TweetModel(
                id=row['id'],
                author=row['author'],
                post_date = row["post_date"],
                clean_text = row['clean_text'],
                comment_num = row['comment_num'],
                retweet_num = row['retweet_num'],
                like_num = row['like_num'],
                tokens=row['tokens']
            )
            valid_records.append(tweet.model_dump())
        except Exception as e:
            # Log invalid tweet data
            logger.error(f"Row {idx} - Invalid Tweet data: {e} | Raw data: {row.to_dict()}")

    return pd.DataFrame(valid_records)

def transform(df: pd.DataFrame) -> pd.DataFrame:    
    df = df[df['body'].str.len() > 0]  # Remove empty tweets
    df['clean_text'] = df['body'].apply(clean_text)
    df['tokens'] = df['clean_text'].apply(tokenize_text)
    df['post_date'] = df['post_date'].apply(normalize_date)
    df.rename(columns={'tweet_id':'id', 'writer':'author'}, inplace=True)
    df = df.dropna(subset=['author', 'post_date'])
    
    cols_select = ['id', 'author', 'post_date', 'clean_text', 
                   'comment_num', 'retweet_num', 'like_num', 'tokens']
    
    df_valid = validate_tweets_data(df[cols_select])
    
    return df_valid, df
