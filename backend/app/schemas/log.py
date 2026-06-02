from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class LogIngest(BaseModel):
    service_name: str
    level: str
    message: str
    trace_id: Optional[str] = None


class LogResponse(BaseModel):
    id: uuid.UUID
    service_name: str
    level: str
    message: str
    trace_id: Optional[str]
    timestamp: datetime

    model_config = {"from_attributes": True}
