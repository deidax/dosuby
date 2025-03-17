import requests
from bs4 import BeautifulSoup

class CrtSearch():
    
    
    
    def search(self, query: str):
        base_url="https://crt.sh/?q={}".format(query)
        response = requests.get(base_url)
        html_content = response.content

        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(html_content, "html.parser")

        # Find the table in the HTML using the table tag and its attributes
        tables = soup.find_all("table")
        table = tables[1]

        # Find all the rows in the table (using the tr tag)
        rows = table.find_all("tr")
        
        for row in rows:
            yield row