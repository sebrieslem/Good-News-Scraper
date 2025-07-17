import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from urllib.parse import quote

# Parameters
SEARCH_QUERY = "tunisie"
KEYWORDS = [
    "victoire", "prix", "récompense", "innovation", "succès",
    "découverte", "espoir", "inspirant", "record", "réussite",
    "positif", "avancement", "inauguration", "hommage", "exploit",
    "médaille", "réussis", "gloire", "distinction", "élu", "nomination"
]
ONE_WEEK_AGO = datetime.now() - timedelta(days=7)

# RSS Feed URL for Google News
RSS_URL = f"https://news.google.com/rss/search?q={quote(SEARCH_QUERY)}&hl=fr&gl=FR&ceid=FR:fr"

# Send request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
response = requests.get(RSS_URL, headers=headers)
soup = BeautifulSoup(response.content, "xml")
items = soup.find_all("item")

print(f"\n🔍 Total articles fetched: {len(items)}\n")

results = []

for item in items:
    title = item.title.text
    link = item.link.text
    pub_date_str = item.pubDate.text

    # Parse date
    try:
        pub_datetime = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %Z")
    except Exception as e:
        print(f"⚠️ Date parse error: {e}")
        continue

    if pub_datetime < ONE_WEEK_AGO:
        continue

    print("📰", title)

    # Show matching keywords (debug)
    matched_keywords = [kw for kw in KEYWORDS if kw in title.lower()]
    if matched_keywords:
        print(f"✅ Matched keywords: {matched_keywords}")
    else:
        print("❌ No keyword match")

    # TEMP: Add all articles from the past week regardless of keywords (for testing)
    results.append({
        "Title": title,
        "Date": pub_datetime.strftime("%Y-%m-%d"),
        "Link": link
    })

# Save to CSV
df = pd.DataFrame(results)
df.to_csv("good_news_tunisia_TEST.csv", index=False, encoding="utf-8")

print(f"\n📁 CSV saved with {len(df)} recent news articles (filtered by date only).")
