import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from urllib.parse import quote

# Parameters
SEARCH_QUERY = "tunisie"
KEYWORDS = [
    "victoire", "victoires", "gagné", "gagnant", "gagnante",
    "prix", "récompense", "récompenses", "récompensé", "lauréat", "lauréate",
    "innovation", "innovations", "innovant", "innovante",
    "succès", "réussite", "réussites", "réussi", "réussis", "réussissent",
    "découverte", "découvertes", "inventé", "inventeur", "inventrice",
    "espoir", "espoirs", "encourageant", "prometteur", "prometteuse",
    "inspirant", "inspiration", "motivant", "remarquable",
    "record", "records", "nouveau record",
    "positif", "positive", "positifs", "positives", "progrès",
    "avancement", "avancées", "progrès", "développement", "évolution",
    "inauguration", "lancement", "démarrage", "ouverture officielle",
    "hommage", "exploit", "exploit sportif", "exploit scientifique",
    "médaille", "médailles", "médaillé", "médaillée",
    "gloire", "distinction", "distinctions", "honoré", "honorée",
    "élu", "élue", "nommé", "nomination",
    "champion", "championne", "championnat", "trophée",
    "partenariat", "collaboration", "subvention", "financement",
    "jeunesse", "engagement", "solidarité", "résilience",
    "victoire historique", "avancée majeure", "bonne nouvelle", "succès tunisien",
    "projet réussi", "réforme réussie", "espoir pour", "première fois"
]

ONE_WEEK_AGO = datetime.now() - timedelta(days=7)

# RSS Feed URL for Google News
RSS_URL = f"https://news.google.com/rss/search?q={quote(SEARCH_QUERY)}&hl=fr&gl=FR&ceid=FR:fr"

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

    # Filter by keywords
    title_lower = title.lower()
    if any(keyword in title_lower for keyword in KEYWORDS):
        results.append({
            "Title": title,
            "Date": pub_datetime.strftime("%Y-%m-%d"),
            "Link": link
        })

# Save to CSV
df = pd.DataFrame(results)
df.to_csv("good_news_tunisia.csv", index=False, encoding="utf-8")
print("✅ CSV file created with", len(df), "good news articles.")
