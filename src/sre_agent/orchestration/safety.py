from typing import Dict, Any
from src.sre_agent.domain.models import K8sActionRequest, DiffResult
from src.sre_agent.domain.interfaces import RiskEvaluator

class BlastRadiusEvaluator(RiskEvaluator):
    
    def __init__(self):
        # Higher score means higher risk
        self.risk_weights = {
            "namespaces": {"kube-system": 50, "default": 20, "prod": 40},
            "kinds": {"Deployment": 10, "StatefulSet": 30, "PersistentVolumeClaim": 50, "Secret": 40, "Pod": 5},
            "actions": {"apply": 10, "delete": 40, "restart": 20}
        }
        
    def calculate_risk(self, request: K8sActionRequest, diff: str) -> DiffResult:
        score = 0
        factors = []
        
        # Action risk
        action_risk = self.risk_weights["actions"].get(request.action_type.lower(), 10)
        score += action_risk
        factors.append(f"Action '{request.action_type}' adds {action_risk} risk")
        
        # Namespace risk
        ns_risk = self.risk_weights["namespaces"].get(request.namespace.lower(), 10)
        score += ns_risk
        factors.append(f"Namespace '{request.namespace}' adds {ns_risk} risk")
        
        # Resource Kind risk
        kind_risk = self.risk_weights["kinds"].get(request.resource_kind, 10)
        score += kind_risk
        factors.append(f"Resource Kind '{request.resource_kind}' adds {kind_risk} risk")
        
        has_changes = bool(diff.strip())
        if not has_changes:
            score = 0
            factors = ["No changes detected in dry-run"]
            
        return DiffResult(
            has_changes=has_changes,
            diff_raw=diff,
            risk_score=min(score, 100),
            risk_factors=factors,
            rollback_manifest=None
        )
