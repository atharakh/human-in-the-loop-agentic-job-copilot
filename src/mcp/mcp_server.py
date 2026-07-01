import json
from datetime import datetime

from src.mcp.tool_registry import MCPToolRegistry


class SimpleMCPServer:
    """
    Lightweight MCP-style server abstraction.

    It exposes internal project functions through:
    - list_tools()
    - call_tool()
    - get_status()

    This demonstrates MCP readiness without requiring an external MCP package.
    """

    def __init__(self):
        self.registry = MCPToolRegistry()
        self.started_at = datetime.now().isoformat()

    def get_status(self) -> dict:
        tools = self.registry.list_tools()

        return {
            "service": "SimpleMCPServer",
            "status": "active",
            "started_at": self.started_at,
            "tools_count": len(tools),
            "tools": tools,
        }

    def list_tools(self) -> list[dict]:
        return self.registry.list_tools()

    def call_tool(self, tool_name: str, payload: dict) -> dict:
        return {
            "tool_name": tool_name,
            "payload": payload,
            "result": self.registry.run_tool(tool_name, payload),
        }


def demo():
    server = SimpleMCPServer()

    print("\nMCP SERVER STATUS")
    print(json.dumps(server.get_status(), indent=2))

    print("\nMCP DEMO TOOL CALL")
    response = server.call_tool(
        "ask_ai",
        {
            "question": "Which candidates have Python experience?"
        },
    )

    print(json.dumps(response, indent=2, default=str))


if __name__ == "__main__":
    demo()

    