from utils.aws_client import get_s3_client
from utils.logger import setup_logger

logger = setup_logger('s3_detection')

def check_s3_public_buckets():
    s3 = get_s3_client()
    
    try:
        buckets = s3.list_buckets()['Buckets']
        issues = []
        
        for bucket in buckets:
            try:
                acl = s3.get_bucket_acl(Bucket=bucket['Name'])
                for grant in acl['Grants']:
                    if 'AllUsers' in grant['Grantee'].get('URI', ''):
                        issues.append({
                            'bucket': bucket['Name'],
                            'issue': 'Publicly readable',
                            'severity': 'HIGH'
                        })
                        break
            except:
                pass
        
        return issues
    except Exception as e:
        logger.error(f"S3 check failed: {e}")
        return []


run = check_s3_public_buckets