import anthropic
import json
from os import getenv
from skills.s3_detection import check_s3_public_buckets
from skills.iam_detection import check_privilege_escalation
from skills.root_login_detection import check_root_login_activity
from tools.tool_definitions import TOOLS

client = anthropic.Anthropic(api_key=getenv('ANTHROPIC_API_KEY'))

def execute_tool(tool_name):
    """Execute detection based on tool name"""
    if tool_name == "check_s3_public_buckets":
        return check_s3_public_buckets()
    elif tool_name == "check_privilege_escalation":
        return check_privilege_escalation()
    elif tool_name == "check_root_login_activity":
        return check_root_login_activity()
    else:
        return {"error": "Unknown tool"}

def run_security_analysis(user_query):
    """Run security analysis with Claude using tool-use"""
    
    messages = [{"role": "user", "content": user_query}]
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=TOOLS,
        messages=messages
    )
    
    while response.stop_reason == "tool_use":
        tool_use = next(block for block in response.content if block.type == "tool_use")
        tool_name = tool_use.name
        
        result = execute_tool(tool_name)
        
        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": json.dumps(result)
                }
            ]
        })
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages
        )
    
    final_response = next(
        (block.text for block in response.content if hasattr(block, "text")),
        None
    )
    
    return final_response