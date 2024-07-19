# webcrawler.py
from bs4 import BeautifulSoup
import requests

class WebCrawler:
    def __init__(self):
        self.search_engines = ["https://www.google.com/search?q=", "https://www.bing.com/search?q="]

    def search_web(self, query):
        results = []
        for engine in self.search_engines:
            response = requests.get(engine + query)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [a.get('href') for a in soup.find_all('a') if a.get('href')]
            results.extend(links)
        return results

    def find_solutions(self, issue):
        query = f"fix for {issue}"
        results = self.search_web(query)
        return results
