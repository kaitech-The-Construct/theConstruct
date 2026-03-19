from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse
from .services.mcp_service import MCPService
import json

router = APIRouter()
mcp_service = MCPService()

@router.get("/sse")
async def sse_endpoint(request: Request):
    """
    Exposes the MCP server over Server-Sent Events (SSE).
    AI agents can connect to this endpoint to discover resources and tools.
    """
    async def event_generator():
        # This is a simplified SSE bridge for the MCP server.
        # In a full implementation, we would use the MCP SDK's SSE transport.
        # For the MVP, we expose the discovery endpoints directly.
        
        # Initial heartbeat or server info
        yield {
            "event": "info",
            "data": json.dumps({
                "name": "The Construct MCP Bridge",
                "version": "1.0.0"
            })
        }
        
    return EventSourceResponse(event_generator())

@router.get("/resources")
async def list_resources():
    return await mcp_service.server.list_resources()

@router.get("/tools")
async def list_tools():
    return await mcp_service.server.list_tools()

@router.post("/tools/{tool_name}")
async def call_tool(tool_name: str, arguments: dict):
    return await mcp_service.server.call_tool(tool_name, arguments)
