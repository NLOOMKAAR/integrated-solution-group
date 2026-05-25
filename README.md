# Integrated Solution Group Website

A fully-featured community learning platform with discussion forums, event management, learning materials, and more. Built with Flask and SQLite.

## Features
- 📚 Learning video library with summaries and descriptions
- 💬 Discussion forum for community collaboration  
- 🆘 Community support ticket system
- 📅 Event listings and management
- 📖 Learning materials repository
- 💡 Inspiration generator for creative projects
- 🔍 Exploratory article scraper for trending topics
- 🤖 Smart assistant for recommendations

## Quick Start (Local)

```bash
# 1. Clone or download the repo
cd IntegratedSolutionGroupWebsite

# 2. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py

# 5. Open browser to http://127.0.0.1:5000/
```

## Deploy to Free Cloud (Railway.app - Recommended)

1. **Create GitHub repo:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```
   
2. **Push to GitHub:**
   - Create new repo on github.com
   - Add remote and push

3. **Deploy on Railway.app:**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub"
   - Connect your GitHub account and select the repo
   - Railway auto-deploys! 🚀

**Live URL will be available in ~2 minutes**

## Alternative: Deploy to Render.com

1. Push code to GitHub (same steps as above)
2. Go to [render.com](https://render.com)
3. Click "New +"
4. Select "Web Service"
5. Connect GitHub and select repo
6. Use this config:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
7. Deploy!

## Local Hosting with Docker

```bash
# Build
docker build -t integrated-solution-group .

# Run
docker run -p 5000:5000 integrated-solution-group

# Open http://localhost:5000
```

## Features Explained

### Videos Library
Add learning videos with summaries and detailed descriptions. Organize by topic for easy discovery.

### Forum
Community members can post discussions, ask questions, and share knowledge.

### Support Tickets
Users can create support requests, get help from the community, and track resolution status.

### Events
Advertise webinars, workshops, and meetups relevant to the learning group.

### Materials
Curate tutorials, articles, and resources in a centralized library.

### Inspiration Generator
Get creative project ideas and innovative directions based on topics.

### Article Explorer
Automatically scrapes trending articles from tech news sources (Hacker News).

### Smart Assistant
Ask questions about topics, get summaries, find inspiration, and discover articles.

## Notes
- Database: SQLite (site.db) - no external DB needed
- No API keys required for core features
- All data stored locally (persists in site.db)
- Fully open-source and customizable

## Tech Stack
- Backend: Flask
- Database: SQLite + SQLAlchemy
- Frontend: Bootstrap 5
- Web Scraping: BeautifulSoup