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
                ),
                Resource(
                    uri="mcp://theconstruct/market/bounties",
                    name="Active Bounties",
                    mimeType="application/json",
                    description="A list of open bounties / feature requests available for agent contributions"
                )
            ]

        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            if uri == "mcp://theconstruct/robotics/designs":
                return json.dumps(design_catalog, indent=2)
            if uri == "mcp://theconstruct/market/bounties":
                from ...market.services.bounty_service import BountyService
                bounties = BountyService().list_bounties()
                return json.dumps([b.dict() for b in bounties], indent=2, default=str)
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
                ),
                Tool(
                    name="get_bounty",
                    description="Retrieve full details for a specific bounty by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "bounty_id": {"type": "string", "description": "The ID of the bounty"}
                        },
                        "required": ["bounty_id"]
                    }
                ),
                Tool(
                    name="submit_agent_work_hitl",
                    description="Submit agent work in Human-in-the-Loop mode. Sends a Xaman sign request to the developer.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "bounty_id": {"type": "string", "description": "The ID of the bounty to submit work for"},
                            "agent_id": {"type": "string", "description": "The ID of the agent submitting"},
                            "developer_wallet": {"type": "string", "description": "The developer's XRPL wallet address"},
                            "code_hash": {"type": "string", "description": "Hash of the submitted code or PR URL"},
                            "submission_details": {"type": "string", "description": "Description of the work completed"},
                            "test_results": {"type": "object", "description": "Dictionary mapping test names to boolean success status"}
                        },
                        "required": ["bounty_id", "agent_id", "developer_wallet", "code_hash", "submission_details", "test_results"]
                    }
                ),
                Tool(
                    name="submit_agent_work_auto",
                    description="Submit agent work autonomously using a pre-signed XRPL transaction blob (Regular Key).",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "bounty_id": {"type": "string", "description": "The ID of the bounty to submit work for"},
                            "agent_id": {"type": "string", "description": "The ID of the agent submitting"},
                            "developer_wallet": {"type": "string", "description": "The developer's XRPL wallet address"},
                            "code_hash": {"type": "string", "description": "Hash of the submitted code or PR URL"},
                            "submission_details": {"type": "string", "description": "Description of the work completed"},
                            "test_results": {"type": "object", "description": "Dictionary mapping test names to boolean success status"},
                            "signed_tx_blob": {"type": "string", "description": "The pre-signed XRPL transaction blob"}
                        },
                        "required": ["bounty_id", "agent_id", "developer_wallet", "code_hash", "submission_details", "test_results", "signed_tx_blob"]
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
            
            elif name == "get_bounty":
                from ...market.services.bounty_service import BountyService
                bounty_service = BountyService()
                bounty = bounty_service.get_bounty(arguments["bounty_id"])
                if not bounty:
                    return [TextContent(type="text", text="Bounty not found")]
                return [TextContent(type="text", text=json.dumps(bounty.dict(), indent=2, default=str))]

            elif name == "submit_agent_work_hitl":
                from ...market.services.bounty_service import BountyService
                from ...market.schemas.bounty import AgentSubmission
                bounty_service = BountyService()
                submission = AgentSubmission(
                    agent_id=arguments["agent_id"],
                    developer_wallet=arguments["developer_wallet"],
                    code_hash=arguments["code_hash"],
                    submission_details=arguments["submission_details"],
                    test_results=arguments["test_results"]
                )
                try:
                    result = bounty_service.submit_agent_work_hitl(arguments["bounty_id"], submission)
                    return [TextContent(type="text", text=json.dumps(result, indent=2))]
                except Exception as e:
                    return [TextContent(type="text", text=f"Error: {str(e)}")]

            elif name == "submit_agent_work_auto":
                from ...market.services.bounty_service import BountyService
                from ...market.schemas.bounty import AgentAutonomousSubmission
                bounty_service = BountyService()
                submission = AgentAutonomousSubmission(
                    agent_id=arguments["agent_id"],
                    developer_wallet=arguments["developer_wallet"],
                    code_hash=arguments["code_hash"],
                    submission_details=arguments["submission_details"],
                    test_results=arguments["test_results"],
                    signed_tx_blob=arguments["signed_tx_blob"]
                )
                try:
                    result = bounty_service.submit_agent_work_autonomous(arguments["bounty_id"], submission)
                    return [TextContent(type="text", text=json.dumps(result, indent=2))]
                except Exception as e:
                    return [TextContent(type="text", text=f"Error: {str(e)}")]
            
            raise ValueError(f"Unknown tool: {name}")

    def get_server(self):
        return self.server
