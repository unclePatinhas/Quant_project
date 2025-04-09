
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import gaussian_kde


def column_dist(df, column_name, ticker_symbol="stock", 
                bins=50, describe=True, kde=True):
    data = df[column_name].dropna()

    if describe:
        print(data.describe())

    fig = go.Figure()

    # KDE calculation first
    if kde and len(data) > 1:
        kde_func = gaussian_kde(data)
        x_kde = np.linspace(data.min(), data.max(), 200)
        y_kde = kde_func(x_kde)

        fig.add_trace(go.Scatter(
            x=x_kde,
            y=y_kde,
            mode='lines',
            name='PDF',
            line=dict(color='green', width=2)
        ))

    # Histogram (normalized)
    fig.add_trace(go.Histogram(
        x=data,
        nbinsx=bins,
        name='Histogram',
        marker_color='blue',
        opacity=0.6,
        histnorm='probability density',  # Matches KDE scaling
    ))

    fig.update_layout(
        title=f"Distribution of {column_name} for {ticker_symbol}",
        xaxis_title=column_name,
        yaxis_title='Density',
        bargap=0.05,
        template='plotly_white',
        width=800,
        height=500
    )

    fig.show()
    
def sentiment_overtime(tweet_df, stock_df, title, score_column_name="score"):
    print("\n\n")
    
    fig = go.Figure()

    # Vertical lines for sentiment
    for i in range(len(tweet_df)):
        fig.add_trace(go.Scatter(
            x=[tweet_df['day_date'].iloc[i], tweet_df['day_date'].iloc[i]],
            y=[0, tweet_df[score_column_name].iloc[i]],
            mode='lines',
            line=dict(color='blue', width=1),
            name='Sentiment' if i == 0 else None,
            yaxis='y1'
        ))

    # Horizontal zero line
    fig.add_trace(go.Scatter(
        x=[tweet_df['day_date'].min(), tweet_df['day_date'].max()],
        y=[0, 0],
        mode='lines',
        line=dict(color='red', dash='dash'),
        name='Zero Line',
        yaxis='y1'
    ))

    # Stock price line
    fig.add_trace(go.Scatter(
        x=stock_df['day_date'],
        y=stock_df['close'],
        mode='lines',
        name='Stock Price',
        line=dict(color='orange', width=2),
        yaxis='y2'
    ))

    # Layout with updated property paths
    fig.update_layout(
        title=f"Effects of {title} tweets on stock price",
        xaxis=dict(title='Post Date'),
        yaxis=dict(
            title=dict(text='Sentiment Score', font=dict(color='blue')),
            tickfont=dict(color='blue')
        ),
        yaxis2=dict(
            title=dict(text='Stock Price', font=dict(color='orange')),
            tickfont=dict(color='orange'),
            anchor='x',
            overlaying='y',
            side='right'
        ),
        showlegend=False,
        legend=dict(x=0.01, y=0.99),
        template='plotly_white',
        width=1000,
        height=600
    )

    fig.show()
    
def draw_stock_price_with_sentiment(tweet_df, stock_df, start_day, end_day, 
                                    ticker_symbols, score_name="score"):
    for ticker_symbol in ticker_symbols:
        print(f"Stock price of the company with ticker symbol is {ticker_symbol}")

        sub_tweet_df = tweet_df[tweet_df["ticker_symbol"] == ticker_symbol]
        sub_tweet_df = sub_tweet_df[(sub_tweet_df["day_date"]>=pd.to_datetime(start_day)) & (sub_tweet_df["day_date"]<=pd.to_datetime(end_day))]
    #     print(sub_tweet_df[:5])
        sub_stock_df = stock_df[stock_df["ticker_symbol"] == ticker_symbol]
        sub_stock_df = sub_stock_df[(sub_stock_df["day_date"]>=pd.to_datetime(start_day)) & (sub_stock_df["day_date"]<=pd.to_datetime(end_day))]

    #     print(sub_stock_df[:5])
        sentiment_overtime(sub_tweet_df, sub_stock_df, title=ticker_symbol, score_column_name=score_name)
        
def heatmapp_vals(stock_tic, pvalues):
    # Mask values >= 0.999
    pvalues[pvalues >= 0.999] = np.nan

    fig = go.Figure(data=go.Heatmap(
        x=stock_tic,
        y=stock_tic,
        z=pvalues, 
        colorscale='RdYlGn_r',
        colorbar=dict(title='p-value'),
        zmin=0,
        zmax=1,
        hovertemplate='x: %{x}<br>y: %{y}<br>p: %{z:.4f}<extra></extra>'
        ))

    fig.update_layout(
        title='P-Value Heatmap',
        width=500,
        height=500,
        xaxis_title='Stock',
        yaxis_title='Stock'
    )

    fig.show()

def price_ratio(ratios):
    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(
        x=ratios.index,
        y=ratios.values,
        mode='lines',
        name='Price Ratio'
    ))

    fig1.add_trace(go.Scatter(
        x=ratios.index,
        y=[ratios.mean()] * len(ratios),
        mode='lines',
        name='Mean',
        line=dict(dash='dash', color='gray')
    ))

    fig1.update_layout(
        title='Price Ratio',
        width=1000,
        height=500,
        showlegend=True
    )

    fig1.show()

def zscore_ratio(z):

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=z.index,
        y=z.values,
        mode='lines',
        name='Ratio z-score'
    ))

    fig2.add_trace(go.Scatter(
        x=z.index,
        y=[0] * len(z),
        mode='lines',
        name='Mean',
        line=dict(color='black')
    ))

    fig2.add_trace(go.Scatter(
        x=z.index,
        y=[1.0] * len(z),
        mode='lines',
        name='+1',
        line=dict(color='red', dash='dash')
    ))

    fig2.add_trace(go.Scatter(
        x=z.index,
        y=[-1.0] * len(z),
        mode='lines',
        name='-1',
        line=dict(color='green', dash='dash')
    ))

    fig2.update_layout(
        title='Z-score of Price Ratio',
        width=1000,
        height=500,
        showlegend=True
    )

    fig2.show()
    
def ratio_mv_avg(train, ratios_mavg_fast, ratios_mavg_slow, fast_name, slow_name):
    fig = go.Figure()

    # Add main ratio
    fig.add_trace(go.Scatter(
        x=train.index,
        y=train.values,
        mode='lines',
        name='Ratio'
    ))

    # Add fast moving average
    fig.add_trace(go.Scatter(
        x=ratios_mavg_fast.index,
        y=ratios_mavg_fast.values,
        mode='lines',
        name=f'{fast_name} days Ratio MA'
    ))

    # Add slow moving average
    fig.add_trace(go.Scatter(
        x=ratios_mavg_slow.index,
        y=ratios_mavg_slow.values,
        mode='lines',
        name=f'{slow_name} days Ratio MA'
    ))

    # Layout customization
    fig.update_layout(
        title='Ratio with Moving Averages',
        xaxis_title='Date',
        yaxis_title='Ratio',
        width=1000,
        height=500,
        showlegend=True
    )

    fig.show()

def rolling_ratio_zscore(zscore_slow_fast):
    
    fig = go.Figure()
    # Main rolling z-score line
    fig.add_trace(go.Scatter(
        x=zscore_slow_fast.index,
        y=zscore_slow_fast.values,
        mode='lines',
        name='Rolling Ratio z-Score'
    ))

    # Horizontal lines for mean and thresholds
    fig.add_trace(go.Scatter(
        x=zscore_slow_fast.index,
        y=[0] * len(zscore_slow_fast),
        mode='lines',
        name='Mean',
        line=dict(color='black')
    ))

    fig.add_trace(go.Scatter(
        x=zscore_slow_fast.index,
        y=[1.0] * len(zscore_slow_fast),
        mode='lines',
        name='+1',
        line=dict(color='red', dash='dash')
    ))

    fig.add_trace(go.Scatter(
        x=zscore_slow_fast.index,
        y=[-1.0] * len(zscore_slow_fast),
        mode='lines',
        name='-1',
        line=dict(color='green', dash='dash')
    ))

    # Layout customization
    fig.update_layout(
        title='Rolling Ratio z-Score',
        xaxis_title='Date',
        yaxis_title='Z-Score',
        width=1000,
        height=500,
        showlegend=True
    )

    fig.show()
    
def buy_sell_sgn(train_plot, buy_plot, sell_plot, ratios):
    fig = go.Figure()

    # Plot main ratio line
    fig.add_trace(go.Scatter(
        x=train_plot.index,
        y=train_plot.values,
        mode='lines',
        name='Ratio'
    ))

    # Plot buy signals as green triangles
    fig.add_trace(go.Scatter(
        x=buy_plot.index,
        y=buy_plot.values,
        mode='markers',
        name='Buy Signal',
        marker=dict(color='green', symbol='triangle-up', size=10)
    ))

    # Plot sell signals as red triangles
    fig.add_trace(go.Scatter(
        x=sell_plot.index,
        y=sell_plot.values,
        mode='markers',
        name='Sell Signal',
        marker=dict(color='red', symbol='triangle-down', size=10)
    ))

    # Custom axis range
    fig.update_yaxes(range=[ratios.min(), ratios.max()])

    # Layout styling
    fig.update_layout(
        title='Ratio with Buy/Sell Signals',
        xaxis_title='Date',
        yaxis_title='Ratio',
        width=1000,
        height=500,
        showlegend=True
    )

    fig.show()
    

def pair_trading_signals(dates, S1, S2, buyR, sellR):
    
    fig = go.Figure()
    # Plot AAPL
    fig.add_trace(go.Scatter(
        x=dates,
        y=S1,
        mode='lines',
        name='AAPL',
        line=dict(color='blue')
    ))

    # Plot GOOGL
    fig.add_trace(go.Scatter(
        x=dates,
        y=S2,
        mode='lines',
        name='GOOGL',
        line=dict(color='darkblue')
    ))

    # Plot Buy signals
    fig.add_trace(go.Scatter(
        x=buyR.dropna().index,
        y=buyR.dropna().values,
        mode='markers',
        name='Buy Signal',
        marker=dict(color='green', symbol='triangle-up', size=12)
    ))

    # Plot Sell signals
    fig.add_trace(go.Scatter(
        x=sellR.dropna().index,
        y=sellR.dropna().values,
        mode='markers',
        name='Sell Signal',
        marker=dict(color='red', symbol='triangle-down', size=12)
    ))

    # Match the axis range
    min_y = min(S1.min(), S2.min())
    max_y = max(S1.max(), S2.max())

    fig.update_layout(
        title="Pair Trading: AAPL vs GOOGL with Buy/Sell Signals",
        xaxis_title="Date",
        yaxis=dict(title="Price", range=[min_y, max_y]),
        template='plotly_white',
        width=1000,
        height=600,
        legend=dict(x=0.01, y=0.99)
    )

    fig.show()
    
def pnl(length_scores, length_scores2):
    fig = go.Figure()

    # Training scores
    fig.add_trace(go.Scatter(
        x=list(range(len(length_scores))),
        y=length_scores,
        mode='lines+markers',
        name='Training',
        line=dict(color='blue')
    ))

    # Test scores
    fig.add_trace(go.Scatter(
        x=list(range(len(length_scores2))),
        y=length_scores2,
        mode='lines+markers',
        name='Test',
        line=dict(color='purple')
    ))

    # Layout settings
    fig.update_layout(
        title='Score vs Window Length',
        xaxis_title='Window length',
        yaxis_title='PnL',
        width=1000,
        height=500,
        template='plotly_white',
        legend=dict(x=0.01, y=0.99)
    )

    fig.show()
