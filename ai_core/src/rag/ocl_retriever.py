"""Modern retrieval is local; exact historical OpenAI retrieval is opt-in."""
from .local_rules import LocalRuleRetriever


class OCLRetrieverEngine(LocalRuleRetriever):
    def __new__(cls, legacy=False):
        if legacy:
            from .legacy_ocl_retriever import OCLRetrieverEngine as OriginalRetriever
            return OriginalRetriever()
        return super().__new__(cls)

    def retrieve_relevant_rules(self,current_uml,top_k=2,srs=""):
        return "\n".join(r["text"] for r in self.retrieve(srs,current_uml,top_k=top_k))
