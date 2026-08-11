from typing import TypedDict, Annotated, Optional
from langgraph.graph.message import add_messages
from src.sre_agent.domain.models import UserContext, ClusterConnectionConfig, K8sActionRequest, DiffResult

class AgentState(TypedDict):
    """LangGraph State for SRE Execution"""
    user_context: UserContext
    cluster_config: ClusterConnectionConfig
    request: K8sActionRequest
    
    # State accumulated during execution
    credentials: Optional[dict]
    diff_result: Optional[DiffResult]
    approval_granted: Optional[bool]
    execution_result: Optional[str]
    audit_trace_id: Optional[str]
    
    # Messages list for conversation/logs
    messages: Annotated[list, add_messages]
