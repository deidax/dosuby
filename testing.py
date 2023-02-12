import requests
from bs4 import BeautifulSoup

# Make a request to the website and get the HTML content
url = "https://crt.sh/?q=uca.ma"
response = requests.get(url)
html_content = response.content

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(html_content, "html.parser")

# Find the table in the HTML using the table tag and its attributes
tables = soup.find_all("table")
table = tables[1]

# Find all the rows in the table (using the tr tag)
rows = table.find_all("tr")

# Loop through each row and extract the data from each cell (using the td tag)
data = []
for row in rows:
    cells = row.find_all("td")
    # Check if there are at least 5 cells in the row
    if len(cells) >= 5:
        fifth_cell = cells[4]
        print(fifth_cell.text)

# Print the extracted data
print(data)
