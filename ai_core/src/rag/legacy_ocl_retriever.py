import logging
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

# Loglama ayarları
logger = logging.getLogger("OCLRetriever")


class OCLRetrieverEngine:
    def __init__(self):
        """
        Critic ajanı için OCL kural setini vektör arama ile bağlama (Week 3 görevi)
        """
        self.embeddings = OpenAIEmbeddings()
        # Reported experiments use a small curated in-memory OCL rule index.
        # The requirement-level persisted vector repository is future work.
        self.vector_store = None
        self._initialize_curated_rule_index()

    def _initialize_curated_rule_index(self):
        """
        Critic agent için kullanılan küçük, elle seçilmiş OCL-inspired kural dizini.
        Bu dizin PURE gereksinimlerinden türetilmiş bağımsız bir bilgi tabanı değildir.
        """
        sample_ocl_rules = [
            Document(
                page_content="OCL Kuralı 1: Bir User nesnesinin age özelliği mutlaka 18'den büyük veya eşit olmalıdır. (context: age >= 18)"
            ),
            Document(
                page_content="OCL Kuralı 2: Bir Order nesnesinin en az bir OrderItem nesnesine bağıntısı olmalıdır. (context: OrderItem.size() > 0)"
            ),
            Document(
                page_content="OCL Kuralı 3: Eğer bir Product'ın is_digital flag'i true ise, weight özelliği null olmalıdır. (context: is_digital = true implies weight = null)"
            ),
            Document(
                page_content="OCL Kuralı 4: Bir hesaba ait bakiyenin (balance) sıfırın altına düşmesine izin verilmez. (context: balance >= 0.0)"
            ),
        ]

        logger.info("Örnek OCL kural seti vektör veritabanına yükleniyor...")
        self.vector_store = FAISS.from_documents(sample_ocl_rules, self.embeddings)

    def retrieve_relevant_rules(self, current_uml: str, top_k: int = 2) -> str:
        """
        OCL retrieval doğrulama (Week 3 görevi)
        Gelen kural parçalarının bağlama uygunluğunu kontrol etmek için UML içeriğini baz alarak
        en alakalı OCL kural parçalarını getirir.
        """
        if not self.vector_store:
            logger.error("Vektör veritabanı başlatılmamış.")
            return "Kurallar bulunamadı."

        logger.info("UML içeriği için en uygun OCL kuralları aranıyor...")

        # Gelen PlantUML metnine en benzer kısıtları (kuralları) vektör uzayında arıyoruz
        results = self.vector_store.similarity_search(query=current_uml, k=top_k)

        if not results:
            return "İlgili özel bir OCL kuralı bulunamadı."

        # Bulunan kuralları formatlayıp Critic'e verilmek üzere tek bir metin haline getiriyoruz
        formatted_rules = "\n".join([f"- {doc.page_content}" for doc in results])
        logger.info(f"{len(results)} adet ilgili kural bulundu.")

        return formatted_rules


# Basit bir lokal test
if __name__ == "__main__":
    retriever = OCLRetrieverEngine()
    test_uml = """
    class Order {
      +id: String
      +totalAmount: Double
    }
    """
    print("Sorgulanan UML için bulunan kurallar:\n", retriever.retrieve_relevant_rules(test_uml))
