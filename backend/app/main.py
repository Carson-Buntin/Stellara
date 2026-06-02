from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.database import engine, Base
from app.api.v1 import logs, metrics, traces


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Stellara APM Platform",
    description="Unified observability and intelligence platform for modern software systems.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(logs.router, prefix="/v1/logs", tags=["Logs"])
app.include_router(metrics.router, prefix="/v1/metrics", tags=["Metrics"])
app.include_router(traces.router, prefix="/v1/traces", tags=["Traces"])


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
