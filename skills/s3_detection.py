from utils.aws_client import get_s3_client
from utils.logger import setup_logger
import json

logger = setup_logger('s3_detection')

def check_s3_public_buckets():
    s3 = get_s3_client()
    
    try:
        buckets = s3.list_buckets()['Buckets']
        issues = []
        
        for bucket in buckets:
            bucket_name = bucket['Name']
            
            # Check 1: ACL for public access
            try:
                acl = s3.get_bucket_acl(Bucket=bucket_name)
                for grant in acl['Grants']:
                    grantee_uri = grant['Grantee'].get('URI', '')
                    
                    # Check for AllUsers or AuthenticatedUsers
                    if 'AllUsers' in grantee_uri or 'AuthenticatedUsers' in grantee_uri:
                        issues.append({
                            'bucket': bucket_name,
                            'issue': f'Publicly readable via ACL ({grantee_uri})',
                            'severity': 'HIGH'
                        })
                        break
            except Exception as acl_error:
                logger.debug(f"Could not check ACL for {bucket_name}: {acl_error}")
            
            # Check 2: Bucket Policy for public access
            try:
                policy_response = s3.get_bucket_policy(Bucket=bucket_name)
                policy = json.loads(policy_response['Policy'])
                
                for statement in policy.get('Statement', []):
                    principal = statement.get('Principal', {})
                    
                    # Check if principal is "*" (everyone)
                    if principal == '*' or principal.get('AWS') == '*':
                        effect = statement.get('Effect', '')
                        actions = statement.get('Action', [])
                        
                        # Check if it allows read/get actions
                        if effect == 'Allow':
                            if isinstance(actions, str):
                                actions = [actions]
                            
                            for action in actions:
                                if 's3:GetObject' in action or 's3:Get*' in action or action == '*':
                                    issues.append({
                                        'bucket': bucket_name,
                                        'issue': 'Publicly readable via bucket policy',
                                        'severity': 'HIGH'
                                    })
                                    break
            except s3.exceptions.NoSuchBucketPolicy:
                pass  # No policy = not public via policy
            except Exception as policy_error:
                logger.debug(f"Could not check policy for {bucket_name}: {policy_error}")
        
        if issues:
            logger.info(f"Found {len(issues)} public S3 bucket(s)")
        
        return issues
    
    except Exception as e:
        logger.error(f"S3 check failed: {e}")
        return []


run = check_s3_public_buckets