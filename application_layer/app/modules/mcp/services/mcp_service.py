import json
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource
from ...common.samples.sample_data import design_catalog

class MCPService:
    def __init__(self):
        self.server = Server("the-construct")
        self._setup_handlers()

    def _setup_handlers(self):
        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            return [
                Resource(
                    uri="mcp://theconstruct/robotics/designs",
                    name="Robot Design Catalog",
                    mimeType="application/json",
                    description="A catalog of available robot designs and their specifications"
                )
            ]

        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            if uri == "mcp://theconstruct/robotics/designs":
                return json.dumps(design_catalog, indent=2)
            raise ValueError(f"Unknown resource: {uri}")

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="search_designs",
                    description="Search for robot designs by name or manufacturer",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search term"},
                            "manufacturer": {"type": "string", "description": "Filter by manufacturer"}
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="get_balance",
                    description="Check the XRP balance of a specific address",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "address": {"type": "string", "description": "The XRPL address to check"}
                        },
                        "required": ["address"]
                    }
                ),
                Tool(
                    name="check_nft_status",
                    description="Verify if a robot design has been minted on-chain",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "robot_id": {"type": "string", "description": "The ID of the robot to check"}
                        },
                        "required": ["robot_id"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent | ImageContent | EmbeddedResource]:
            if name == "search_designs":
                query = arguments.get("query", "").lower()
                manufacturer = arguments.get("manufacturer", "").lower()
                
                results = [
                    d for d in design_catalog 
                    if (query in d["name"].lower() or query in d["description"].lower())
                    and (not manufacturer or manufacturer in d.get("manufacturer_id", "").lower())
                ]
                
                return [TextContent(type="text", text=json.dumps(results, indent=2))]
            
            elif name == "get_balance":
                from ...ledger.services.blockchain_service import BlockchainService
                blockchain = BlockchainService()
                balance = await blockchain.get_account_balance(arguments["address"])
                return [TextContent(type="text", text=f"Balance: {balance} XRP")]

            elif name == "check_nft_status":
                from ...robotics.services.robot_service import RobotService
                robot_service = RobotService()
                robot = robot_service.get_robot_by_id(arguments["robot_id"])
                if not robot:
                    return [TextContent(type="text", text="Robot not found")]
                
                status = robot.get("blockchain", {"is_minted": False})
                return [TextContent(type="text", text=json.dumps(status, indent=2))]
            
            raise ValueError(f"Unknown tool: {name}")

    def get_server(self):
        return self.server
