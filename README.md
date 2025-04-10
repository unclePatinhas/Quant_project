# Navigating the project
While I am still organizing and cleaning the code, the jupiter notebook *Trading_model.ipynb* is the easiest way to start.

After downloading the data (see Tweets below), running *!python main.py* launches the ETL, it then creates a database *stock_tweets.db* containing the pre-processed data.

Then the project is organized in the foloowing steps
1. EDA and feature engineering of tweet data. (Need to implement features based on likes and re-tweets)

2. Pair trading - here we find cointegrated stocks and build trading signals using the z-score of the stock prices ration. (Need to debug the filtered spread from KL, due to missing data, and check if improves the PnL)

3. Integrate both text features and pair trading signals to improve the strategy (still in progress)

4. Implement the strategy with real-time data. (websockets)

## To create the required environment and installing dependencies do:
uv sync

## Tweets data
Should be downloaded from <https://www.kaggle.com/datasets/omermetinn/tweets-about-the-top-companies-from-2015-to-2020> and put under *data/stock_tweets*

## To run uniitests
python -m unittest discover tests


## Create the venv, using uv:
uv init --app --python 3.13.1
uv run main.py


