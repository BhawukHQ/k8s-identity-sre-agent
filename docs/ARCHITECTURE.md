# Architecture & Security Flow

## 1. ASCII Architecture Diagram

```text
+-----------------------------------------------------------------------------------+
|                            ENTERPRISE K8s SRE AI AGENT                            |
+-----------------------------------------------------------------------------------+
|  [Google Stitch UI]                                                               |
|  - Auth/OIDC Login                                                                |
|  - ClusterSelector, DiffViewer, ApprovalModal                                     |
+------------------------------------+----------------------------------------------+
                                     | (JWT / OIDC Token)
                                     v
+------------------------------------+----------------------------------------------+
|                          API & PRESENTATION LAYER                                 |
|  [FastAPI / WebSockets]                                                           |
|  - Route HTTP/WS requests                                                         |
|  - Validate OIDC JWT Signature                                                    |
+------------------------------------+----------------------------------------------+
                                     |
+------------------------------------+----------------------------------------------+
|                          ORCHESTRATION LAYER (LangGraph)                          |
|  [State: {tenant_id}:{cluster_id}:{session_id}]                                   |
|   1. Intent Parsing -> 2. Plan -> 3. Dry-Run -> 4. Risk Eval -> 5. HITL Interrupt |
+------------------------------------+----------------------------------------------+
                                     |
+------------------------------------+----------------------------------------------+
|                           TRANSPORT & TOOL LAYER                                  |
|  [AWS STS Handler]        [MCP Client Connector]         [Audit/KMS Logger]       |
|  - AssumeRoleWithWebId    - Dynamic Tool Binder          - DynamoDB + CloudWatch  |
|  - JIT Ticket Validator   - Rate Limiter & Breakers      - Tamper-proof logs      |
+------------------------------------+----------------------------------------------+
                                     |
           +-------------------------+-------------------------+
           |                         |                         |
(Option 1: Agentless/OOB)  (Option 2: Tunnel/Sidecar) (Option 3: Shadow Mode)
           |                         |                         |
           v                         v                         v
+--------------------+   +-----------------------+   +--------------------+
|   AWS EKS Cluster  |   | Private/On-Prem K8s   |   | Any K8s Cluster    |
| (IAM OIDC Trust)   |   | (MCP gRPC Sidecar)    |   | (Read-Only RBAC)   |
| Impersonate-User   |   | Impersonate-User      |   | Audit Logging Only |
+--------------------+   +-----------------------+   +--------------------+
```

## 2. Sequence Diagram (Mermaid)

```mermaid
sequenceDiagram
    participant U as End User (UI)
    participant API as FastAPI (API Layer)
    participant LG as LangGraph (Orchestrator)
    participant IAM as AWS STS / IAM
    participant MCP as MCP Tool Layer
    participant K8S as K8s API Server
    participant AUD as DynamoDB/CloudWatch

    U->>API: 1. Submit Request + OIDC JWT
    API->>IAM: 2. AssumeRoleWithWebIdentity (JWT)
    IAM-->>API: 3. Return Temp AWS Credentials
    API->>LG: 4. Invoke SRE Graph (State Init)
    LG->>MCP: 5. Execute Dry-Run (kubectl diff)
    MCP->>K8S: 6. API Call (Impersonate-User, Dry-Run)
    K8S-->>MCP: 7. Diff Output
    MCP-->>LG: 8. Return Diff Result
    LG->>LG: 9. Calculate Blast Radius Score (0-100)
    
    alt Risk Score > 30 or Mutating
        LG->>U: 10. interrupt() -> Request HITL Approval
        U->>LG: 11. Approve + JIT Ticket ID
        LG->>AUD: 12. Log Approval & Signatures (KMS Encrypted)
    end

    LG->>MCP: 13. Execute Mutation
    MCP->>K8S: 14. API Call (Impersonate-User, Apply)
    K8S-->>MCP: 15. Success/Failure
    MCP->>AUD: 16. Log Final Execution State
    LG-->>API: 17. Update Graph State
    API-->>U: 18. Return Success & Audit ID
```
