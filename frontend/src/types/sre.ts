export interface UserContext {
  userId: string;
  groups: string[];
  jwtToken: string;
}

export interface K8sActionRequest {
  actionType: 'apply' | 'delete' | 'restart' | 'scale';
  resourceKind: string;
  namespace: string;
  resourceName?: string;
  payload?: any;
}

export interface DiffResult {
  hasChanges: boolean;
  diffRaw: string;
  riskScore: number;
  riskFactors: string[];
  rollbackManifest?: string;
}

export interface ApprovalRequest {
  actionId: string;
  ticketId?: string;
  diff: DiffResult;
  status: 'pending' | 'approved' | 'rejected';
}
