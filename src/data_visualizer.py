import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

class DataVisualizer:
    def __init__(self):
        plt.style.use('seaborn')

    def plot_sentiment_distribution(self, sentiment_scores: list):
        """
        Create a histogram of sentiment polarities
        """
        polarities = [score.polarity for score in sentiment_scores]
        
        plt.figure(figsize=(10, 6))
        plt.hist(polarities, bins=50, color='skyblue', edgecolor='black')
        plt.title('Bitcoin Tweet Sentiment Distribution')
        plt.xlabel('Sentiment Polarity')
        plt.ylabel('Frequency')
        plt.show()

    def plot_sentiment_timeline(self, sentiment_scores: list):
        """
        Create a line plot of sentiment over time
        """
        df = pd.DataFrame([
            {
                'timestamp': score.timestamp,
                'polarity': score.polarity
            }
            for score in sentiment_scores
        ])
        
        df = df.set_index('timestamp')
        df = df.resample('1Min').mean()
        
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df.polarity, color='blue')
        plt.title('Bitcoin Sentiment Timeline')
        plt.xlabel('Time')
        plt.ylabel('Average Sentiment Polarity')
        plt.grid(True)
        plt.show() 