from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.core.auth import get_tenant
from app.db.database import get_db
from app.models.tenant import Tenant
from app.models.trace import TraceSpan
from app.schemas.trace import TraceIngest, TraceResponse

router = APIRouter()


@router.post("", response_model=TraceResponse, status_code=status.HTTP_201_CREATED)
async def ingest_trace(
    payload: TraceIngest,
    tenant: Tenant = Depends(get_tenant),
    db: AsyncSession = Depends(get_db),
):
    span = TraceSpan(
        tenant_id=tenant.id,
        trace_id=payload.trace_id,
        span_id=payload.span_id,
        service_name=payload.service_name,
        operation=payload.operation,
        duration_ms=payload.duration_ms,
        status=payload.status,
    )
    db.add(span)
    await db.commit()
    await db.refresh(span)
    return span


@router.get("/{trace_id}", response_model=list[TraceResponse])
async def get_trace(
    trace_id: str,
    tenant: Tenant = Depends(get_tenant),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve all spans for a given trace_id."""
    result = await db.execute(
        select(TraceSpan)
        .where(TraceSpan.tenant_id == tenant.id, TraceSpan.trace_id == trace_id)
        .order_by(TraceSpan.timestamp)
    )
    return result.scalars().all()


@router.get("", response_model=list[TraceResponse])
async def query_traces(
    service_name: str | None = None,
    status: str | None = None,
    limit: int = 100,
    tenant: Tenant = Depends(get_tenant),
    db: AsyncSession = Depends(get_db),
):
    query = select(TraceSpan).where(TraceSpan.tenant_id == tenant.id)

    if service_name:
        query = query.where(TraceSpan.service_name == service_name)
    if status:
        query = query.where(TraceSpan.status == status)

    query = query.order_by(desc(TraceSpan.timestamp)).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()
