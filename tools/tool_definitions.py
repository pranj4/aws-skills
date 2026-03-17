TOOLS = [
    {
        "name": "check_s3_public_buckets",
        "description": "Check for publicly accessible S3 buckets in AWS account",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "check_privilege_escalation",
        "description": "Check for IAM users with overly permissive policies",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "check_root_login_activity",
        "description": "Check for root account login activity in CloudTrail logs",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]