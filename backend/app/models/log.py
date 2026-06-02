import uuid
from sqlalchemy import Column, String, DateTime, Text, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base


class Log(Base):
    __tablename__ = "logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    service_name = Column(String, nullable=False, index=True)
    level = Column(String, nullable=False)  # debug, info, warning, error, critical
    message = Column(Text, nullable=False)
    trace_id = Column(String, nullable=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
