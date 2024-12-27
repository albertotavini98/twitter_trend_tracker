from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

print("Starting test...")
print("Setting up Chrome driver...")
service = Service(ChromeDriverManager().install())
print("Creating Chrome browser instance...")
driver = webdriver.Chrome(service=service)
print("Opening Google...")
driver.get("https://www.google.com")
print("Test successful!")
driver.quit() 