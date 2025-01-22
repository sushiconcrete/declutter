import os
from dotenv import load_dotenv
import requests
import pandas as pd
from bs4 import BeautifulSoup
load_dotenv()
API_KEY = os.getenv("NEWSAPI_API_KEY")
print(API_KEY)
BASE_URL = "https://newsapi.org/v2/everything"
VALID_SORT_OPTIONS = ["relevancy", "popularity", "publishedAt"]


def fetch_news(query, target_count=5, sort_by="relevancy"):
    if sort_by not in VALID_SORT_OPTIONS:
        print(f"Invalid sortBy value: {sort_by}. Using default 'relevancy'.")
        sort_by = "relevancy"

    valid_articles = []
    page = 1
    page_size = target_count * 2  # Fetch extra to account for filtering

    while len(valid_articles) < target_count:
        params = {
            "q": query,
            "apiKey": API_KEY,
            "pageSize": page_size,
            "page": page,
            "language": "en",
            "sortBy": sort_by,
        }
        try:
            response = requests.get(BASE_URL, params=params)
            if response.status_code == 200:
                articles = response.json().get("articles", [])
                valid_articles.extend(filter_removed_links(articles))
                if not articles:  # If no more articles are available
                    break
            else:
                print(f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}")
                break
        except requests.RequestException as e:
            print(f"An error occurred while fetching news: {e}")
            break

        page += 1

    return valid_articles[:target_count]  # Ensure exactly target_count articles


def filter_removed_links(articles):
    valid_articles = []
    for article in articles:
        title = article.get("title", "")
        url = article.get("url")
        if (
            "[Removed]" not in title
            and url
            and "consent.yahoo.com" not in url
        ):
            valid_articles.append(article)
    return valid_articles


def fetch_full_article_content(url):
    """Scrape full article content from the provided URL."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # Extract paragraphs or main content (adjust the selector based on the site's structure)
            paragraphs = soup.find_all("p")
            full_content = " ".join([p.get_text() for p in paragraphs])
            return full_content
        else:
            print(f"Failed to fetch content. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching article content: {e}")
        return None


def process_articles_to_df(articles):
    """Process a list of articles into a structured DataFrame.
    
    Args:
        articles (list): List of article dictionaries containing metadata
        
    Returns:
        pd.DataFrame: DataFrame containing processed article data
    """
    articles_data = []
    
    for article in articles:
        # Fetch metadata
        title = article.get("title", "")
        url = article.get("url", "")
        published_at = article.get("publishedAt", "")

        # Fetch full content
        full_content = fetch_full_article_content(url)

        # Append to the data list
        articles_data.append({
            "Title": title,
            "URL": url,
            "Published At": published_at,
            "Full Content": full_content
        })
    
    # Convert the list of dictionaries to a DataFrame
    return pd.DataFrame(articles_data)