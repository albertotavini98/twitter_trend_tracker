from textblob import TextBlob
from dataclasses import dataclass
from datetime import datetime
import re
from typing import Tuple

@dataclass
class SentimentScore:
    text: str
    positive_belief: float  # Score between 0 and 1
    negative_belief: float  # Score between 0 and 1
    timestamp: datetime

class SentimentAnalyzer:
    def __init__(self):
        # Keywords that indicate positive/negative sentiment about Bitcoin
        self.positive_words = {
            'bullish', 'buy', 'up', 'gain', 'profit', 'moon', 'rise', 'rising',
            'growth', 'growing', 'strong', 'strength', 'higher', 'rally', 'good',
            'positive', 'success', 'winning', 'win', 'better', 'best', 'great',
            'moon', 'hodl', 'hold', 'accumulate', 'accumulation', 'support'
        }
        
        self.negative_words = {
            'bearish', 'sell', 'down', 'loss', 'crash', 'fall', 'falling',
            'drop', 'dropping', 'weak', 'weakness', 'lower', 'dump', 'bad',
            'negative', 'fail', 'failing', 'worse', 'worst', 'poor', 'death',
            'bear', 'resistance', 'correction', 'fear', 'panic', 'risk'
        }

    def preprocess_text(self, text: str) -> str:
        """Clean and normalize text"""
        text = text.lower()
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)  # Remove URLs
        text = re.sub(r'@\w+', '', text)  # Remove mentions
        text = re.sub(r'#', '', text)  # Remove hashtag symbol but keep the text
        return text

    def calculate_belief_scores(self, text: str) -> Tuple[float, float]:
        """Calculate positive and negative belief scores"""
        words = set(self.preprocess_text(text).split())
        
        # Count matches with positive and negative word sets
        positive_matches = len(words.intersection(self.positive_words))
        negative_matches = len(words.intersection(self.negative_words))
        
        # Calculate basic scores
        total_matches = positive_matches + negative_matches
        if total_matches == 0:
            return 0.5, 0.5  # Neutral when no sentiment words found
        
        # Convert to probabilities
        positive_belief = positive_matches / (total_matches + 1)  # Add 1 for smoothing
        negative_belief = negative_matches / (total_matches + 1)
        
        # Normalize to ensure they sum to 1
        total = positive_belief + negative_belief
        if total > 0:
            positive_belief = positive_belief / total
            negative_belief = negative_belief / total
        
        return positive_belief, negative_belief

    def analyze_tweet(self, tweet_text: str) -> SentimentScore:
        """Analyze the sentiment of a given tweet text"""
        positive_belief, negative_belief = self.calculate_belief_scores(tweet_text)
        
        return SentimentScore(
            text=tweet_text,
            positive_belief=positive_belief,
            negative_belief=negative_belief,
            timestamp=datetime.now()
        )

    def get_sentiment_label(self, positive_belief: float, negative_belief: float) -> str:
        """Convert belief scores to sentiment label"""
        if positive_belief > 0.6:
            return 'Positive'
        elif negative_belief > 0.6:
            return 'Negative'
        return 'Neutral' 