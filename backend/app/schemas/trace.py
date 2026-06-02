from pydantic import BaseModel
from datetime import datetime
import uuid


class TraceIngest(BaseModel):
    trace_id: str
    span_id: str
    service_name: str
    operation: str
    duration_ms: int
    status: str


class TraceResponse(BaseModel):
    id: uuid.UUID
    trace_id: str
    span_id: str
    service_name: str
    operation: str
    duration_ms: int
    status: str
    timestamp: datetime

    model_config = {"from_attributes": True}
