import time
from celery import Celery

# Configure Celery to use Redis as the Message Broker and Result Backend
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task(bind=True)
def heavy_data_scraping_job(self, iterations: int):
    """Simulates a heavy, long-running extraction or ML training computation."""
    print(f" Background Worker accepted job. Processing {iterations} nodes...")
    
    for i in range(iterations):
        # Update progress metadata back to Redis for live tracking
        self.update_state(
            state='PROGRESS',
            meta={'current': i, 'total': iterations, 'percent': int((i / iterations) * 100)}
        )
        time.sleep(0.5) # Simulating dynamic page rendering or model training delays
        
    print(" Background task complete!")
    return {"status": "Complete", "processed_records": iterations}
