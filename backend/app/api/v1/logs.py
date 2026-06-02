from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.core.auth import get_tenant
from app.db.database import get_db
from app.models.tenant import Tenant
from app.models.log import Log
from app.schemas.log import LogIngest, LogResponse

router = APIRouter()


@router.post("", response_model=LogResponse, status_code=status.HTTP_201_CREATED)
async def ingest_log(
    payload: LogIngest,
    tenant: Tenant = Depends(get_tenant),
    db: AsyncSession = Depends(get_db),
):
    log = Log(
        tenant_id=tenant.id,
        service_name=payload.service_name,
        level=payload.level,
        message=payload.message,
        trace_id=payload.trace_id,
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


@router.get("", response_model=list[LogResponse])
async def query_logs(
    service_name: str | None = None,
    level: str | None = None,
    limit: int = 100,
    tenant: Tenant = Depends(get_tenant),
    db: AsyncSession = Depends(get_db),
):
    query = select(Log).where(Log.tenant_id == tenant.id)

    if service_name:
        query = query.where(Log.service_name == service_name)
    if level:
        query = query.where(Log.level == level)

    query = query.order_by(desc(Log.timestamp)).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()
