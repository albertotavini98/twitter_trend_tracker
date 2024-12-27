from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from datetime import datetime
import time
import random
from .proxy_manager import ProxyManager

class TwitterScraper:
    def __init__(self):
        self.proxy_manager = ProxyManager()
        self.current_proxy = None
        self.setup_driver()
        self.min_delay = 2
        self.max_delay = 5

    def random_delay(self):
        """Add random delay between actions to avoid detection"""
        time.sleep(random.uniform(self.min_delay, self.max_delay))

    def setup_driver(self):
        """Setup Chrome driver with rotating proxies and user agents"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Add random user agent
        ua = UserAgent()
        chrome_options.add_argument(f'user-agent={ua.random}')
        
        # Add proxy if available
        self.current_proxy = self.proxy_manager.get_random_proxy()
        if self.current_proxy:
            chrome_options.add_argument(f'--proxy-server={self.current_proxy}')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def rotate_proxy(self):
        """Rotate to a new proxy and restart the driver"""
        if self.current_proxy:
            self.proxy_manager.remove_proxy(self.current_proxy)
        self.driver.quit()
        self.setup_driver()

    def get_bitcoin_tweets(self, limit=100):
        """
        Scrape recent tweets about Bitcoin with proxy rotation and delay
        """
        max_retries = 3
        tweets = []
        search_url = "https://twitter.com/search?q=bitcoin%20OR%20%23btc%20OR%20%23bitcoin&src=typed_query&f=live"
        
        for attempt in range(max_retries):
            try:
                self.driver.get(search_url)
                self.random_delay()
                
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                tweet_elements = []
                scroll_attempts = 0
                max_scroll_attempts = 10
                
                while len(tweet_elements) < limit and scroll_attempts < max_scroll_attempts:
                    # Wait for tweets to load
                    wait = WebDriverWait(self.driver, 10)
                    tweet_elements = wait.until(EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, 'article[data-testid="tweet"]')
                    ))
                    
                    # Extract tweet data
                    for tweet in tweet_elements[:limit]:
                        try:
                            tweet_text = tweet.find_element(
                                By.CSS_SELECTOR, 
                                'div[data-testid="tweetText"]'
                            ).text
                            
                            # Try to get timestamp if available
                            try:
                                time_element = tweet.find_element(
                                    By.CSS_SELECTOR,
                                    'time'
                                )
                                timestamp = time_element.get_attribute('datetime')
                                tweet_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                            except:
                                tweet_time = datetime.now()
                            
                            tweets.append({
                                'text': tweet_text,
                                'created_at': tweet_time
                            })
                        except Exception as e:
                            print(f"Error extracting tweet: {str(e)}")
                            continue
                    
                    if len(tweets) >= limit:
                        break
                    
                    # Scroll with random delay
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    self.random_delay()
                    
                    new_height = self.driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        scroll_attempts += 1
                    else:
                        scroll_attempts = 0
                        last_height = new_height
                
                break  # If successful, break the retry loop
                
            except Exception as e:
                print(f"Error during scraping (attempt {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    print("Rotating proxy and retrying...")
                    self.rotate_proxy()
                else:
                    print("Max retries reached. Some tweets may be missing.")
        
        return tweets[:limit]

    def __del__(self):
        """Clean up the driver when done"""
        try:
            self.driver.quit()
        except:
            pass 