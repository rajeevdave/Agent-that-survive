"""
Chapter 4: Tool Calling — Minimal Example

Implements the Tool Use pattern with:
- Typed tool definitions
- Safe tool execution with error handling
- The agent loop (generate → call tools → generate again)

Book reference: Gap 4 (Safety Blindspot) — Least Privilege, path traversal prevention.
Gap 3 (Isolation Problem) — Tool Use + Exception Handling interaction.

Run:
    python chapters/04-tool-calling/minimal/main.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../src"))

from agentic_patterns.llm.providers.base import Message, ToolDefinition
from agentic_patterns.llm.providers.factory import create_provider
from agentic_patterns.utils.logging.logger import get_logger

logger = get_logger(__name__)

# ── Tool definitions ──────────────────────────────────────────────────────────
TOOLS = [
    ToolDefinition(
        name="get_weather",
        description="Get the current weather for a city",
        parameters={
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name, e.g. 'London'"},
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit",
                },
            },
            "required": ["city"],
        },
    ),
    ToolDefinition(
        name="calculate",
        description="Evaluate a safe mathematical expression",
        parameters={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A mathematical expression, e.g. '2 + 2 * 10'",
                }
            },
            "required": ["expression"],
        },
    ),
]


# ── Tool implementations ───────────────────────────────────────────────────────
def get_weather(city: str, unit: str = "celsius") -> dict:
    """Mock weather tool — replace with real API in production."""
    mock_data = {
        "london": {"temp": 15, "condition": "Cloudy", "humidity": 80},
        "new york": {"temp": 22, "condition": "Sunny", "humidity": 55},
        "tokyo": {"temp": 28, "condition": "Hot", "humidity": 70},
    }
    data = mock_data.get(city.lower(), {"temp": 20, "condition": "Clear", "humidity": 60})
    temp = data["temp"] if unit == "celsius" else int(data["temp"] * 9 / 5 + 32)
    return {
        "city": city,
        "temperature": temp,
        "unit": unit,
        "condition": data["condition"],
        "humidity": data["humidity"],
    }


def calculate(expression: str) -> dict:
    """Safe calculator — only allows numeric expressions."""
    import re
    # Allow only digits, operators, spaces, dots, parentheses
    if not re.match(r"^[\d\s\+\-\*\/\.\(\)]+$", expression):
        return {"error": "Invalid expression — only numeric operations allowed"}
    try:
        result = eval(expression, {"__builtins__": {}})  # restricted eval
        return {"expression": expression, "result": result}
    except Exception as exc:
        return {"error": str(exc)}


TOOL_FUNCTIONS = {"get_weather": get_weather, "calculate": calculate}


def run_tool_agent(user_message: str, llm=None) -> str:
    """Run the tool-calling agent loop."""
    llm = llm or create_provider()
    messages = [
        Message(role="system", content="You are a helpful assistant with tools."),
        Message(role="user", content=user_message),
    ]

    MAX_ITERATIONS = 5
    for iteration in range(MAX_ITERATIONS):
        response = llm.complete(messages=messages, tools=TOOLS, max_tokens=500)

        if not response.tool_calls:
            return response.content

        # Add assistant's tool-calling message
        messages.append(
            Message(role="assistant", content=response.content, tool_calls=response.tool_calls)
        )

        # Execute each tool
        for tc in response.tool_calls:
            tool_name = tc["function"]["name"]
            tool_args = json.loads(tc["function"]["arguments"])
            tool_fn = TOOL_FUNCTIONS.get(tool_name)

            if tool_fn:
                result = tool_fn(**tool_args)
                logger.info("tool_executed", tool=tool_name, success="error" not in result)
            else:
                result = {"error": f"Unknown tool: {tool_name}"}

            messages.append(
                Message(role="tool", content=json.dumps(result), tool_call_id=tc["id"])
            )

    return "I wasn't able to complete this task within the allowed steps."


if __name__ == "__main__":
    queries = [
        "What is the weather in London and Tokyo?",
        "What is 15 * 7 + 3?",
        "What's 25% of 840?",
    ]
    for query in queries:
        print(f"\nUser: {query}")
        try:
            answer = run_tool_agent(query)
            print(f"Agent: {answer}")
        except Exception as exc:
            print(f"Error: {exc}")
            break
