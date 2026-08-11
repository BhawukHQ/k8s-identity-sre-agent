from abc import ABC, abstractmethod
from typing import Optional
from src.sre_agent.domain.models import (
    UserContext, 
    ClusterConnectionConfig, 
    K8sActionRequest, 
    DiffResult, 
    AuditLogEntry
)

class IdentityVerifier(ABC):
    """Handles Identity Propagation & JIT Elevation."""
    
    @abstractmethod
    async def verify_and_assume_role(
        self, context: UserContext, config: ClusterConnectionConfig
    ) -> dict:
        """Exchanges JWT for short-lived credentials or impersonation headers."""
        pass

class MCPClusterConnector(ABC):
    """Abstracts execution to K8s via Agentless AWS or MCP Tunnel."""
    
    @abstractmethod
    async def execute_dry_run(
        self, request: K8sActionRequest, credentials: dict
    ) -> DiffResult:
        """Executes a non-mutating dry-run and generates a rollback snapshot."""
        pass
        
    @abstractmethod
    async def execute_mutation(
        self, request: K8sActionRequest, credentials: dict
    ) -> str:
        """Executes the actual mutation with impersonation."""
        pass

class RiskEvaluator(ABC):
    """Safety & Blast Radius Engine."""
    
    @abstractmethod
    def calculate_risk(self, request: K8sActionRequest, diff: str) -> DiffResult:
        """Calculates 0-100 score based on namespace, kind, and diff magnitude."""
        pass

class ApprovalEngine(ABC):
    """Manages Human-in-the-Loop Interrupts and Validations."""
    
    @abstractmethod
    async def request_approval(
        self, context: UserContext, diff: DiffResult
    ) -> bool:
        """Interrupts execution and waits for user/SRE approval."""
        pass

class AuditLogger(ABC):
    """Immutable Tamper-Proof Logging."""
    
    @abstractmethod
    async def log_event(self, entry: AuditLogEntry) -> None:
        """Emits encrypted log to backend (DynamoDB/CloudWatch)."""
        pass
