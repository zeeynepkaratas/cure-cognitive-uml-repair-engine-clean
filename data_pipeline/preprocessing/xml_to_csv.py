import os
import re
import pandas as pd
from pathlib import Path

PIPELINE_ROOT = Path(__file__).resolve().parents[1]
XML_DIR = PIPELINE_ROOT / "datasets" / "xml_verileri"
OUTPUT_PATH = PIPELINE_ROOT / "datasets" / "pure_dataset.csv"

print("1. İnatçı XML dosyaları 'Buldozer' yöntemiyle parçalanıyor...")
klasor_yolu = str(XML_DIR)
tum_gereksinimler = []

for kok_dizin, alt_dizinler, dosyalar in os.walk(klasor_yolu):
    if '__MACOSX' in kok_dizin:
        continue
        
    for dosya_adi in dosyalar:
        if dosya_adi.endswith('.xml') and not dosya_adi.startswith('._'):
            tam_yol = os.path.join(kok_dizin, dosya_adi)
            try:
                # Dosyayı XML olarak değil, dümdüz metin olarak okuyoruz
                with open(tam_yol, 'r', encoding='utf-8', errors='ignore') as f:
                    icerik = f.read()
                    
                # İçindeki tüm XML etiketlerini (<tag> vb.) acımasızca silip atıyoruz
                metin = re.sub(r'<[^>]+>', ' ', icerik)
                
                # Kalan fazla boşlukları temizliyoruz
                metin = re.sub(r'\s+', ' ', metin)
                
                # Metni noktalardan (.) bölerek cümlelere ayırıyoruz
                cumleler = metin.split('. ')
                
                for cumle in cumleler:
                    cumle = cumle.strip()
                    # Sadece 20 karakterden uzun, anlamlı cümleleri alıyoruz (saçma sapan harfleri eliyoruz)
                    if len(cumle) > 20:
                        tum_gereksinimler.append(cumle + '.')
                        
            except Exception as e:
                print(f"Hata atlandı: {dosya_adi} - {e}")

print("2. Saf metinler elde edildi! Kopya cümleler temizleniyor...")

# Listeyi tabloya (DataFrame) çeviriyoruz
df = pd.DataFrame(tum_gereksinimler, columns=['Requirement'])

# Birbirinin kopyası olan satırları atıyoruz ki veritabanımız gereksiz şişmesin
df = df.drop_duplicates()

# Final dosyasına kaydediyoruz
df.to_csv(OUTPUT_PATH, index=False)

print(f"BİNGÖ! Bütün çöpler ayıklandı. Toplam {len(df)} adet saf gereksinim cümlesi 'pure_dataset.csv' dosyasına kaydedildi.")
