from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import logging

# Loglama sisteminin kurulumu

# .env dosyasından API anahtarlarını yükle
load_dotenv()


class UMLGenerator:
    def __init__(self, model_name="gpt-4o-mini", temperature=0):
        # LLM API Bağlantısı
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)

        # Ham metinden UML üretimi için prompt tasarımı
        self.prompt = PromptTemplate(
            input_variables=["requirements"],
            template="""
            Sen uzman bir yazılım mimarısın. Aşağıdaki gereksinim metnini analiz et ve geçerli bir PlantUML sınıf diyagramı (Class Diagram) kodu üret.
            Sadece PlantUML kodunu döndür, ekstra açıklama yapma.
            
            Gereksinimler:
            {requirements}
            
            PlantUML Kodu:
            """,
        )
        self.chain = self.prompt | self.llm

    def generate_uml(self, requirements_text: str) -> str:
        logging.info(f"UML üretimi başlatıldı. Girdi: {requirements_text[:50]}...")
        try:
            # İlk PlantUML üretimi
            response = self.chain.invoke({"requirements": requirements_text})
            uml_content = response.content
            logging.info("UML başarıyla üretildi.")
            return uml_content
        except Exception as e:
            logging.error(f"UML üretimi sırasında hata oluştu: {str(e)}")
            return f"Hata: {str(e)}"


# Prompt testleri için basit bir kullanım örneği
if __name__ == "__main__":
    generator = UMLGenerator()
    test_text = "Sistemde User ve Order sınıfları olmalıdır. User birden fazla Order verebilir. Order sınıfında total_amount özelliği bulunmalıdır."

    result = generator.generate_uml(test_text)
    print("Üretilen PlantUML:\n", result)
