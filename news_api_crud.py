import requests
import json
from datetime import datetime, timedelta

# API bilgileri
API_KEY = "f7879c8127cd4f83a0fcd9e36644f019"
BASE_URL = "https://newsapi.org/v2/everything"

# Haberleri saklamak için bir liste (Veritabanı gibi çalışacak)
news_db = []

# Haberleri API'den çekme fonksiyonu
def get_news(query="bitcoin", from_date=None, to_date=None):
    params = {
        "q": query,
        "apiKey": API_KEY,
        "from": from_date,
        "to": to_date,
        "language": "en",
        "sortBy": "publishedAt",
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data["articles"]
    else:
        print(f"Hata: {response.status_code}")
        return []

# 📌 CRUD İşlemleri

# ✅ CREATE - Haber ekleme
def create_news(article):
    news_db.append(article)
    return "✅ Haber başarıyla eklendi."

# ✅ READ - Tüm haberleri listeleme
def read_news():
    return news_db

# ✅ UPDATE - Belirli bir haberi güncelleme
def update_news(index, updated_article):
    if 0 <= index < len(news_db):
        news_db[index] = updated_article
        return "✅ Haber başarıyla güncellendi."
    return "❌ Hata: Geçersiz indeks."

# ✅ DELETE - Belirli bir haberi silme
def delete_news(index):
    if 0 <= index < len(news_db):
        deleted_news = news_db.pop(index)
        return f"✅ Haber başarıyla silindi: {deleted_news['title']}"
    return "❌ Hata: Geçersiz indeks."

# 🔍 Günlük haber çekme
def get_daily_news(query="bitcoin"):
    today = datetime.today().strftime('%Y-%m-%d')
    return get_news(query, from_date=today, to_date=today)

# 📅 Haftalık haber çekme
def get_weekly_news(query="bitcoin"):
    today = datetime.today()
    last_week = today - timedelta(days=7)
    return get_news(query, from_date=last_week.strftime('%Y-%m-%d'), to_date=today.strftime('%Y-%m-%d'))

# 🗓️ Aylık haber çekme
def get_monthly_news(query="bitcoin"):
    today = datetime.today()
    last_month = today - timedelta(days=30)
    return get_news(query, from_date=last_month.strftime('%Y-%m-%d'), to_date=today.strftime('%Y-%m-%d'))

# Örnek Kullanım
if __name__ == "__main__":
    print("\n🔍 Günlük Haberler (İlk 5 Haber):")
    daily_news = get_daily_news()
    for i, news in enumerate(daily_news[:5]):  # İlk 5 haberi yazdıralım
        print(f"{i+1}. {news['title']} - {news['publishedAt']}")
        create_news(news)  # Veritabanına ekleyelim

    print("\n📜 Kaydedilen Haberler:")
    print(json.dumps(read_news(), indent=2, ensure_ascii=False))

    # Haber Güncelleme (Örnek: İlk haberi güncelle)
    if news_db:
        print("\n✏️ İlk haberi güncelliyoruz...")
        updated_article = news_db[0].copy()
        updated_article["title"] = "📌 [GÜNCELLENDİ] " + updated_article["title"]
        print(update_news(0, updated_article))

    # Haber Silme (Örnek: Son haberi sil)
    if news_db:
        print("\n🗑️ Son haberi siliyoruz...")
        print(delete_news(len(news_db) - 1))

    print("\n📜 Güncellenmiş Haber Listesi:")
    print(json.dumps(read_news(), indent=2, ensure_ascii=False))
