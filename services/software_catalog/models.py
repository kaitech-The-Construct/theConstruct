from typing import List

from pydantic import BaseModel

class SoftwareDetails(BaseModel):
    """Software details model"""
    name: str
    version: str
    author: str
    description: str
    compatibility: List[str]
    license: str
    documentation_url: str
    image_url: str | None = None