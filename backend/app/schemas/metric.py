from pydantic import BaseModel
from datetime import datetime
import uuid


class MetricIngest(BaseModel):
    service_name: str
    metric_name: str
    value: float


class MetricResponse(BaseModel):
    id: uuid.UUID
    service_name: str
    metric_name: str
    value: float
    timestamp: datetime

    model_config = {"from_attributes": True}
