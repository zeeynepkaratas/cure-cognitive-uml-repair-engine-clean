"""Public repair workflow API; original implementation is explicitly opt-in."""
from .repair_agent import RepairConfig, UMLRepairAgent


class UMLMultiAgentSystem:
    def __new__(cls, model_name="gpt-4o-mini", temperature=0, max_iterations=3, legacy=True):
        if legacy:
            from .legacy_workflow import UMLMultiAgentSystem as OriginalWorkflow
            return OriginalWorkflow(model_name=model_name,temperature=temperature,max_iterations=max_iterations)
        return UMLRepairAgent(RepairConfig(model_critic=model_name,model_healer=model_name,
                                          temperature=temperature,max_iterations=max_iterations))
