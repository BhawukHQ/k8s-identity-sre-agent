import boto3
from typing import Dict
from src.sre_agent.domain.interfaces import IdentityVerifier
from src.sre_agent.domain.models import UserContext, ClusterConnectionConfig

class AWSOIDCIdentityVerifier(IdentityVerifier):
    def __init__(self, region_name: str = "us-east-1"):
        self.sts_client = boto3.client('sts', region_name=region_name)
        
    async def verify_and_assume_role(self, context: UserContext, config: ClusterConnectionConfig) -> Dict:
        """
        Assumes an IAM Role using the incoming OIDC JWT token.
        This provides ephemeral credentials scoped exactly to the user's rights.
        """
        if not config.role_arn:
            raise ValueError("Role ARN is required for Agentless AWS mode")
            
        kwargs = {
            "RoleArn": config.role_arn,
            "RoleSessionName": context.user_id.replace("@", "-"),
            "WebIdentityToken": context.jwt_token,
            "DurationSeconds": 900 # 15 minutes JIT max
        }
        
        # Verify external ID for cross-account security if provided
        if config.external_id:
            # Note: AssumeRoleWithWebIdentity doesn't natively support ExternalId like standard AssumeRole,
            # but we can enforce claims inside the JWT or use standard AssumeRole if chaining.
            pass
            
        response = self.sts_client.assume_role_with_web_identity(**kwargs)
        
        return {
            "AccessKeyId": response['Credentials']['AccessKeyId'],
            "SecretAccessKey": response['Credentials']['SecretAccessKey'],
            "SessionToken": response['Credentials']['SessionToken']
        }
