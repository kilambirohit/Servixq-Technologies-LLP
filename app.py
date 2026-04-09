from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid
from worker import start_job, jobs

app = FastAPI()

app.mount("/clips", StaticFiles(directory="clips"), name="clips")

class Request(BaseModel):
    url: str

@app.post("/clip")
def create(req: Request):
    job_id = str(uuid.uuid4())
    start_job(job_id, req.url)
    return {"job_id": job_id}

@app.get("/status/{job_id}")
def status(job_id: str):
    return jobs.get(job_id, {"status": "not_found"})
