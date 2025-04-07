import pandas as pd
import logging

logger =  logging.getLogger(__name__)

def extract_tweets(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        logger.info(f"{len(df)} tweets loaded from {file_path}")
        return df
    
    except Exception as e:
        logger.exception("Failed to extract tweets from source")
        raise