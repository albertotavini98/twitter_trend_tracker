import yaml
from src.twitter_client import TwitterScraper
from src.sentiment_analyzer import SentimentAnalyzer
from src.data_visualizer import DataVisualizer
import time

def load_config():
    with open('config/config.yaml', 'r') as file:
        return yaml.safe_load(file)

def main():
    config = load_config()
    
    # Initialize components
    twitter_client = TwitterScraper()
    sentiment_analyzer = SentimentAnalyzer()
    data_visualizer = DataVisualizer()
    
    sentiment_scores = []
    
    try:
        while True:
            # Fetch tweets
            tweets = twitter_client.get_bitcoin_tweets(
                limit=config['twitter']['tweet_limit']
            )
            
            # Analyze sentiments
            for tweet in tweets:
                sentiment = sentiment_analyzer.analyze_tweet(tweet['text'])
                sentiment_scores.append(sentiment)
            
            # Visualize data
            data_visualizer.plot_sentiment_distribution(sentiment_scores)
            data_visualizer.plot_sentiment_timeline(sentiment_scores)
            
            # Wait for next update
            time.sleep(config['sentiment']['update_interval'])
            
    except KeyboardInterrupt:
        print("\nGracefully shutting down...")

if __name__ == "__main__":
    main() 