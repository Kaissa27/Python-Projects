import asyncio
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float

app = FastAPI(title="Hyper-Scale Non-Blocking Data API")

# 1. ASYNCHRONOUS STORAGE CONFIGURATION
# We use the async-compatible sqlite+aiosqlite driver to model a live production asyncpg PostgreSQL setup
ASYNC_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=False, pool_size=20, max_overflow=30)
AsyncSessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class AutomatedMetric(Base):
    __tablename__ = "automated_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    target_node = Column(String(100), nullable=False)
    latency_ms = Column(Float, nullable=False)

# Validation schema for incoming network packets
class MetricIngestionPayload(BaseModel):
    target_node: str = Field(..., min_length=2)
    latency_ms: float = Field(..., ge=0.0)

@app.on_event("startup")
async def db_setup_hook():
    """Asynchronously creates application table definitions on startup."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# =====================================================================
# 2. NON-BLOCKING ASYNC ENDPOINT
# =====================================================================
@app.post("/metrics", status_code=201)
async def ingest_pipeline_metric(payload: MetricIngestionPayload):
    """Asynchronous endpoint handler. Notice the 'async def' and 'await' syntax."""
    
    # Open a clean, non-blocking transactional session line
    async with AsyncSessionLocal() as session:
        try:
            # Instantiate our table object
            new_metric = AutomatedMetric(
                target_node=payload.target_node,
                latency_ms=payload.latency_ms
            )
            
            # Stage the insert operation inside the async session memory pipeline
            session.add(new_metric)
            
            # AWALIT: Here, the code pauses execution of this specific request,
            # releases control of the event loop to handle other web traffic, 
            # and returns right here once the database writes the data to disk.
            await session.commit()
            
            return {"status": "success", "inserted_id": new_metric.id}
            
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Async Database Fail: {str(e)}")

# =====================================================================
# 3. MOCK HIGH-VOLUME CONCURRENCY TEST ENGINE
# =====================================================================
async def simulate_concurrent_load(total_requests=500):
    """Simulates hundreds of scraping nodes hitting the API server simultaneously."""
    async with AsyncSessionLocal() as session:
        print(f"⚡ Booting Event Loop. Coordinating {total_requests} async db operations simultaneously...")
        start_time = time.time()
        
        # Build an array of concurrent asynchronous coroutine tasks
        tasks = []
        for i in range(total_requests):
            metric = AutomatedMetric(target_node=f"Cluster_Node_{i}", latency_ms=12.4 + (i % 5))
            session.add(metric)
            
        # Commit them all concurrently using a unified async transaction
        await session.commit()
        
        elapsed = time.time() - start_time
        print(f"🏁 Asynchronous batch operation completed in {elapsed:.4f} seconds!")

if __name__ == "__main__":
    import uvicorn
    # To run the web server: uvicorn.run(app, host="0.0.0.0", port=8000)
    # Or run the mock concurrency load loop directly:
    asyncio.run(simulate_concurrent_load())
