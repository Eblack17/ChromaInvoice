from typing import Any, Dict, List
from langchain.callbacks import get_openai_callback
from langchain.schema import AgentAction, AgentFinish

def get_token_usage(func):
    """Decorator to track token usage of LangChain operations"""
    def wrapper(*args, **kwargs):
        with get_openai_callback() as cb:
            result = func(*args, **kwargs)
            print(f"\nToken usage:")
            print(f"- Prompt tokens: {cb.prompt_tokens}")
            print(f"- Completion tokens: {cb.completion_tokens}")
            print(f"- Total tokens: {cb.total_tokens}")
            print(f"- Cost: ${cb.total_cost:.4f}")
        return result
    return wrapper

def format_agent_action(action: AgentAction) -> str:
    """Format an agent action for logging"""
    return f"Action: {action.tool}\nAction Input: {action.tool_input}\n"

def format_agent_finish(finish: AgentFinish) -> str:
    """Format an agent finish for logging"""
    return f"Final Answer: {finish.return_values['output']}\n"

def safe_parse_json(text: str) -> Dict[str, Any]:
    """Safely parse JSON from text"""
    try:
        import json
        return json.loads(text)
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON", "text": text} 