import logging
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# Loglama ayarları
logger = logging.getLogger("SemanticEvaluator")

# Output şeması standardı (Week 4 görevi)[cite: 2]
class SemanticFidelityScore(BaseModel):
    score: int = Field(description="1-5 arası Semantic Fidelity skoru. 1: Çok Kötü, 5: Kusursuz")
    justification: str = Field(description="Verilen skorun kısa akademik gerekçesi")
    critical_errors: str = Field(description="Varsa kritik hata notları, yoksa 'Yok'")

class LLMAsAJudge:
    def __init__(self, model_name="gpt-4o", temperature=0):
        # Skorlama mekanizması için daha güçlü bir model (gpt-4o) kullanmak genellikle daha tutarlı sonuç verir.
        # with_structured_output ile LLM'i zorla belirttiğimiz Pydantic formatında (JSON) yanıt vermeye itiyoruz.
        self.llm = ChatOpenAI(model=model_name, temperature=temperature).with_structured_output(SemanticFidelityScore)
        
        # Skorlama promptu geliştirme (Week 4 görevi)[cite: 2]
        self.eval_prompt = PromptTemplate(
            input_variables=["requirements", "final_uml"],
            template="""
            Sen objektif bir akademik değerlendiricisin (LLM-as-a-Judge). 
            Aşağıdaki sistem gereksinimlerini ve üretilen final PlantUML diyagramını incele.
            
            Değerlendirme Ölçütleri:
            1. Doğruluk (Sınıflar ve nitelikler doğru yansıtılmış mı?)
            2. Tutarlılık (İlişkiler ve yönler mantıklı mı?)
            3. Eksiksizlik (Metindeki tüm isterler diyagramda var mı?)
            
            Sadece JSON formatında (score, justification, critical_errors) yanıt ver. Skor 1 ile 5 arasında tam sayı olmalıdır.
            Kabul edilebilir eşik değer (Threshold) 4'tür. 4'ün altındaki skorlarda kritik hataları mutlaka belirt.
            
            Gereksinimler:
            {requirements}
            
            Final PlantUML:
            {final_uml}
            """
        )

    def evaluate_diagram(self, requirements_text: str, final_uml: str) -> dict:
        """
        Pipeline entegrasyonu için çağrılacak ana fonksiyon (Week 4 görevi)[cite: 2]
        """
        logger.info("Semantic Fidelity skorlaması başlatıldı...")
        try:
            # Yapılandırılmış LLM çağrısı
            result: SemanticFidelityScore = self.llm.invoke(
                self.eval_prompt.format(requirements=requirements_text, final_uml=final_uml)
            )
            
            # Eşik değer (Threshold) kontrolü[cite: 2]
            threshold_passed = result.score >= 4
            
            eval_output = {
                "score": result.score,
                "justification": result.justification,
                "critical_errors": result.critical_errors,
                "is_publishable": threshold_passed
            }
            
            logger.info(f"Skorlama tamamlandı. Skor: {result.score}/5. Yayınlanabilir mi: {threshold_passed}")
            return eval_output
            
        except Exception as e:
            logger.error(f"Skorlama sırasında hata: {str(e)}")
            return {"error": str(e), "is_publishable": False}

# Test bloğu
if __name__ == "__main__":
    evaluator = LLMAsAJudge()
    test_req = "Sistemde Müşteri ve Adres sınıfları olacak. Müşteri birden çok adrese sahip olabilir."
    test_uml = "class Müşteri\nclass Adres\nMüşteri \"1\" -- \"*\" Adres"
    
    print(evaluator.evaluate_diagram(test_req, test_uml))