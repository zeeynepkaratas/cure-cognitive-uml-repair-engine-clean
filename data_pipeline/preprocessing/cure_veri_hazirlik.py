import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
import torch
from pathlib import Path

PIPELINE_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PIPELINE_ROOT / "datasets" / "pure_dataset.csv"
VECTOR_DB_PATH = PIPELINE_ROOT / "vector_db" / "cure_vector_db"

print(f"1. PURE Veri Seti ({DATASET_PATH}) okunuyor...")
try:
    df = pd.read_csv(DATASET_PATH)
    temiz_veriler = df['Requirement'].dropna().tolist()
    print(f"BAŞARILI: {len(temiz_veriler)} adet gerçek gereksinim cümlesi yüklendi!")
except Exception as e:
    print(f"HATA: Veri seti okunamadı! Lütfen pure_dataset.csv dosyasının var olduğundan emin ol. Hata: {e}")
    exit()

print("2. Metinler vektörleştirme için parçalanıyor (Chunking)...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  
    chunk_overlap=50 
)
chunks = text_splitter.create_documents(temiz_veriler)

print("3. Embedding Modeli yükleniyor...")
print("DİKKAT: 7219 satırın matematiksel vektörlere çevrilmesi bilgisayarının hızına göre 5-15 dakika sürebilir. LÜTFEN BEKLE, program donmadı arka planda çalışıyor!")

device = "cuda" if torch.cuda.is_available() else "cpu"

embeddings = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={'device': device},
    encode_kwargs={'normalize_embeddings': True}
)

print("4. Vektör Veritabanı (ChromaDB) oluşturuluyor ve diske yazılıyor...")
persist_directory = str(VECTOR_DB_PATH)

vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=persist_directory
)

print(f"\nŞOV TAMAMLANDI! {len(temiz_veriler)} gerçek gereksinim cümlesi vektörleştirildi ve '{persist_directory}' klasörüne kalıcı olarak kaydedildi.")

# ==========================================
# TEST: GERÇEK VERİTABANINDA ARAMA
# ==========================================
print("\n--- GERÇEK VERİ İLE TEST: RAG Araması Simülasyonu ---")
query = "The system shall provide a user interface"
print(f"Metin'in Ajanının Sorusu: '{query}'")

sonuclar = vector_db.similarity_search(query, k=1) 
if sonuclar:
    print(f"Veritabanından Gelen Gerçek Sonuç: {sonuclar[0].page_content}")
