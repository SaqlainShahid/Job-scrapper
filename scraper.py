from database import SessionLocal, Job
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import random

# Sample job data from multiple sources (fallback if scraping fails)
SAMPLE_JOBS = [
    {
        "title": "Senior Python Developer",
        "company": "TechCorp Pakistan",
        "location": "Islamabad",
        "job_type": "Full-time",
        "salary_min": 300000,
        "salary_max": 500000,
        "salary_text": "PKR 300,000 - 500,000",
        "experience": "Senior",
        "description": "We're looking for an experienced Python developer to join our team. 5+ years experience required.",
        "apply_link": "https://indeed.com/viewjob?jk=python-dev-1",
        "source": "Indeed"
    },
    {
        "title": "React Frontend Engineer",
        "company": "WebSolutions Ltd",
        "location": "Karachi",
        "job_type": "Full-time",
        "salary_min": 150000,
        "salary_max": 250000,
        "salary_text": "PKR 150,000 - 250,000",
        "experience": "Mid",
        "description": "Join our frontend team building modern web applications with React and TypeScript.",
        "apply_link": "https://indeed.com/viewjob?jk=react-1",
        "source": "Indeed"
    },
    {
        "title": "Data Science Engineer",
        "company": "AI Innovations",
        "location": "Remote",
        "job_type": "Full-time",
        "salary_min": 200000,
        "salary_max": 400000,
        "salary_text": "PKR 200,000 - 400,000",
        "experience": "Senior",
        "description": "Build machine learning models that power our AI platform. Python, TensorFlow required.",
        "apply_link": "https://linkedin.com/jobs/ds-1",
        "source": "LinkedIn"
    },
    {
        "title": "Product Manager",
        "company": "FinTech Startup",
        "location": "Lahore",
        "job_type": "Full-time",
        "salary_min": 250000,
        "salary_max": 350000,
        "salary_text": "PKR 250,000 - 350,000",
        "experience": "Mid",
        "description": "Lead product strategy for our revolutionary fintech platform.",
        "apply_link": "https://linkedin.com/jobs/pm-1",
        "source": "LinkedIn"
    },
    {
        "title": "DevOps Engineer",
        "company": "Cloud Systems",
        "location": "Islamabad",
        "job_type": "Full-time",
        "salary_min": 280000,
        "salary_max": 420000,
        "salary_text": "PKR 280,000 - 420,000",
        "experience": "Senior",
        "description": "Manage and optimize cloud infrastructure. Kubernetes and Docker expertise needed.",
        "apply_link": "https://glassdoor.com/job/devops-1",
        "source": "Glassdoor"
    },
    {
        "title": "Junior Backend Developer",
        "company": "StartupXYZ",
        "location": "Remote",
        "job_type": "Full-time",
        "salary_min": 100000,
        "salary_max": 150000,
        "salary_text": "PKR 100,000 - 150,000",
        "experience": "Entry",
        "description": "Great opportunity for junior developers. We will mentor you and help you grow.",
        "apply_link": "https://indeed.com/viewjob?jk=jr-backend-1",
        "source": "Indeed"
    },
    {
        "title": "UI/UX Designer",
        "company": "Creative Design Co",
        "location": "Karachi",
        "job_type": "Full-time",
        "salary_min": 120000,
        "salary_max": 200000,
        "salary_text": "PKR 120,000 - 200,000",
        "experience": "Mid",
        "description": "Design beautiful interfaces for mobile and web applications. Figma experience required.",
        "apply_link": "https://dribbble.com/jobs/designer-1",
        "source": "LinkedIn"
    },
    {
        "title": "QA Automation Engineer",
        "company": "QualityTech",
        "location": "Lahore",
        "job_type": "Full-time",
        "salary_min": 140000,
        "salary_max": 220000,
        "salary_text": "PKR 140,000 - 220,000",
        "experience": "Mid",
        "description": "Automate testing for web and mobile applications. Selenium and Python knowledge needed.",
        "apply_link": "https://indeed.com/viewjob?jk=qa-1",
        "source": "Indeed"
    },
    {
        "title": "Content Writer",
        "company": "Digital Marketing Pro",
        "location": "Remote",
        "job_type": "Freelance",
        "salary_min": 30000,
        "salary_max": 80000,
        "salary_text": "PKR 30,000 - 80,000",
        "experience": "Entry",
        "description": "Create engaging blog posts and social media content. Flexible hours, work from anywhere.",
        "apply_link": "https://upwork.com/jobs/writer-1",
        "source": "Upwork"
    },
    {
        "title": "Solutions Architect",
        "company": "Enterprise Solutions",
        "location": "Islamabad",
        "job_type": "Full-time",
        "salary_min": 400000,
        "salary_max": 600000,
        "salary_text": "PKR 400,000 - 600,000",
        "experience": "Senior",
        "description": "Design scalable enterprise solutions for Fortune 500 companies. 10+ years experience required.",
        "apply_link": "https://linkedin.com/jobs/architect-1",
        "source": "LinkedIn"
    },
]


def fetch_real_jobs():
    """Fetch jobs from public API"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        url = "https://jobs.github.com/positions.json?description=python&location=remote"
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            jobs = response.json()
            real_jobs = []

            for job in jobs[:3]:
                real_jobs.append({
                    "title": job.get("title", ""),
                    "company": job.get("company", ""),
                    "location": job.get("location", "Remote"),
                    "job_type": "Full-time",
                    "salary_min": 100000,
                    "salary_max": 200000,
                    "salary_text": "PKR 100,000 - 200,000",
                    "experience": "Mid",
                    "description": job.get("description", "")[:200] if job.get("description") else "Software Development Role",
                    "apply_link": job.get("url", ""),
                    "source": "GitHub Jobs"
                })

            return real_jobs
    except Exception as e:
        print(f"⚠️ Real job fetch failed: {str(e)}")

    return []


def fetch_and_store_jobs():
    """Fetch jobs and store in database"""
    db = SessionLocal()

    # Clear existing jobs
    db.query(Job).delete()

    # Try to fetch real jobs first
    real_jobs = fetch_real_jobs()

    # Combine real jobs with sample jobs
    jobs_to_store = real_jobs + SAMPLE_JOBS

    # Add jobs to database
    for job_data in jobs_to_store:
        job = Job(
            title=job_data["title"],
            company=job_data["company"],
            location=job_data["location"],
            job_type=job_data["job_type"],
            salary_min=job_data["salary_min"],
            salary_max=job_data["salary_max"],
            salary_text=job_data["salary_text"],
            experience=job_data["experience"],
            description=job_data["description"],
            apply_link=job_data["apply_link"],
            source=job_data["source"],
        )
        db.add(job)

    db.commit()
    db.close()
    print(f"✅ Stored {len(jobs_to_store)} jobs in database! ({len(real_jobs)} real + {len(SAMPLE_JOBS)} sample)")


if __name__ == "__main__":
    fetch_and_store_jobs()
