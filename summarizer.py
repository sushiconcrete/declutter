import openai
import pandas as pd
from news_fetcher import fetch_news, fetch_full_article_content
from dotenv import load_dotenv
import os
load_dotenv()
# The API key is securely loaded from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def chunk_text(text, max_tokens=1500):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        current_chunk.append(word)
        current_length += 1
        if current_length >= max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0

    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def summarize_text(text, model="gpt-3.5-turbo", temperature=0.0):
    prompt = f"""
You are a professional news editor. Read the following content and produce a concise English summary:
{text}

Please output the summary in paragraph form without unnecessary details.
"""
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an AI specialized in generating concise English news summaries."},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_tokens=300,
    )
    summary = response.choices[0].message.content.strip()
    return summary

def summarize_long_text(text, model="gpt-3.5-turbo"):
    chunks = chunk_text(text, max_tokens=1500)
    partial_summaries = []

    for i, chunk in enumerate(chunks):
        print(f"\n--- Summarizing chunk {i+1}/{len(chunks)} ---")
        chunk_summary = summarize_text(chunk, model=model)
        partial_summaries.append(chunk_summary)

    merged_summary_text = "\n".join(partial_summaries)
    print("\n--- Summarizing merged partial summaries ---")
    final_summary = summarize_text(merged_summary_text, model=model)
    return final_summary


def process_articles(articles):
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
