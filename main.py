from dotenv import load_dotenv
load_dotenv()  # Load FIRST

import os
from tools.anthropic_integration import run_security_analysis
from utils.logger import setup_logger

logger = setup_logger('main')

def main():
    logger.info("Starting AWS Security Detection Agent")
    
    queries = [
        "Check my AWS account for S3 security issues",
        "Scan for IAM privilege escalation risks",
        "Check if root account has been used recently"
    ]
    
    for query in queries:
        logger.info(f"Query: {query}")
        result = run_security_analysis(query)
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        print(result)
        print()

if __name__ == "__main__":
    main()