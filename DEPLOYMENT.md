# 🚀 Job Scraper - Deployment Guide

Complete guide to deploy Job Scraper on Railway, Render, and Netlify.

---

## **Option 1: Railway (Backend) - RECOMMENDED** ⭐

### Quick Deploy:
1. Go to: https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select: `SaqlainShahid/Job-scrapper`
5. Click "Deploy"

### Manual Setup:
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

**Result:** Backend will be at `https://[your-railway-app].railway.app`

---

## **Option 2: Netlify (Frontend)**

### Method A: Direct GitHub Connection (Best)
1. Go to: https://netlify.com
2. Click "Add new site" → "Import from Git"
3. Select GitHub → Choose `SaqlainShahid/Job-scrapper`
4. Branch: `main`
5. Build command: Leave empty (or `echo 'Static'`)
6. Publish directory: `.`
7. Click "Deploy"

### Method B: Manual Deploy
```bash
npm install -g netlify-cli
netlify login
netlify deploy --prod --dir .
```

**Result:** Frontend at `https://[your-netlify-site].netlify.app`

---

## **Option 3: Render (Fallback)**

### For Backend:
1. https://render.com → New → Web Service
2. Connect GitHub → `SaqlainShahid/Job-scrapper`
3. Runtime: Docker
4. Click "Deploy"

### For Frontend:
1. https://render.com → New → Static Site
2. Connect GitHub → `SaqlainShahid/Job-scrapper`
3. Publish directory: `.`
4. Click "Deploy"

---

## **Update Frontend API URL**

After getting backend URL, update in `index.html`:

Find this line (around line 239):
```javascript
const API_BASE = "https://job-scraper-backend-0ugv.onrender.com/api";
```

Replace with your new backend URL:
```javascript
const API_BASE = "https://your-railway-app.railway.app/api";
```

Then commit & push:
```bash
git add index.html
git commit -m "chore: Update backend URL for deployment"
git push origin main
```

---

## **Environment Variables (if needed)**

For Railway or Render, add these in dashboard:
```
PYTHONUNBUFFERED=1
PORT=8000
```

---

## **Quick Test Commands**

After deployment:

```bash
# Test backend
curl https://your-backend.app/api/jobs?limit=1

# Test frontend
curl https://your-frontend.app | grep "<title>"
```

---

## **File Structure**

```
Job-scrapper/
├── app.py              # FastAPI backend
├── database.py         # SQLite models
├── scraper.py          # Job scraper
├── requirements.txt    # Python deps
├── Dockerfile          # Docker config
├── index.html          # Frontend
├── railway.json        # Railway config
├── netlify.toml        # Netlify config
└── README.md           # Documentation
```

---

## **Troubleshooting**

| Issue | Solution |
|-------|----------|
| Backend not starting | Check `requirements.txt` - run `pip install -r requirements.txt` locally |
| Frontend blank | Update API_BASE URL in `index.html` |
| Jobs not showing | Check backend logs for database errors |
| Build fails | Ensure `Dockerfile` and `requirements.txt` are in root |

---

## **Live URLs (After Deployment)**

- **Backend:** `https://your-railway-app.railway.app/docs` (API docs)
- **Frontend:** `https://your-netlify-site.netlify.app`

---

**Need Help?** Check logs in platform dashboard → "Deployments" → View logs

