import uuid
from sqlalchemy import Column, String, DateTime, Float, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    service_name = Column(String, nullable=False, index=True)
    metric_name = Column(String, nullable=False, index=True)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
