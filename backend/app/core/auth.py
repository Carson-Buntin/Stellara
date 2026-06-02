from fastapi import Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.models.tenant import Tenant
from fastapi import Depends


# For MVP, we resolve tenant from the API key directly via DB lookup.
async def get_tenant(
    api_key: str = Header(..., alias="api_key"),
    db: AsyncSession = Depends(get_db),
) -> Tenant:
    result = await db.execute(select(Tenant).where(Tenant.api_key == api_key))
    tenant = result.scalar_one_or_none()

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )

    return tenant
