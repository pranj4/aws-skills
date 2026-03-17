from utils.aws_client import get_iam_client
from utils.logger import setup_logger

logger = setup_logger('iam_detection')

def check_privilege_escalation():
    iam = get_iam_client()
    
    try:
        users = iam.list_users()['Users']
        issues = []
        
        for user in users:
            policies = iam.list_user_policies(UserName=user['UserName'])['PolicyNames']
            
            for policy_name in policies:
                policy_doc = iam.get_user_policy(
                    UserName=user['UserName'],
                    PolicyName=policy_name
                )['PolicyDocument']
                
                for statement in policy_doc.get('Statement', []):
                    actions = statement.get('Action', [])
                    if isinstance(actions, str):
                        actions = [actions]
                    
                    if '*' in actions:
                        issues.append({
                            'user': user['UserName'],
                            'issue': 'Has wildcard permissions',
                            'severity': 'HIGH'
                        })
                        break
        
        return issues
    except Exception as e:
        logger.error(f"IAM check failed: {e}")
        return []


run = check_privilege_escalation