# core/services/software_service.py

from typing import List, Optional

from core.config.settings import settings
from fastapi import HTTPException, status
from google.cloud import firestore
from schemas.software import SoftwareCreate, SoftwareResponse, SoftwareUpdate


class SoftwareService:
    def __init__(self):
        self.db = firestore.Client()

    def create_software(self, software: SoftwareCreate) -> SoftwareResponse:
        """Create Software Item"""
        software_data = software.dict()
        new_software_ref = self.db.collection(f"{settings.ENVIR}_software").document()
        new_software_ref.set(software_data)
        new_software_data = new_software_ref.get().to_dict()

        return SoftwareResponse(**new_software_data)

    def get_all_software(self) -> List[SoftwareResponse]:
        """Retrieve all Software Listings"""
        software_list = self.db.collection(f"{settings.ENVIR}_software").get()
        return [SoftwareResponse(**software.to_dict()) for software in software_list]

    def get_software_by_id(self, software_id: str) -> Optional[SoftwareResponse]:
        """Get Software by ID"""
        software_ref = self.db.collection(f"{settings.ENVIR}_software").document(
            software_id
        )
        software = software_ref.get()
        if software.exists:
            return SoftwareResponse(**software.to_dict())
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Software not found"
            )

    def update_software(
        self, software_id: str, software: SoftwareUpdate
    ) -> Optional[SoftwareResponse]:
        """Update Software"""
        software_ref = self.db.collection(f"{settings.ENVIR}_software").document(
            software_id
        )
        software_data = vars(software)
        software_data = {k: v for k, v in software_data.items() if v is not None}
        software_ref.update(software_data)
        updated_software = software_ref.get()
        if updated_software.exists:
            return SoftwareResponse(**updated_software.to_dict())
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Software not found"
            )

    def delete_software(self, version_id: str) -> bool:
        """Delete Software"""
        software_ref = self.db.collection(f"{settings.ENVIR}_software").document(
            version_id
        )
        software = software_ref.get()
        if software.exists:
            software_ref.delete()
            return True
        else:
            return False
