import logging
import json
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from rag.ocl_retriever import OCLRetrieverEngine
from ai.plantuml_normalizer import normalize_plantuml_text

# Loglama entegrasyonu
logging.basicConfig(filename='agent_workflow.log', level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MultiAgentWorkflow")

# LangGraph state güncellemesi: iteration_count eklendi
class WorkflowState(TypedDict):
    original_text: str
    current_uml: str
    errors: List[str]
    error_categories: List[str]
    is_valid: bool
    iteration_count: int  

class UMLMultiAgentSystem:
    def __init__(self, model_name="gpt-4o-mini", temperature=0, max_iterations: int = 3):
        if max_iterations < 1:
            raise ValueError("max_iterations en az 1 olmalidir.")

        self.max_iterations = max_iterations
        self.last_final_state = None
        self.llm_call_count = 0
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)

        #RAG modülü başlatılıyor
        self.retriever = OCLRetrieverEngine()
        
        # Critic hata tespit promptu
        self.critic_prompt = PromptTemplate(
        input_variables=["original_text", "current_uml", "ocl_rules"],
        template="""
        Sen katı bir UML denetmenisin. Gereksinimi ve UML'i karşılaştır.
        Ayrıca aşağıdaki OCL iş kurallarının UML'de ihlal edilmediğinden kesinlikle emin ol.

        OCL Kuralları:
        {ocl_rules}

        Hata yoksa sadece "GECERLI" yaz. Hata varsa bunları JSON formatında liste olarak dön.
        Örnek JSON: {{"hatalar": ["Eksik sınıf: User", "OCL İhlali: age özelliği yok"], "kategori": ["Eksiklik", "OCL"]}}

        Gereksinim: {original_text}
        PlantUML: {current_uml}
        """
    )
        
        # Onarım promptu
        self.healer_prompt = PromptTemplate(
            input_variables=["current_uml", "errors"],
            template="""
            Sen onarıcı ajansın (Healer). Hataları JSON formatında alıyorsun. 
            Aşağıdaki hatalı UML kodunu düzelt ve sadece yeni PlantUML kodunu dön.
            
            Hatalı UML: {current_uml}
            Hatalar (JSON): {errors}
            """
        )
        
        self.workflow = self._build_graph()

    def critic_node(self, state: WorkflowState) -> WorkflowState:
        logger.info(f"Critic Node çalışıyor. İterasyon: {state['iteration_count']}")
        
        #  RAG modülü ile OCL kurallarını çekiyoruz
        relevant_rules = self.retriever.retrieve_relevant_rules(state["current_uml"])
        logger.info(f"Critic'e sağlanan OCL kuralları: {relevant_rules}")
        
        # LLM'i çağırırken prompta 'ocl_rules' değişkenini de gönderiyoruz
        self.llm_call_count += 1
        response = self.llm.invoke(
            self.critic_prompt.format(
                original_text=state["original_text"], 
                current_uml=state["current_uml"],
                ocl_rules=relevant_rules
            )
        )
        
        # YANITIN İŞLENMESİ 
        feedback = response.content.strip()
        if feedback == "GECERLI":
            state["is_valid"] = True
            state["errors"] = []
        else:
            state["is_valid"] = False
            state["errors"] = [feedback] 
            logger.warning("Critic hata buldu.")
            
        return state

    def healer_node(self, state: WorkflowState) -> WorkflowState:
        logger.info("Healer Node çalışıyor: UML onarılıyor...")
        self.llm_call_count += 1
        response = self.llm.invoke(
            self.healer_prompt.format(current_uml=state["current_uml"], errors=json.dumps(state["errors"]))
        )
        
        state["current_uml"] = normalize_plantuml_text(response.content)
        state["errors"] = [] 
        # State'e deneme sayısı yazma
        state["iteration_count"] += 1 
        logger.info(f"Healer yeni UML üretti. Yeni iterasyon sayacı: {state['iteration_count']}")
        return state

    # Döngü kırma senaryoları ve 3 iterasyon limiti
    def routing_logic(self, state: WorkflowState) -> str:
        if state["is_valid"]:
            logger.info("Sistem başarılı. Süreç sonlandırılıyor.")
            return "end"
            
        if state["iteration_count"] > self.max_iterations:
            logger.warning(f"Maksimum {self.max_iterations} iterasyon limitine ulaşıldı! Döngü kırılıyor.")
            return "end"
            
        return "continue"

    def _build_graph(self):
        workflow = StateGraph(WorkflowState)
        workflow.add_node("Critic", self.critic_node)
        workflow.add_node("Healer", self.healer_node)
        workflow.set_entry_point("Critic")
        
        workflow.add_conditional_edges(
            "Critic",
            self.routing_logic,
            {"continue": "Healer", "end": END}
        )
        workflow.add_edge("Healer", "Critic")
        return workflow.compile()

    def run(self, original_text: str, initial_uml: str, return_state: bool = False):
        logger.info("--- Otonom Döngü Başlatıldı ---")
        initial_state = WorkflowState(
            original_text=original_text,
            current_uml=initial_uml,
            errors=[],
            error_categories=[],
            is_valid=False,
            iteration_count=1  # Sayaç 1'den başlar
        )
        final_state = self.workflow.invoke(initial_state)
        self.last_final_state = final_state
        if return_state:
            return final_state
        return final_state["current_uml"]
