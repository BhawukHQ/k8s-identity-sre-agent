import uuid
from langgraph.graph import StateGraph, END
from src.sre_agent.orchestration.state import AgentState
from src.sre_agent.orchestration.safety import BlastRadiusEvaluator
from src.sre_agent.domain.models import DiffResult
# In a real setup, these would be injected dependencies
# from src.sre_agent.transport.mcp_connector import DefaultMCPConnector

# Node functions
def authenticate_and_assume_role(state: AgentState):
    # Call AWS STS handler
    # For now, mock the credentials
    return {"credentials": {"AccessKeyId": "MOCK", "SecretAccessKey": "MOCK"}}

def execute_dry_run(state: AgentState):
    # Mock executing dry run via MCP
    mock_diff = "--- old\n+++ new\n+ replicas: 3\n- replicas: 1"
    return {"diff_result": DiffResult(
        has_changes=True,
        diff_raw=mock_diff,
        risk_score=0,
        risk_factors=[]
    )}

def evaluate_blast_radius(state: AgentState):
    evaluator = BlastRadiusEvaluator()
    diff_res = evaluator.calculate_risk(state["request"], state["diff_result"].diff_raw)
    return {"diff_result": diff_res}

def check_human_approval(state: AgentState):
    # In LangGraph, we can use an interrupt for HITL
    risk_score = state["diff_result"].risk_score
    if risk_score > 30 or state["request"].action_type in ["delete", "apply"]:
        # We simulate this via state for now. In a real server, this node would interrupt
        if state.get("approval_granted") is None:
            # Here we would raise an exception or use LangGraph's interrupt()
            # For demonstration, we just return
            pass
    return {}

def execute_mutation(state: AgentState):
    # Mock mutation execution
    return {"execution_result": "Success"}

def log_audit(state: AgentState):
    trace_id = str(uuid.uuid4())
    return {"audit_trace_id": trace_id}

# Build the Graph
def build_sre_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("auth", authenticate_and_assume_role)
    workflow.add_node("dry_run", execute_dry_run)
    workflow.add_node("risk_eval", evaluate_blast_radius)
    workflow.add_node("hitl_check", check_human_approval)
    workflow.add_node("mutate", execute_mutation)
    workflow.add_node("audit", log_audit)
    
    workflow.set_entry_point("auth")
    workflow.add_edge("auth", "dry_run")
    workflow.add_edge("dry_run", "risk_eval")
    workflow.add_edge("risk_eval", "hitl_check")
    
    # Conditional edge after HITL
    def hitl_router(state: AgentState):
        risk_score = state["diff_result"].risk_score
        if risk_score <= 30 and state["request"].action_type not in ["delete", "apply"]:
            return "mutate"
        if state.get("approval_granted"):
            return "mutate"
        return "audit" # if rejected or not approved
    
    workflow.add_conditional_edges("hitl_check", hitl_router, {
        "mutate": "mutate",
        "audit": "audit"
    })
    
    workflow.add_edge("mutate", "audit")
    workflow.add_edge("audit", END)
    
    return workflow.compile()
