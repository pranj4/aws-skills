from dotenv import load_dotenv
load_dotenv()

from skills.s3_detection import check_s3_public_buckets
from skills.iam_detection import check_privilege_escalation
from skills.root_login_detection import check_root_login_activity

print("="*60)
print("Testing S3 Detection...")
print("="*60)
s3_results = check_s3_public_buckets()
print(f'Results: {s3_results}\n')

print("="*60)
print("Testing IAM Detection...")
print("="*60)
iam_results = check_privilege_escalation()
print(f'Results: {iam_results}\n')

print("="*60)
print("Testing Root Login Detection...")
print("="*60)
root_results = check_root_login_activity()
print(f'Results: {root_results}\n')

print("="*60)
print("All tests completed!")
print("="*60)