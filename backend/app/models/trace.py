import uuid
from sqlalchemy import Column, String, DateTime, Integer, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base


class TraceSpan(Base):
    __tablename__ = "trace_spans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    trace_id = Column(String, nullable=False, index=True)
    span_id = Column(String, nullable=False)
    service_name = Column(String, nullable=False, index=True)
    operation = Column(String, nullable=False)
    duration_ms = Column(Integer, nullable=False)
    status = Column(String, nullable=False)  # ok, error, timeout
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
