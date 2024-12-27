from textblob import TextBlob
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SentimentScore:
    text: str
    polarity: float
    subjectivity: float
    timestamp: datetime

class SentimentAnalyzer:
    def analyze_tweet(self, tweet_text: str) -> SentimentScore:
        """
        Analyze the sentiment of a given tweet text
        """
        blob = TextBlob(tweet_text)
        return SentimentScore(
            text=tweet_text,
            polarity=blob.sentiment.polarity,
            subjectivity=blob.sentiment.subjectivity,
            timestamp=datetime.now()
        )

    def get_sentiment_label(self, polarity: float) -> str:
        """
        Convert polarity score to sentiment label
        """
        if polarity > 0:
            return 'Positive'
        elif polarity < 0:
            return 'Negative'
        return 'Neutral' 