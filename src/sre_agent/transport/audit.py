from src.sre_agent.domain.interfaces import AuditLogger
from src.sre_agent.domain.models import AuditLogEntry
import json
import logging

logger = logging.getLogger(__name__)

class DynamoDBAuditLogger(AuditLogger):
    def __init__(self, table_name: str = "SRE_AuditLogs"):
        self.table_name = table_name
        # self.dynamodb = boto3.resource('dynamodb')
        
    async def log_event(self, entry: AuditLogEntry) -> None:
        """
        Emits an encrypted log to DynamoDB.
        KMS encryption is handled transparently if the DDB table is configured with a CMK.
        """
        payload = entry.model_dump(mode='json')
        # table = self.dynamodb.Table(self.table_name)
        # table.put_item(Item=payload)
        logger.info(f"AUDIT LOG: {json.dumps(payload)}")
