from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import SessionLocal, Job
from scraper import fetch_and_store_jobs
from typing import List, Optional

app = FastAPI(title="Job Scraper API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    job_type: str
    salary_text: str
    salary_min: Optional[float]
    salary_max: Optional[float]
    experience: str
    description: str
    apply_link: str
    source: str

    class Config:
        from_attributes = True


@app.on_event("startup")
def startup_event():
    """Load jobs on startup"""
    fetch_and_store_jobs()


@app.get("/")
def read_root():
    return {
        "message": "🎯 Job Scraper API",
        "docs": "/docs",
        "endpoints": {
            "search": "/api/jobs?search=python",
            "filter": "/api/jobs?location=Islamabad&min_salary=100000"
        }
    }


@app.get("/api/jobs", response_model=List[JobResponse])
def search_jobs(
    search: Optional[str] = Query(None, description="Search by job title or company"),
    location: Optional[str] = Query(None, description="Filter by location"),
    job_type: Optional[str] = Query(None, description="Filter by job type"),
    min_salary: Optional[float] = Query(None, description="Minimum salary"),
    max_salary: Optional[float] = Query(None, description="Maximum salary"),
    experience: Optional[str] = Query(None, description="Filter by experience level"),
    skip: int = Query(0),
    limit: int = Query(20),
):
    """Search and filter jobs"""
    db = SessionLocal()

    query = db.query(Job)

    # Search filter
    if search:
        search_term = f"%{search.lower()}%"
        query = query.filter(
            (Job.title.ilike(search_term)) |
            (Job.company.ilike(search_term)) |
            (Job.description.ilike(search_term))
        )

    # Location filter
    if location:
        query = query.filter(Job.location == location)

    # Job type filter
    if job_type:
        query = query.filter(Job.job_type == job_type)

    # Salary filters
    if min_salary:
        query = query.filter(Job.salary_min >= min_salary)

    if max_salary:
        query = query.filter(Job.salary_max <= max_salary)

    # Experience filter
    if experience:
        query = query.filter(Job.experience == experience)

    jobs = query.offset(skip).limit(limit).all()
    db.close()

    return jobs


@app.get("/api/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int):
    """Get specific job details"""
    db = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()
    db.close()

    if not job:
        return {"error": "Job not found"}

    return job


@app.get("/api/filters")
def get_available_filters():
    """Get available filter options"""
    db = SessionLocal()

    locations = [item[0] for item in db.query(Job.location).distinct().all()]
    job_types = [item[0] for item in db.query(Job.job_type).distinct().all()]
    experiences = [item[0] for item in db.query(Job.experience).distinct().all()]

    db.close()

    return {
        "locations": locations,
        "job_types": job_types,
        "experiences": experiences,
    }


@app.post("/api/refresh")
def refresh_jobs():
    """Manually refresh jobs from scraper"""
    try:
        fetch_and_store_jobs()
        return {"message": "✅ Jobs refreshed successfully"}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
