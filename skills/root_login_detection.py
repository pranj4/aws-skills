from utils.aws_client import get_cloudtrail_client
from utils.logger import setup_logger
from datetime import datetime, timedelta

logger = setup_logger('root_login_detection')

def check_root_login_activity():
    cloudtrail = get_cloudtrail_client()
    
    try:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=7)
        
        events = cloudtrail.lookup_events(
            LookupAttributes=[
                {'AttributeKey': 'EventName', 'AttributeValue': 'ConsoleLogin'}
            ],
            StartTime=start_time,
            EndTime=end_time,
            MaxResults=50
        )['Events']
        
        issues = []
        
        for event in events:
            if 'root' in str(event).lower():
                issues.append({
                    'event': 'Root account login detected',
                    'time': str(event['EventTime']),
                    'severity': 'CRITICAL'
                })
        
        return issues
    except Exception as e:
        logger.error(f"CloudTrail check failed: {e}")
        return []


run = check_root_login_activity