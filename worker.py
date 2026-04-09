import threading
from pipeline import run_pipeline

jobs = {}

def process(job_id, url):
    jobs[job_id] = {"status": "processing"}
    try:
        clips = run_pipeline(url, job_id)
        jobs[job_id] = {
            "status": "done",
            "clips": clips
        }
    except Exception as e:
        jobs[job_id] = {"status": "error", "error": str(e)}

def start_job(job_id, url):
    jobs[job_id] = {"status": "queued"}
    threading.Thread(target=process, args=(job_id, url)).start()
