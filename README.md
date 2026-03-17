### Prerequisites
- Python 3.8+
- AWS Account with appropriate credentials
- Anthropic API Key

## How It Works

1. You ask a security question
2. Claude AI decides which AWS checks to run
3. The agent scans your account
4. Results are analyzed and formatted
5. You get a readable security report



## Project Structure

```
aws-security-agent-skills/
├── skills/                 # Detection logic
│   ├── s3_detection.py
│   ├── iam_detection.py
│   └── root_login_detection.py
├── tools/                  # Claude integration
│   ├── tool_definitions.py
│   └── anthropic_integration.py
├── utils/                  # Helpers
│   ├── aws_client.py
│   └── logger.py
├── main.py                 # Entry point
├── requirements.txt
├── .env.example
└── README.md
```
