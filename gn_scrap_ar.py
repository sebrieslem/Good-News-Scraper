import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from urllib.parse import quote

# Parameters
SEARCH_QUERY = "تونس"
KEYWORDS = [
    "انتصار", "جائزة", "تكريم", "ابتكار", "نجاح",
    "اكتشاف", "أمل", "ملهم", "رقم قياسي", "إنجاز",
    "إيجابي", "تقدم", "افتتاح", "تحية", "إنجازات",
    "ميدالية", "ناجح", "مجد", "تمييز", "اختيار", "ترشيح",
    "تطور", "فوز", "مفيد", "تحقيق",
 "ميدالية", "تميّز","تتويج", "احتفال", "أفضل", "متميز", "استثنائي"
]

ONE_WEEK_AGO = datetime.now() - timedelta(days=7)

# RSS Feed URL for Google News (Arabic language)
RSS_URL = f"https://news.google.com/rss/search?q={quote(SEARCH_QUERY)}&hl=ar&gl=TN&ceid=TN:ar"

# Send request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
response = requests.get(RSS_URL, headers=headers)
soup = BeautifulSoup(response.content, features="xml")
items = soup.find_all("item")

# Extract and filter news
results = []

for item in items:
    title = item.title.text
    link = item.link.text
    pub_date_str = item.pubDate.text

    # Convert pubDate to datetime object
    try:
        pub_datetime = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %Z")
    except Exception:
        continue

    # Filter by date
    if pub_datetime < ONE_WEEK_AGO:
        continue

    # Filter by Arabic keywords
    title_stripped = title.strip()
    if any(keyword in title_stripped for keyword in KEYWORDS):
        results.append({
            "Title": title_stripped,
            "Date": pub_datetime.strftime("%Y-%m-%d"),
            "Link": link
        })

# Save to CSV
df = pd.DataFrame(results)
df.to_csv("good_news_arabic_tunisia.csv", index=False, encoding="utf-8-sig")
print("✅ CSV file created with", len(df), "good news articles in Arabic.")
