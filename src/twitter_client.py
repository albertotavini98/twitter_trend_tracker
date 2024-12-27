from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from datetime import datetime
import time
import random
import chromedriver_autoinstaller
import os
from dotenv import load_dotenv

class TwitterScraper:
    def __init__(self):
        # Set delays first
        self.min_delay = 2
        self.max_delay = 5
        
        # Then load environment variables
        load_dotenv()
        self.email = os.getenv('TWITTER_EMAIL')
        self.password = os.getenv('TWITTER_PASSWORD')
        self.username = os.getenv('TWITTER_USERNAME')
        
        # Finally setup the driver
        self.setup_driver()

    def random_delay(self):
        time.sleep(random.uniform(self.min_delay, self.max_delay))

    def setup_driver(self):
        try:
            chromedriver_autoinstaller.install()
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-notifications')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-infobars')
            chrome_options.add_argument('--disable-extensions')
            
            # Add random user agent
            ua = UserAgent()
            chrome_options.add_argument(f'user-agent={ua.random}')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()  # Maximize window to ensure elements are visible
            
            # Login to Twitter
            self.login()
            
        except Exception as e:
            print(f"Error setting up Chrome driver: {str(e)}")
            raise

    def login(self):
        """Login to Twitter"""
        try:
            print("Logging in to Twitter...")
            self.driver.get("https://twitter.com/i/flow/login")
            time.sleep(5)  # Wait for page to fully load

            # Enter email
            print("Entering email...")
            email_xpath = "//input[@autocomplete='username']"
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, email_xpath))
            ).send_keys(self.email)
            time.sleep(2)

            # Click first "Avanti" button after email
            print("Clicking first Next...")
            try:
                # Try multiple selectors for the Next button
                selectors = [
                    "//div[@role='button']//span[text()='Avanti']/..",
                    "//span[text()='Avanti']/parent::div",
                    "//div[contains(@class, 'css-175oi2r')]//span[contains(text(), 'Avanti')]/..",
                    "//div[contains(@class, 'css-18t94o4')]//span[contains(text(), 'Avanti')]/.."
                ]
                
                for selector in selectors:
                    try:
                        next_button = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        next_button.click()
                        print(f"Successfully clicked using selector: {selector}")
                        break
                    except:
                        continue
                
                time.sleep(3)
            except Exception as e:
                print(f"Error clicking first Next button: {str(e)}")
                self.driver.save_screenshot("next_button_error.png")
                raise

            # Handle username verification
            print("Entering username...")
            try:
                username_field = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "text"))
                )
                username_field.send_keys(self.username)
                time.sleep(2)

                # Click second "Avanti" button after username
                print("Clicking second Next...")
                for selector in selectors:  # Use same selectors as before
                    try:
                        next_button = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        next_button.click()
                        print(f"Successfully clicked using selector: {selector}")
                        break
                    except:
                        continue
                time.sleep(3)
            except Exception as e:
                print("Username verification step skipped:", str(e))

            # Enter password
            print("Entering password...")
            password_xpath = "//input[@autocomplete='current-password']"
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, password_xpath))
            )
            password_field.send_keys(self.password)
            time.sleep(2)

            # Click "Accedi" button
            print("Clicking Login...")
            accedi_selectors = [
                "//div[@role='button']//span[text()='Accedi']/..",
                "//span[text()='Accedi']/parent::div",
                "//div[contains(@class, 'css-175oi2r')]//span[contains(text(), 'Accedi')]/..",
                "//div[contains(@class, 'css-18t94o4')]//span[contains(text(), 'Accedi')]/.."
            ]
            
            for selector in accedi_selectors:
                try:
                    login_button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    login_button.click()
                    print(f"Successfully clicked using selector: {selector}")
                    break
                except:
                    continue
            
            time.sleep(5)

            # Verify login
            print("Verifying login...")
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@data-testid='primaryColumn']"))
                )
                print("Successfully logged in to Twitter")
            except:
                print("Login verification failed. Current URL:", self.driver.current_url)
                self.driver.save_screenshot("login_error.png")
                raise Exception("Login failed")

        except Exception as e:
            print(f"Error during login: {str(e)}")
            print("Current URL:", self.driver.current_url)
            self.driver.save_screenshot("login_error.png")
            print("Screenshot saved as login_error.png")
            raise

    def get_bitcoin_tweets(self, limit=100):
        tweets = []
        search_url = "https://twitter.com/search?q=bitcoin%20OR%20%23btc%20OR%20%23bitcoin&src=typed_query&f=live"
        
        try:
            self.driver.get(search_url)
            self.random_delay()
            
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            tweet_elements = []
            scroll_attempts = 0
            max_scroll_attempts = 10
            
            while len(tweet_elements) < limit and scroll_attempts < max_scroll_attempts:
                wait = WebDriverWait(self.driver, 10)
                tweet_elements = wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, 'article[data-testid="tweet"]')
                ))
                
                for tweet in tweet_elements[:limit]:
                    try:
                        tweet_text = tweet.find_element(
                            By.CSS_SELECTOR, 
                            'div[data-testid="tweetText"]'
                        ).text
                        
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
                    except:
                        continue
                
                if len(tweets) >= limit:
                    break
                
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.random_delay()
                
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    scroll_attempts += 1
                else:
                    scroll_attempts = 0
                    last_height = new_height
                    
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
        
        return tweets[:limit]

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass 