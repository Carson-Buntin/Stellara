"""
Run once after first startup to seed a test tenant.
Usage: python seed.py
"""
import asyncio
from app.db.database import AsyncSessionLocal, engine, Base
from app.models.tenant import Tenant


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        tenant = Tenant(name="Test Org", api_key="sk_test_123")
        session.add(tenant)
        await session.commit()
        print(f"Created tenant: {tenant.name} | API Key: {tenant.api_key}")


if __name__ == "__main__":
    asyncio.run(seed())
