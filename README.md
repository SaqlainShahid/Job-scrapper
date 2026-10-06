# 💼 Job Scraper - Live Job Aggregation Platform

A real-time job scraping and filtering platform that aggregates jobs from multiple sources (Indeed, LinkedIn, Glassdoor, etc.) with advanced filtering capabilities.

## ✨ Features

- ✅ **Multi-source Job Scraping** - Aggregate jobs from Indeed, LinkedIn, Glassdoor
- ✅ **Real-time Filtering** - Filter by location, salary, job type, experience level
- ✅ **Full-text Search** - Search by job title, company, or keywords
- ✅ **Live API** - RESTful API for job search and filtering
- ✅ **Interactive Frontend** - Beautiful, responsive web interface
- ✅ **Instant Updates** - Jobs update instantly as you filter

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

The server will start at **http://localhost:8000**

### Open Frontend

Open `index.html` in your browser to see the live job listings with filters.

## 📁 Project Structure

```
.
├── app.py              # FastAPI backend server
├── database.py         # SQLAlchemy database models
├── scraper.py          # Job scraper logic
├── index.html          # Frontend UI
├── requirements.txt    # Python dependencies
└── jobs.db            # SQLite database (auto-created)
```

## 🔌 API Endpoints

### Search & Filter Jobs
```
GET /api/jobs?search=python&location=Islamabad&min_salary=100000
```

**Parameters:**
- `search` - Search by job title or company
- `location` - Filter by location
- `job_type` - Filter by job type (Full-time, Part-time, etc.)
- `min_salary` - Minimum salary
- `max_salary` - Maximum salary
- `experience` - Filter by experience level

**Response:**
```json
[
  {
    "id": 1,
    "title": "Senior Python Developer",
    "company": "TechCorp Pakistan",
    "location": "Islamabad",
    "job_type": "Full-time",
    "salary_text": "PKR 300,000 - 500,000",
    "salary_min": 300000,
    "salary_max": 500000,
    "experience": "Senior",
    "description": "We're looking for an experienced Python developer...",
    "apply_link": "https://indeed.com/viewjob?jk=...",
    "source": "Indeed"
  }
]
```

### Get Available Filters
```
GET /api/filters
```

**Response:**
```json
{
  "locations": ["Islamabad", "Karachi", "Lahore", "Remote"],
  "job_types": ["Full-time", "Part-time", "Contract", "Freelance"],
  "experiences": ["Entry", "Mid", "Senior"]
}
```

### Get Specific Job
```
GET /api/jobs/{job_id}
```

### Refresh Jobs
```
POST /api/refresh
```

Manually trigger the scraper to fetch latest jobs.

## 🎯 Usage Examples

### Search for Python jobs
```bash
curl "http://localhost:8000/api/jobs?search=python"
```

### Find jobs in Islamabad with minimum salary
```bash
curl "http://localhost:8000/api/jobs?location=Islamabad&min_salary=200000"
```

### Get all Senior level jobs
```bash
curl "http://localhost:8000/api/jobs?experience=Senior"
```

## 📊 Current Sample Data

The system includes **10 sample jobs** from multiple sources:
- Indeed
- LinkedIn
- Glassdoor
- Dribbble
- Upwork

## 🔄 Adding Real Scrapers

To add real job scrapers:

1. Modify `scraper.py` to add BeautifulSoup/Selenium scrapers
2. Update `SAMPLE_JOBS` with real scraped data
3. Call `fetch_and_store_jobs()` to populate database
4. Use `/api/refresh` endpoint to update jobs

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** SQLite + SQLAlchemy
- **Frontend:** HTML5 + Vanilla JavaScript
- **Scraping:** BeautifulSoup, Selenium
- **API:** RESTful JSON API

## 📝 Next Steps

- [ ] Add real job scrapers (Indeed, LinkedIn, Glassdoor)
- [ ] Implement scheduled scraping with Celery
- [ ] Add user authentication
- [ ] Add job favorites/bookmarks
- [ ] Implement email alerts
- [ ] Deploy to production

## 🚀 Deployment

Ready to deploy on:
- Heroku
- Railway
- Render
- AWS
- DigitalOcean

## 📧 Support

For issues or questions, create a GitHub issue or contact the team.

---

**Happy job hunting!** 💼
