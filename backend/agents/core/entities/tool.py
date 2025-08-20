from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
import uuid


class Tool(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    type: str  # e.g., 'prebuilt', 'custom'
    config: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
