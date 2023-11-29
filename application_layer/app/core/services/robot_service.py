# core/services/robot_service.py

from typing import List, Optional

from core.config.settings import settings
from google.cloud import firestore
from schemas.robot import RobotCreate, RobotUpdate


class RobotService:
    def __init__(self):
        self.db = firestore.Client()

    def create_robot(self, robot_data: RobotCreate) -> dict:
        """Create Robot Item"""
        try:
            robot_data = robot_data.dict()
            self.db.collection(f"{settings.ENVIR}_robots").add(robot_data)
            return robot_data
        except Exception as exc:
            print(f"Error creating robot listing: {exc}")

    # TODO: Create cloud functions to update document with doc id

    def get_all_robots(self) -> List[dict]:
        """Retrieve all Robot Items"""
        try:
            robots_ref = self.db.collection(f"{settings.ENVIR}_robots")
            robots = [doc.to_dict() for doc in robots_ref.stream()]
            return robots
        except Exception as exc:
            print(f"Error retrieving robot list: {exc}")

    def get_robot_by_id(self, robot_id: str) -> Optional[dict]:
        """Get Robot by ID"""
        try:
            robot_ref = self.db.collection(f"{settings.ENVIR}_robots").document(
                robot_id
            )
            robot = robot_ref.get()
            if not robot.exists:
                return None
            return robot.to_dict()
        except Exception as exc:
            print(f"Error retrieving robot by ID: {exc}")

    def update_robot(
        self, robot_id: str, robot_update_data: RobotUpdate
    ) -> Optional[dict]:
        """Update Robot Item"""
        try:
            robot_ref = self.db.collection(f"{settings.ENVIR}_robots").document(
                robot_id
            )
            robot_data = robot_update_data.dict(exclude_unset=True)
            robot_ref.update(robot_data)
            robot = robot_ref.get()
            if not robot.exists:
                return None
            return robot.to_dict()
        except Exception as exc:
            print(f"Error updating robot by ID: {exc}")

    def delete_robot(self, robot_id: str) -> bool:
        """Delete Robot Item"""
        try:
            robot_ref = self.db.collection(f"{settings.ENVIR}_robots").document(
                robot_id
            )
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
