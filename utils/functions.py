import json
import statsmodels
import numpy as np
from statsmodels.tsa.stattools import coint


def safe_json_load(x):
    """
        Deserializes json to a Python object
    """
    try:
        if isinstance(x, str) and x.strip().startswith('['):
            return json.loads(x)
        return x
    except json.JSONDecodeError:
        return [] 


def find_cointegrated_pairs(data, pvalue_threshold = 0.05):
    """
        Finds cointegrated stock 
    """
    n = data.shape[1]
    score_matrix = np.zeros((n, n))
    pvalue_matrix = np.ones((n, n))
    keys = data.keys()
    pairs = []
    
    for i in range(n):
        for j in range(i+1, n):
            time_series_1 = data[keys[i]]
            time_series_2 = data[keys[j]]
            
            result = coint(time_series_1, time_series_2)
            score, pvalue = result[0], result[1]
            
            score_matrix[i, j] = score
            pvalue_matrix[i, j] = pvalue
            
            if pvalue < pvalue_threshold:
                pairs.append((keys[i], keys[j]))
    
    return score_matrix, pvalue_matrix, pairs

def zscore(series):
    return (series - series.mean()) / np.std(series)

def trade(S1, S2, window1, window2):
    # window must be bigger than 0
    if (window1 == 0) or (window2 == 0):
        return 0
    
    # Rolling mean and rolling standard deviation
    ratios = S1/S2
    ma1 = ratios.rolling(window=window1, center=False).mean()
    ma2 = ratios.rolling(window=window2, center=False).mean()
    std = ratios.rolling(window=window2, center=False).std()
    
    zscore = (ma1 - ma2)/std
    
    # Simulate trading
    # Start with no money and stocks
    money = 0
    countS1 = 0
    countS2 = 0
    for i in range(len(ratios)):
        # short if the z-score is > 1
        if zscore.iloc[i] > 1:
            money += S1.iloc[i] - S2.iloc[i] * ratios.iloc[i]
            countS1 -= 1
            countS2 += ratios.iloc[i]
            
        # long if the z-score is < -1
        elif zscore.iloc[i] < -1:
            money -= S1.iloc[i] - S2.iloc[i] * ratios.iloc[i]
            countS1 += 1
            countS2 -= ratios.iloc[i]
            
        # Clear positions if the z-score in [-.5, .5]
        elif abs(zscore.iloc[i]) < 0.5:
            money += countS1 * S1.iloc[i] + S2.iloc[i] * countS2
            countS1, countS2 = 0, 0
    return money


def kalman_filter_pairs(spread, x_init, Q=0.1, R=0.1):
    """
        Applies the Kalman Filter algorithm to a time series of spread data
    """
    n = len(spread)
    #spread = data_1 - data_2
    x_hat = np.zeros(n)    # Predicted state estimate
    x_hat[0] = x_init
    P = np.zeros(n)        # Predicted error covariance
    x_hat_minus = np.zeros(n)
    P_minus = np.zeros(n)
    
    for k in range(1, n):
        # Time update
        x_hat_minus[k] = x_hat[k-1].copy()
        P_minus[k] = P[k-1].copy() + Q
        # Measurement update
        K = P_minus[k] / (P_minus[k] + R)
        x_hat[k] = x_hat_minus[k] + K * (spread[k] - x_hat_minus[k])
        P[k] = (1 - K) * P_minus[k].copy()
    return x_hat
