import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from urllib.parse import quote

# Parameters
SEARCHES = [
    {
        "query": "tunisie",
        "keywords": [
            "victoire", "victoires", "gagné", "gagnant", "gagnante",
            "prix", "récompense", "récompenses", "récompensé", "lauréat", "lauréate",
            "innovation", "innovations", "innovant", "innovante",
            "succès", "réussite", "réussites", "réussi", "réussis", "réussissent",
            "découverte", "découvertes", "inventé", "inventeur", "inventrice",
            "espoir", "espoirs", "encourageant", "prometteur", "prometteuse",
            "inspirant", "inspiration", "motivant", "remarquable",
            "record", "records", "nouveau record",
            "positif", "positive", "positifs", "positives", "progrès",
            "avancement", "avancées", "développement", "évolution",
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
        ],
        "lang": "fr",
        "region": "FR",
        "language_name": "French"
    },
    {
        "query": "تونس",
        "keywords": [
            "انتصار", "جائزة", "تكريم", "ابتكار", "نجاح",
            "اكتشاف", "أمل", "ملهم", "رقم قياسي", "إنجاز",
            "إيجابي", "تقدم", "افتتاح", "تحية", "إنجازات",
            "ميدالية", "ناجح", "مجد", "تمييز", "اختيار", "ترشيح",
            "تطور", "فوز", "مفيد", "تحقيق",
            "مديح", "احتفال", "أفضل", "متميز", "استثنائي"
        ],
        "lang": "ar",
        "region": "TN",
        "language_name": "Arabic"
    }
]

ONE_WEEK_AGO = datetime.now() - timedelta(days=7)
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
all_results = []

# Loop through French and Arabic configurations
for search in SEARCHES:
    query = quote(search["query"])
    keywords = search["keywords"]
    lang = search["lang"]
    region = search["region"]
    language_name = search["language_name"]

    rss_url = f"https://news.google.com/rss/search?q={query}&hl={lang}&gl={region}&ceid={region}:{lang}"
    response = requests.get(rss_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.find_all("item")

    for item in items:
        title = item.title.text.strip()
        link = item.link.text.strip()
        pub_date_str = item.pubDate.text.strip()

        try:
            pub_datetime = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %Z")
        except Exception:
            continue

        if pub_datetime < ONE_WEEK_AGO:
            continue

        # Check for keywords in title
        if any(kw in title.lower() for kw in keywords):
            all_results.append({
                "Title": title,
                "Date": pub_datetime.strftime("%Y-%m-%d"),
                "Link": link,
                "Language": language_name
            })

# Save to CSV
df = pd.DataFrame(all_results)
df.to_csv("good_news_tunisia_combined.csv", index=False, encoding="utf-8-sig")
print(f"✅ Combined CSV created with {len(df)} good news articles.")
