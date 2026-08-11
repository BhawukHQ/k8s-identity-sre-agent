from fastapi import FastAPI, Depends, HTTPException
from src.sre_agent.domain.models import K8sActionRequest, UserContext
# from src.sre_agent.presentation.auth import verify_jwt
# from src.sre_agent.orchestration.graph import build_sre_graph

app = FastAPI(title="Identity-Aware SRE Agent")

@app.post("/api/v1/cluster/{cluster_id}/action")
async def request_action(cluster_id: str, request: K8sActionRequest):
    # This endpoint receives the OIDC JWT (via middleware)
    # user_context = verify_jwt(token)
    
    # graph = build_sre_graph()
    # state = {"user_context": user_context, "request": request, "cluster_config": ...}
    # result = graph.invoke(state)
    
    return {"status": "pending_approval", "diff_url": f"/api/v1/action/123/diff"}

@app.post("/api/v1/action/{action_id}/approve")
async def approve_action(action_id: str, ticket_id: str):
    # Resumes LangGraph execution
    return {"status": "executed"}
