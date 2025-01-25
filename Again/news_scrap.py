from requests_html import HTMLSession
import sqlite3
import sys

# Ensure UTF-8 encoding for stdout
sys.stdout.reconfigure(encoding='utf-8')

# URL to scrape
url = "https://www.dailynayadiganta.com/"

# Create a session and fetch the page
session = HTMLSession()
response = session.get(url)

# Render the page (for dynamic content)
# response.html.render(timeout=20)

# Debug: Print the HTML content
print("Page Content:")
print(response.html.html[:1000])  # Print only the first 1000 characters for brevity

# Fetch title
title_element = response.html.find('h2', first=True)
title = title_element.text if title_element else "Title not found"

# Fetch category
category_element = response.html.find('div', first=True)
category = (
    category_element.find('a', first=True).text
    if category_element else "Category not found"
)

# Fetch datetime
#datetime_element = response.html.find('div', first=True)
#news_datetime = (
##    datetime_element.attrs['span'] if datetime_element else "Datetime not found"
#)

# Fetch reporter
reporter_element = response.html.find('.contributor-name', first=True)
reporter = reporter_element.text if reporter_element else "Reporter not found"

# Fetch news body
news_body_elements = response.html.find('p')
news_body = "\n".join([p.text for p in news_body_elements]) if news_body_elements else "News body not found"

# Print results
print("Title:", title)
print("Category:", category)
#print("Datetime:", news_datetime)
print("Reporter:", reporter)
print("News Body:", news_body)