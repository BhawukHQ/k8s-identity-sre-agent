# Enterprise Identity-Aware K8s SRE Agent

A modular, production-grade Identity-Aware Kubernetes SRE AI Platform featuring Connect Your Own Cluster (CYOC) functionality.

## Core Features
1. **Zero Trust, Identity Propagation:** Uses AWS STS and K8s Impersonation. No shared `cluster-admin` tokens.
2. **CYOC Engine:** Connect agentless via AWS IAM OIDC or via Tunnel (MCP gRPC Sidecar) for private clusters.
3. **Safety & Blast Radius:** Mandatory dry-runs, blast radius assessment, and Human-In-The-Loop (HITL) approval flows.
4. **Agent Architecture:** Powered by LangGraph for deterministic state, checkpointing, and execution.

## Documentation
Please refer to [ARCHITECTURE.md](./docs/ARCHITECTURE.md) for detailed sequence flows and component diagrams.

## Quick Start
*TBD*
