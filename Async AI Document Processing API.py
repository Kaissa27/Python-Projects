from fastapi import FastAPI, BackgroundTasks, UploadFile, File
import uuid
import time

app = FastAPI(title="Async AI Processing API")

# Simple in-memory database for demo purposes
jobs_db = {}

def process_document_with_ai(job_id: str, file_contents: bytes):
    """Simulates background text extraction and AI summarization."""
    jobs_db[job_id]["status"] = "processing"
    
    # Simulate heavy parsing & AI call delay
    time.sleep(5) 
    
    # Placeholder for actual LLM response logic
    summary = f"Processed {len(file_contents)} bytes. Key insight: The document is valid."
    
    jobs_db[job_id]["status"] = "completed"
    jobs_db[job_id]["result"] = summary

@app.post("/api/v1/documents/upload")
async def upload_document(
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...)
):
    job_id = str(uuid.uuid4())
    contents = await file.read()
    
    jobs_db[job_id] = {"status": "pending", "result": None}
    
    # Offload the slow AI processing to the background
    background_tasks.add_task(process_document_with_ai, job_id, contents)
    
    return {"job_id": job_id, "status": "pending", "message": "File processing started."}

@app.get("/api/v1/jobs/{job_id}")
async def get_job_status(job_id: str):
    job = jobs_db.get(job_id)
    if not job:
        return {"error": "Job not found"}
    return job
