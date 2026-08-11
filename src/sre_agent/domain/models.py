from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

class ConnectionMode(str, Enum):
    AGENTLESS = "agentless"
    TUNNEL = "tunnel"
    SHADOW = "shadow"

class UserContext(BaseModel):
    user_id: str = Field(..., description="OIDC Subject / Email")
    groups: List[str] = Field(default_factory=list, description="OIDC Groups")
    jwt_token: str = Field(..., repr=False)
    ticket_id: Optional[str] = Field(None, description="Jira/PagerDuty ID for JIT")

class ClusterConnectionConfig(BaseModel):
    cluster_id: str
    tenant_id: str
    mode: ConnectionMode
    role_arn: Optional[str] = Field(None, description="AWS IAM Role for Agentless")
    mcp_endpoint: Optional[str] = Field(None, description="gRPC/WS endpoint for Tunnel")
    external_id: Optional[str] = Field(None, description="Cross-account trust External ID")

class K8sActionRequest(BaseModel):
    action_type: str = Field(..., description="e.g., apply, delete, restart, scale")
    resource_kind: str
    namespace: str
    resource_name: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None

class DiffResult(BaseModel):
    has_changes: bool
    diff_raw: str = Field(..., description="Raw output from kubectl diff")
    risk_score: int = Field(..., ge=0, le=100)
    risk_factors: List[str] = Field(default_factory=list)
    rollback_manifest: Optional[str] = None

class AuditLogEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    trace_id: str
    user_id: str
    cluster_id: str
    action: K8sActionRequest
    risk_score: int
    approved_by: Optional[str] = None
    execution_result: str
