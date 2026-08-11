from kubernetes_asyncio import client, config
from src.sre_agent.domain.models import UserContext, K8sActionRequest
import json

class K8sClientWrapper:
    def __init__(self, kubeconfig_path: str = None):
        self.kubeconfig_path = kubeconfig_path
        
    async def get_impersonated_api_client(self, user_context: UserContext, credentials: dict):
        """
        Initializes an async K8s API client applying Impersonate-User headers.
        """
        # In a real scenario, we'd use the AWS credentials to get a token via aws-iam-authenticator
        # For now, we set up the headers.
        configuration = client.Configuration()
        # Add impersonation headers
        configuration.api_key['authorization'] = "Bearer MOCK_TOKEN" 
        
        api_client = client.ApiClient(configuration)
        api_client.default_headers['Impersonate-User'] = user_context.user_id
        
        if user_context.groups:
            # Provide groups as comma-separated or multiple headers based on client support
            api_client.default_headers['Impersonate-Group'] = ",".join(user_context.groups)
            
        return api_client

    async def apply_resource(self, api_client: client.ApiClient, request: K8sActionRequest, dry_run: bool = False):
        """
        Executes a dynamic apply using the impersonated client.
        """
        # Using dynamic client or raw API call
        path = f"/api/v1/namespaces/{request.namespace}/{request.resource_kind.lower()}s"
        if request.resource_name:
            path += f"/{request.resource_name}"
            
        query_params = []
        if dry_run:
            query_params.append(("dryRun", "All"))
            
        response = await api_client.call_api(
            path, 
            'PATCH' if request.action_type == 'apply' else 'DELETE',
            query_params=query_params,
            body=request.payload
        )
        return response
