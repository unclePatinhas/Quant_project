# import modules
import logging
import pandas as pd 

# import my modules
import etl.extract as ext
import etl.load as ld
import etl.transform as tfm
from utils.logger import setup_logger


def main():
    setup_logger()
    logging.info("Starting ETL pipeline.")
    
    # Extract
    df_raw = ext.extract_tweets("data/stock_tweets/tweets.csv")
    df_ticker = ext.extract_tweets("data/stock_tweets/company_tweet.csv") # tweet_id,ticker_symbol
    df_ticker_tweet = pd.merge(df_raw, df_ticker, on="tweet_id", how = "inner")

    # Transform
    df_clean_valid, _ = tfm.transform(df_ticker_tweet)
    
    # Load
    ld.load_to_sqlite(df_clean_valid, db_path="data/stock_tweets.db")
    
    logging.info("ETL pipeline completed.")


if __name__ == "__main__":
    main()
