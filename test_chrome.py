from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller

print("Checking Chrome version...")
chromedriver_autoinstaller.install()  # This will install the correct chromedriver version

print("Setting up Chrome driver...")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')

print("Creating driver...")
driver = webdriver.Chrome(options=chrome_options)

print("Testing connection...")
driver.get("https://www.google.com")
print("Title:", driver.title)

print("Closing driver...")
driver.quit()
print("Test completed successfully!") 