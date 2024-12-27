import requests
import random
from typing import List, Optional
import time

class ProxyManager:
    def __init__(self):
        self.proxies: List[str] = []
        self.last_update = 0
        self.update_interval = 3600  # Update proxy list every hour
        
    def update_proxy_list(self):
        """
        Update the proxy list from free proxy sources
        You can replace these URLs with paid proxy services for better reliability
        """
        try:
            # Free proxy list - replace with your preferred proxy service
            response = requests.get('https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt')
            if response.status_code == 200:
                self.proxies = [
                    line.strip() for line in response.text.split('\n')
                    if line.strip()
                ]
                self.last_update = time.time()
        except Exception as e:
            print(f"Error updating proxy list: {str(e)}")
            
    def get_random_proxy(self) -> Optional[str]:
        """Get a random proxy from the list"""
        if not self.proxies or time.time() - self.last_update > self.update_interval:
            self.update_proxy_list()
        
        return random.choice(self.proxies) if self.proxies else None
    
    def remove_proxy(self, proxy: str):
        """Remove a non-working proxy from the list"""
        if proxy in self.proxies:
            self.proxies.remove(proxy) 