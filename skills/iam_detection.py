from utils.aws_client import get_iam_client
from utils.logger import setup_logger

logger = setup_logger('iam_detection')

def check_privilege_escalation():
    iam = get_iam_client()
    
    try:
        users = iam.list_users()['Users']
        issues = []
        
        for user in users:
            user_name = user['UserName']
            
            # Check 1: Inline policies
            try:
                inline_policies = iam.list_user_policies(UserName=user_name)['PolicyNames']
                
                for policy_name in inline_policies:
                    policy_doc = iam.get_user_policy(
                        UserName=user_name,
                        PolicyName=policy_name
                    )['PolicyDocument']
                    
                    for statement in policy_doc.get('Statement', []):
                        if statement.get('Effect') == 'Allow':
                            actions = statement.get('Action', [])
                            if isinstance(actions, str):
                                actions = [actions]
                            
                            # Check for wildcards
                            if '*' in actions:
                                issues.append({
                                    'user': user_name,
                                    'policy': policy_name,
                                    'issue': 'Has wildcard permissions (inline)',
                                    'severity': 'CRITICAL'
                                })
                                break
            except Exception as inline_error:
                logger.debug(f"Could not check inline policies for {user_name}: {inline_error}")
            
            # Check 2: Attached managed policies
            try:
                attached_policies = iam.list_attached_user_policies(UserName=user_name)['AttachedPolicies']
                
                for policy in attached_policies:
                    policy_arn = policy['PolicyArn']
                    policy_name = policy['PolicyName']
                    
                    # Dangerous managed policies
                    risky_policies = [
                        'AdministratorAccess',
                        'PowerUserAccess',
                        'IAMFullAccess',
                        'SecurityAudit'  # Can be abused
                    ]
                    
                    if policy_name in risky_policies:
                        issues.append({
                            'user': user_name,
                            'policy': policy_name,
                            'issue': f'Attached managed policy: {policy_name}',
                            'severity': 'HIGH'
                        })
                    
                    # Also check the policy document for wildcards
                    try:
                        policy_version = iam.get_policy(PolicyArn=policy_arn)['Policy']
                        default_version_id = policy_version['DefaultVersionId']
                        
                        policy_doc = iam.get_policy_version(
                            PolicyArn=policy_arn,
                            VersionId=default_version_id
                        )['PolicyVersion']['Document']
                        
                        for statement in policy_doc.get('Statement', []):
                            if statement.get('Effect') == 'Allow':
                                actions = statement.get('Action', [])
                                if isinstance(actions, str):
                                    actions = [actions]
                                
                                if '*' in actions:
                                    issues.append({
                                        'user': user_name,
                                        'policy': policy_name,
                                        'issue': 'Attached policy has wildcard permissions',
                                        'severity': 'CRITICAL'
                                    })
                                    break
                    except Exception as version_error:
                        logger.debug(f"Could not check policy document for {policy_name}: {version_error}")
            
            except Exception as attached_error:
                logger.debug(f"Could not check attached policies for {user_name}: {attached_error}")
        
        if issues:
            logger.info(f"Found {len(issues)} IAM privilege escalation risk(s)")
        else:
            logger.info("No IAM privilege escalation risks found")
        
        return issues
    
    except Exception as e:
        logger.error(f"IAM check failed: {e}")
        return []


run = check_privilege_escalation