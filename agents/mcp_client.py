from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
import requests
from typing import Dict, Any



class MCPClient:
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.message_id = 0
        self.session = requests.Session()
    
    def _next_id(self) -> int:
        self.message_id += 1
        return self.message_id
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call an MCP tool and return the result"""
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            },
            "id": self._next_id()
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/message",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            if "error" in result:
                return f"Error: {result['error']['message']}"
            
            content = result.get("result", {}).get("content", [])
            if content and len(content) > 0:
                return content[0].get("text", "No result")
            return "No result"
            
        except Exception as e:
            return f"MCP Error: {str(e)}"
    
    def read_resource(self, uri: str) -> str:
        """Read an MCP resource"""
        payload = {
            "jsonrpc": "2.0",
            "method": "resources/read",
            "params": {"uri": uri},
            "id": self._next_id()
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/message",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            if "error" in result:
                return f"Error: {result['error']['message']}"
            
            contents = result.get("result", {}).get("contents", [])
            if contents and len(contents) > 0:
                return contents[0].get("text", "No content")
            return "No content"
            
        except Exception as e:
            return f"MCP Error: {str(e)}"


# Initialize MCP client (global)
mcp = MCPClient()