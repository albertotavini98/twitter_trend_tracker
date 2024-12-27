import yaml
from src.twitter_client import TwitterScraper
from src.sentiment_analyzer import SentimentAnalyzer
from src.data_visualizer import DataVisualizer
import time
from datetime import datetime

def load_config():
    with open('config/config.yaml', 'r') as file:
        return yaml.safe_load(file)

def main():
    print("\n=== Bitcoin Twitter Sentiment Analyzer Starting ===\n")
    config = load_config()
    
    # Initialize components
    print("Initializing components...")
    twitter_client = TwitterScraper()
    sentiment_analyzer = SentimentAnalyzer()
    data_visualizer = DataVisualizer()
    
    sentiment_scores = []
    iteration = 1
    
    try:
        while True:
            print(f"\n--- Iteration {iteration} starting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
            
            # Fetch tweets
            print(f"Fetching {config['twitter']['tweet_limit']} tweets about Bitcoin...")
            tweets = twitter_client.get_bitcoin_tweets(
                limit=config['twitter']['tweet_limit']
            )
            print(f"Successfully fetched {len(tweets)} tweets")
            
            # Analyze sentiments
            print("Analyzing tweet sentiments...")
            new_sentiments = 0
            for tweet in tweets:
                sentiment = sentiment_analyzer.analyze_tweet(tweet['text'])
                sentiment_scores.append(sentiment)
                new_sentiments += 1
            print(f"Analyzed {new_sentiments} new tweets")
            
            # Visualize data
            print(f"Generating visualizations for {len(sentiment_scores)} total tweets...")
            data_visualizer.plot_sentiment_distribution(sentiment_scores)
            data_visualizer.plot_sentiment_timeline(sentiment_scores)
            
            # Wait for next update
            next_update = datetime.now().timestamp() + config['sentiment']['update_interval']
            print(f"\nWaiting {config['sentiment']['update_interval']} seconds until next update...")
            print(f"Next update at: {datetime.fromtimestamp(next_update).strftime('%Y-%m-%d %H:%M:%S')}")
            
            iteration += 1
            time.sleep(config['sentiment']['update_interval'])
            
    except KeyboardInterrupt:
        print("\n\nReceived keyboard interrupt...")
        print("Gracefully shutting down...")
        print(f"Analyzed a total of {len(sentiment_scores)} tweets across {iteration-1} iterations")
        print("\n=== Bitcoin Twitter Sentiment Analyzer Stopped ===")

if __name__ == "__main__":
    main() 