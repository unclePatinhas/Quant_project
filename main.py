# import modules
import logging
import pandas as pd 
import sqlite3

# import my modules
import etl.extract as ext
import etl.load as ld
import etl.transform as tfm
from utils.logger import setup_logger
from utils.functions import safe_json_load



def main():
    setup_logger()
    
    # ETL --------------------------------------------------------- #
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

    # Get processed data ----------------------------------------- #
    logging.info("Get processed data from database.")
    # Read sqlite query results into a pandas DataFrame
    conn = sqlite3.connect("data/stock_tweets.db")
    df = pd.read_sql_query("SELECT * from processed_tweets", conn)
    df['tokens'] = df['tokens'].apply(safe_json_load) # Loads serialized json string to array
    conn.close()
    logging.info("Done fetching processed data from database.")
    
    # Feature Engineering ----------------------------------------- #
    #logging.info("Starting Features engineering.")
    


if __name__ == "__main__":
    main()
