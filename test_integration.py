from dotenv import load_dotenv
load_dotenv()

from tools.anthropic_integration import run_security_analysis

print("="*60)
print("Testing Full Security Analysis with Claude")
print("="*60)

queries = [
    "Check my AWS account for S3 security issues",
    "Scan for IAM privilege escalation risks",
    "Check if root account has been used recently"
]

for query in queries:
    print(f"\n🔍 Query: {query}")
    print("-"*60)
    result = run_security_analysis(query)
    print(f"📊 Analysis:\n{result}")
    print()