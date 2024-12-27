import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

class DataVisualizer:
    def __init__(self):
        plt.style.use('seaborn')

    def plot_sentiment_distribution(self, sentiment_scores: list):
        """Create a dual histogram of positive and negative beliefs"""
        positive_beliefs = [score.positive_belief for score in sentiment_scores]
        negative_beliefs = [score.negative_belief for score in sentiment_scores]
        
        plt.figure(figsize=(12, 6))
        
        # Plot positive beliefs
        plt.hist(positive_beliefs, bins=20, alpha=0.5, color='green', 
                label='Positive Belief', range=(0, 1))
        
        # Plot negative beliefs
        plt.hist(negative_beliefs, bins=20, alpha=0.5, color='red', 
                label='Negative Belief', range=(0, 1))
        
        plt.title('Bitcoin Tweet Sentiment Distribution')
        plt.xlabel('Belief Score')
        plt.ylabel('Frequency')
        plt.legend()
        plt.show()

    def plot_sentiment_timeline(self, sentiment_scores: list):
        """Create a line plot of sentiment beliefs over time"""
        df = pd.DataFrame([
            {
                'timestamp': score.timestamp,
                'positive_belief': score.positive_belief,
                'negative_belief': score.negative_belief
            }
            for score in sentiment_scores
        ])
        
        df = df.set_index('timestamp')
        df = df.resample('1Min').mean()
        
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df.positive_belief, color='green', label='Positive Belief')
        plt.plot(df.index, df.negative_belief, color='red', label='Negative Belief')
        plt.title('Bitcoin Sentiment Timeline')
        plt.xlabel('Time')
        plt.ylabel('Belief Score')
        plt.legend()
        plt.grid(True)
        plt.show() 