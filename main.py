# import modules
import logging

# import my modules
import etl.extract as ext
import etl.load as ld
import etl.transform as tfm
from utils.logger import setup_logger


def main():
    setup_logger()
    logging.info("Starting ETL pipeline.")
    
    # Extract
    df_raw = ext.extract_tweets("data/twitter_disaster_data/train.csv")
    # Transform
    df_clean = tfm.transform(df_raw)
    # Load
    # ld.load_to_sqlite(df_clean, db_path="tweets.db")
    
    logging.info("ETL pipeline completed.")


if __name__ == "__main__":
    main()
