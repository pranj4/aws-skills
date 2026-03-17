# AWS Security Detection Agent - Architecture

## System Overview

```mermaid
graph TB
    User["User"] -->|Query| Main["main.py"]
    Main -->|Query + Tools| Claude["Claude API"]
    Claude -->|Tool Decision| Integration["anthropic_integration.py"]
    
    Integration -->|Execute| S3["s3_detection.py"]
    Integration -->|Execute| IAM["iam_detection.py"]
    Integration -->|Execute| Root["root_login_detection.py"]
    
    S3 -->|AWS API| AWS1["S3"]
    IAM -->|AWS API| AWS2["IAM"]
    Root -->|AWS API| AWS3["CloudTrail"]
    
    AWS1 -->|Data| S3
    AWS2 -->|Data| IAM
    AWS3 -->|Data| Root
    
    S3 -->|Results| Claude
    IAM -->|Results| Claude
    Root -->|Results| Claude
    
    Claude -->|Report| Main
    Main -->|Display| User
    
    style User fill:#e1f5ff
    style Claude fill:#fff3e0
    style Main fill:#f3e5f5
```

## Data Flow

```mermaid
sequenceDiagram
    User->>Main: Security Query
    Main->>Claude: Send Query + Tools
    Claude->>Integration: Which tool to use?
    Integration->>Skills: Run Detection
    Skills->>AWS: Check AWS Account
    AWS-->>Skills: Return Data
    Skills->>Claude: Here are the findings
    Claude->>Main: Security Report
    Main->>User: Display Report
```

## Project Structure

```
aws-security-agent-skills/
├── skills/
│   ├── s3_detection.py
│   ├── iam_detection.py
│   └── root_login_detection.py
├── tools/
│   ├── tool_definitions.py
│   └── anthropic_integration.py
├── utils/
│   ├── aws_client.py
│   └── logger.py
├── examples/
│   └── demo.py
├── main.py
├── requirements.txt
└── .env
```

## How It Works

1. **User enters a security query** (e.g., "Check my S3 buckets")
2. **main.py sends it to Claude** along with available tools
3. **Claude decides which tool to use** based on the query
4. **anthropic_integration.py executes the chosen tool**
5. **Detection skill runs AWS checks** (S3, IAM, CloudTrail)
6. **Results sent back to Claude** for analysis
7. **Claude formats a readable report**
8. **Report displayed to user**

## Tech Stack

- **Python 3.8+** — Code
- **Anthropic Claude** — AI Intelligence
- **boto3** — AWS API Access
- **python-dotenv** — Credentials Management

## Key Components

| File | Purpose |
|------|---------|
| `main.py` | User interface |
| `anthropic_integration.py` | Claude orchestration |
| `s3_detection.py` | Check S3 security |
| `iam_detection.py` | Check IAM risks |
| `root_login_detection.py` | Check root access |
| `aws_client.py` | AWS authentication |
