from typing import List, Optional
from schemas.designs import DesignCreate, DesignUpdate

from core.config.settings import settings
from google.cloud import firestore



class DesignService:
    """Design Service"""
    def __init__(self):
        self.db = firestore.Client()

    def create_design(self, design_data: DesignCreate) -> dict:
        """Create Design Item"""
        try:
            design_data = design_data.dict()
            self.db.collection(f"{settings.ENVIR}_designs").add(design_data)
            return design_data
        except Exception as exc:
            print(f"Error creating design listing: {exc}")

    # TODO: Create cloud functions to update document with doc id

    def get_all_designs(self) -> List[dict]:
        """Retrieve all Design Items"""
        try:
            designs_ref = self.db.collection(f"{settings.ENVIR}_designs")
            designs = [doc.to_dict() for doc in designs_ref.stream()]
            return designs
        except Exception as exc:
            print(f"Error retrieving design list: {exc}")

    def get_design_by_id(self, design_id: str) -> Optional[dict]:
        """Get Design by ID"""
        try:
            design_ref = self.db.collection(f"{settings.ENVIR}_designs").document(
                design_id
            )
            design = design_ref.get()
            if not design.exists:
                return None
            return design.to_dict()
        except Exception as exc:
            print(f"Error retrieving design by ID: {exc}")

    def update_design(
        self, design_id: str, design_update_data: DesignUpdate
    ) -> Optional[dict]:
        """Update Design Item"""
        try:
            design_ref = self.db.collection(f"{settings.ENVIR}_designs").document(
                design_id
            )
            design_data = design_update_data.dict(exclude_unset=True)
            design_ref.update(design_data)
            design = design_ref.get()
            if not design.exists:
                return None
            return design.to_dict()
        except Exception as exc:
            print(f"Error updating design by ID: {exc}")

    def delete_design(self, design_id: str) -> bool:
        """Delete Design Item"""
        try:
            design_ref = self.db.collection(f"{settings.ENVIR}_designs").document(
                design_id
            )
            design = design_ref.get()
            if not design.exists:
                return False
            design_ref.delete()
            return True
        except Exception as exc:
            print(f"Error deleting design by ID: {exc}")
            return False

    def get_all_designers(self) -> List[dict]:
        """Retrieve all designers"""
        try:
            manufacturer_ref = self.db.collection(f"{settings.ENVIR}_designers")
            designers = [doc.to_dict() for doc in manufacturer_ref.stream()]
            return designers
        except Exception as exc:
            print(f"Error retrieving manufacturer list: {exc}")


