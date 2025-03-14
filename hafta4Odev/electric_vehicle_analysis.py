# -------------------- Kütüphaneleri İçe Aktarma --------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# -------------------- Veri Setini Yükleme --------------------
# Electric Vehicle Population veri setini yükle
df = pd.read_csv('ElectricVehiclePopulationData.csv')

# İlk 5 satırı göster
print("İlk 5 satır:")
print(df.head())

# Veri setinin boyutunu göster
print("\nVeri seti boyutu:", df.shape)

# Sütun isimlerini göster
print("\nSütunlar:", df.columns)

# Eksik verileri kontrol et
print("\nEksik veriler:")
print(df.isnull().sum())

# -------------------- Veri Temizleme/Düzenleme --------------------
# Eksik verileri doldurma
df['County'].fillna('Unknown', inplace=True)
df['City'].fillna('Unknown', inplace=True)
df['State'].fillna('Unknown', inplace=True)
df['Postal Code'].fillna('Unknown', inplace=True)
df['Electric Utility'].fillna('Unknown', inplace=True)

# Gereksiz sütunları kaldırma
df.drop(['VIN (1-10)', 'DOL Vehicle ID', 'Vehicle Location', '2020 Census Tract'], axis=1, inplace=True)

# Eksik verileri tekrar kontrol et
print("\nEksik veriler (temizleme sonrası):")
print(df.isnull().sum())

# -------------------- Veri Standardizasyonu ve Normalizasyon --------------------
# Electric Range sütununu standartlaştırma
scaler = StandardScaler()
df['Electric Range_standardized'] = scaler.fit_transform(df[['Electric Range']])

# Electric Range sütununu normalizasyon (0-1 aralığına getirme)
min_max_scaler = MinMaxScaler()
df['Electric Range_normalized'] = min_max_scaler.fit_transform(df[['Electric Range']])

print("\nStandartlaştırılmış ve Normalize Edilmiş Electric Range Sütunu:")
print(df[['Electric Range', 'Electric Range_standardized', 'Electric Range_normalized']].head())

# -------------------- Veri Görselleştirme --------------------
# Markalara göre araç sayısı (Top 10)
plt.figure(figsize=(12, 6))
sns.countplot(y='Make', data=df, order=df['Make'].value_counts().index[:10], palette='viridis')
plt.title('En Çok Elektrikli Araç Üreten Markalar (Top 10)')
plt.xlabel('Araç Sayısı')
plt.ylabel('Marka')
plt.show()

# Electric Range dağılımı
plt.figure(figsize=(10, 6))
sns.histplot(df['Electric Range'], bins=30, kde=True, color='blue')
plt.title('Elektrik Menzili Dağılımı')
plt.xlabel('Electric Range (Mil)')
plt.ylabel('Frekans')
plt.show()

# Araç Türlerine Göre Dağılım (BEV vs PHEV)
plt.figure(figsize=(8, 8))
df['Electric Vehicle Type'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Elektrikli Araç Türlerinin Dağılımı')
plt.ylabel('')
plt.show()

# -------------------- Analiz ve Filtreleme --------------------
# En yüksek menzile sahip araçlar (Top 5)
top_range = df.nlargest(5, 'Electric Range')
print("\nEn Yüksek Elektrik Menzilli Araçlar:")
print(top_range[['Make', 'Model', 'Electric Range']])

# Tesla araçlarını filtrele
tesla_cars = df[df['Make'] == 'TESLA']
print("\nTesla Araçları (İlk 5 Kayıt):")
print(tesla_cars.head())

# 2020 ve sonrası model yılları için filtreleme
recent_models = df[df['Model Year'] >= 2020]
print("\n2020 ve Sonrası Model Yılları (İlk 5 Kayıt):")
print(recent_models.head())

# -------------------- GroupBy ve Özgün Analiz --------------------
# Markalara göre ortalama elektrik menzili
avg_range_by_make = df.groupby('Make')['Electric Range'].mean().sort_values(ascending=False).head(10)
print("\nMarkalara Göre Ortalama Elektrik Menzili (Top 10):")
print(avg_range_by_make)

# -------------------- Sonuçları Kaydetme --------------------
# Temizlenmiş veriyi yeni bir CSV dosyası olarak kaydet
df.to_csv('cleaned_ElectricVehicleData.csv', index=False)
print("\nVeri başarıyla kaydedildi: cleaned_ElectricVehicleData.csv")