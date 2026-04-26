# Spaceflight News API Example
import requests

url = "https://api.spaceflightnewsapi.net/v4/articles"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    # Articles are usually contained in the 'results' key in v4
    articles = data.get('results', [])
    
    for article in articles:
        print(f"Title: {article['title']}")
        print(f"Source: {article['news_site']}")
        print(f"Link: {article['url']}\n")
else:
    print(f"Error: {response.status_code}")