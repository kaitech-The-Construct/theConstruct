from typing import List, Optional, Any

from core.config.settings import settings
from google.cloud import firestore
from ..schemas.robot import RobotCreate, RobotUpdate
from ...ledger.services.blockchain_service import BlockchainService

class RobotService:
    def __init__(self):
        self.db = firestore.Client()
        self.robots_collection = self.db.collection(f"{settings.ENVIR}_robots")
        self.blockchain = BlockchainService(ledger_type="xrpl")

    async def create_robot(self, robot_data: RobotCreate, mint_on_chain: bool = False, wallet: Optional[Any] = None) -> dict:
        """
        Create Robot Item and optionally mint it as an NFT on-chain.
        """
        try:
            robot_dict = robot_data.dict()
            robot_dict["ratings"] = {"average": 0, "count": 0}
            
            # If minting on chain is requested
            if mint_on_chain and wallet:
                # In a real scenario, we'd upload metadata to IPFS first
                metadata_uri = f"https://api.theconstruct.io/robots/metadata/{robot_data.name}"
                tx_hash = await self.blockchain.mint_robot_blueprint(wallet, metadata_uri)
                robot_dict["blockchain"] = {
                    "network": "xrpl-testnet",
                    "mint_tx_hash": tx_hash,
                    "is_minted": True
                }

            doc_ref = self.robots_collection.document()
            doc_ref.set(robot_dict)
            robot_dict["id"] = doc_ref.id
            return robot_dict
        except Exception as exc:
            print(f"Error creating robot listing: {exc}")
            return {}

    def get_all_robots(self) -> List[dict]:
        """Retrieve all Robot Items"""
        try:
            robots = []
            for doc in self.robots_collection.stream():
                robot_dict = doc.to_dict()
                robot_dict["id"] = doc.id
                robots.append(robot_dict)
            return robots
        except Exception as exc:
            print(f"Error retrieving robot list: {exc}")
            return []

    def get_robot_by_id(self, robot_id: str) -> Optional[dict]:
        """Get Robot by ID"""
        try:
            robot_ref = self.robots_collection.document(robot_id)
            robot = robot_ref.get()
            if not robot.exists:
                return None
            robot_dict = robot.to_dict()
            robot_dict["id"] = robot.id
            return robot_dict
        except Exception as exc:
            print(f"Error retrieving robot by ID: {exc}")
            return None

    def update_robot(
        self, robot_id: str, robot_update_data: RobotUpdate
    ) -> Optional[dict]:
        """Update Robot Item"""
        try:
            robot_ref = self.robots_collection.document(robot_id)
            robot_data = robot_update_data.dict(exclude_unset=True)
            robot_ref.update(robot_data)
            robot = robot_ref.get()
            if not robot.exists:
                return None
            robot_dict = robot.to_dict()
            robot_dict["id"] = robot.id
            return robot_dict
        except Exception as exc:
            print(f"Error updating robot by ID: {exc}")
            return None

    def delete_robot(self, robot_id: str) -> bool:
        """Delete Robot Item"""
        try:
            robot_ref = self.robots_collection.document(robot_id)
            robot = robot_ref.get()
            if not robot.exists:
                return False
            robot_ref.delete()
            return True
        except Exception as exc:
            print(f"Error deleting robot by ID: {exc}")
            return False

    def get_all_manufacturers(self) -> List[dict]:
        """Retrieve all manufacturers"""
        try:
            manufacturer_ref = self.db.collection(f"{settings.ENVIR}_manufacturers")
            manufacturers = [doc.to_dict() for doc in manufacturer_ref.stream()]
            return manufacturers
        except Exception as exc:
            print(f"Error retrieving manufacturer list: {exc}")
            return []

    def advanced_search(self, filters: dict) -> List[dict]:
        """Advanced search with filters"""
        try:
            query = self.robots_collection
            
            # Apply filters
            if filters.get("min_price"):
                query = query.where("price.listing_price", ">=", filters["min_price"])
            if filters.get("max_price"):
                query = query.where("price.listing_price", "<=", filters["max_price"])
            if filters.get("manufacturer"):
                query = query.where("manufacturer", "==", filters["manufacturer"])
            if filters.get("category"):
                query = query.where("specifications.technical.category", "==", filters["category"])
            if filters.get("min_rating"):
                query = query.where("ratings.average", ">=", filters["min_rating"])
            
            robots = []
            for doc in query.stream():
                robot_dict = doc.to_dict()
                robot_dict["id"] = doc.id
                robots.append(robot_dict)
            
            return robots
        except Exception as exc:
            print(f"Error in advanced search: {exc}")
            return []

    def get_recommendations(self, user_id: str) -> List[dict]:
        """Get product recommendations for a user"""
        try:
            query = self.robots_collection.order_by("ratings.average", direction=firestore.Query.DESCENDING).limit(10)
            
            robots = []
            for doc in query.stream():
                robot_dict = doc.to_dict()
                robot_dict["id"] = doc.id
                robots.append(robot_dict)
            
            return robots
        except Exception as exc:
            print(f"Error getting recommendations: {exc}")
            return []

    def manage_inventory(self, product_id: str, inventory_data: dict) -> bool:
        """Manage product inventory"""
        try:
            robot_ref = self.robots_collection.document(product_id)
            inventory_update = {f"inventory.{key}": value for key, value in inventory_data.items()}
            robot_ref.update(inventory_update)
            return True
        except Exception as exc:
            print(f"Error managing inventory: {exc}")
            return False

    def handle_product_reviews(self, product_id: str, review_data: dict) -> bool:
        """Handle product reviews and update ratings"""
        try:
            reviews_ref = self.db.collection(f"{settings.ENVIR}_reviews")
            review_data["product_id"] = product_id
            review_data["created_at"] = firestore.SERVER_TIMESTAMP
            reviews_ref.add(review_data)
            
            robot_ref = self.robots_collection.document(product_id)
            robot = robot_ref.get()
            if robot.exists:
                robot_data = robot.to_dict()
                current_ratings = robot_data.get("ratings", {"average": 0, "count": 0})
                
                total_rating = current_ratings["average"] * current_ratings["count"]
                new_count = current_ratings["count"] + 1
                new_average = (total_rating + review_data["rating"]) / new_count
                
                robot_ref.update({
                    "ratings.average": new_average,
                    "ratings.count": new_count
                })
            
            return True
        except Exception as exc:
            print(f"Error handling product review: {exc}")
            return False

    def track_product_analytics(self, product_id: str) -> dict:
        """Track product analytics"""
        try:
            robot = self.get_robot_by_id(product_id)
            if not robot:
                return {}
            
            reviews_ref = self.db.collection(f"{settings.ENVIR}_reviews")
            reviews = reviews_ref.where("product_id", "==", product_id).stream()
            review_count = len(list(reviews))
            
            orders_ref = self.db.collection(f"{settings.ENVIR}_orders")
            orders = orders_ref.where("items", "array_contains", {"product_id": product_id}).stream()
            order_count = len(list(orders))
            
            return {
                "views": robot.get("views", 0),
                "orders": order_count,
                "reviews": review_count,
                "rating": robot.get("ratings", {}).get("average", 0),
                "inventory": robot.get("inventory", {})
            }
        except Exception as exc:
            print(f"Error tracking product analytics: {exc}")
            return {}
