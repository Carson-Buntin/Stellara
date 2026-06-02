from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.core.auth import get_tenant
from app.db.database import get_db
from app.models.tenant import Tenant
from app.models.metric import Metric
from app.schemas.metric import MetricIngest, MetricResponse

router = APIRouter()


@router.post("", response_model=MetricResponse, status_code=status.HTTP_201_CREATED)
async def ingest_metric(
    payload: MetricIngest,
    tenant: Tenant = Depends(get_tenant),
    db: AsyncSession = Depends(get_db),
):
    metric = Metric(
        tenant_id=tenant.id,
        service_name=payload.service_name,
        metric_name=payload.metric_name,
        value=payload.value,
    )
    db.add(metric)
    await db.commit()
    await db.refresh(metric)
    return metric


@router.get("", response_model=list[MetricResponse])
async def query_metrics(
    service_name: str | None = None,
    metric_name: str | None = None,
    limit: int = 100,
    tenant: Tenant = Depends(get_tenant),
    db: AsyncSession = Depends(get_db),
):
    query = select(Metric).where(Metric.tenant_id == tenant.id)

    if service_name:
        query = query.where(Metric.service_name == service_name)
    if metric_name:
        query = query.where(Metric.metric_name == metric_name)

    query = query.order_by(desc(Metric.timestamp)).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()
