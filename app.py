import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///site.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class LearningVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    topic = db.Column(db.String(160), nullable=False)
    summary = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ForumPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SupportTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    issue = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(40), default="Open")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(200), nullable=True)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class LearningMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(400), nullable=True)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ExplorationArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    link = db.Column(db.String(500), nullable=False)
    source = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


def generate_inspiration_ideas(topic_text: str) -> str:
    """Generate creative project ideas for a given topic."""
    ideas = {
        "python": [
            "Build a data analysis dashboard with real-time updates",
            "Create a web scraper for industry trends",
            "Develop a CLI tool for automating daily tasks",
        ],
        "web": [
            "Design a collaborative note-taking app",
            "Build a portfolio showcase with animations",
            "Create an interactive learning platform",
        ],
        "machine learning": [
            "Train a model to predict user behavior patterns",
            "Build a recommendation system for personalized content",
            "Create a chatbot for community support",
        ],
        "databases": [
            "Design a scalable analytics database",
            "Build a real-time event streaming system",
            "Create a distributed caching layer",
        ],
    }

    topic_lower = topic_text.lower()
    default_ideas = [
        f"Build an innovative project around {topic_text}",
        f"Create a tutorial series on {topic_text}",
        f"Start a community discussion on {topic_text}",
    ]

    for key, value in ideas.items():
        if key in topic_lower:
            return f"Creative Ideas for {topic_text}:\n\n" + "\n".join([f"• {idea}" for idea in value])

    return f"Creative Ideas for {topic_text}:\n\n" + "\n".join([f"• {idea}" for idea in default_ideas])


def summarize_topic_content(topic_text: str) -> str:
    """Provide a summary and guidance for a learning topic."""
    summaries = {
        "python": "Python is a versatile programming language used for web development, data science, automation, and more. Start by learning basics like variables, loops, and functions. Then explore libraries like Pandas for data analysis or Django for web development.",
        "web development": "Web development involves building websites and applications using HTML, CSS, and JavaScript. Master frontend frameworks like React or Vue, backend frameworks like Flask or Node.js, and databases like PostgreSQL. Learn responsive design and APIs.",
        "machine learning": "ML enables computers to learn from data without explicit programming. Start with supervised learning (classification, regression), then explore unsupervised learning. Use libraries like scikit-learn, TensorFlow, or PyTorch. Practice with real datasets.",
        "cloud computing": "Cloud platforms like AWS, Azure, and Google Cloud offer scalable infrastructure. Learn containerization with Docker, orchestration with Kubernetes, and serverless computing. Practice deploying applications and managing cloud resources.",
    }

    topic_lower = topic_text.lower()
    default_summary = f"{topic_text} is an important area of study. Start with foundational concepts, practice with projects, engage with the community, and continuously learn new tools and techniques."

    for key, value in summaries.items():
        if key in topic_lower:
            return f"Summary: {topic_text}\n\n{value}"

    return f"Summary: {topic_text}\n\n{default_summary}"


def scrape_exploratory_articles_tool(query_text: str) -> str:
    try:
        url = "https://news.ycombinator.com/"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.select(".athing")[:8]
        if not rows:
            return f"No articles found for {query_text or 'technology'}. Try again later."
        output = [f"Exploratory topics for {query_text or 'technology'}:"]
        for row in rows:
            title_tag = row.select_one("a.storylink")
            if not title_tag:
                continue
            title = title_tag.text.strip()
            href = title_tag["href"].strip()
            output.append(f"- {title} — {href}")
        return "\n".join(output) if output else "No articles found. Please try again."
    except requests.Timeout:
        return "Request timed out. Please try again later."
    except Exception as error:
        return "Unable to scrape exploratory articles. Please try again later."


def generate_inspiration_tool(topic_text: str) -> str:
    """Wrapper for inspiration generation."""
    return generate_inspiration_ideas(topic_text)


def run_agent(prompt_text: str) -> str:
    """Process user prompt and generate response."""
    try:
        if "inspiration" in prompt_text.lower() or "idea" in prompt_text.lower():
            topic = prompt_text.replace("inspiration", "").replace("idea", "").strip()
            return generate_inspiration_ideas(topic or "general learning")
        elif "summarize" in prompt_text.lower() or "summary" in prompt_text.lower():
            topic = prompt_text.replace("summarize", "").replace("summary", "").strip()
            return summarize_topic_content(topic or "learning")
        elif "explore" in prompt_text.lower() or "article" in prompt_text.lower():
            query = prompt_text.replace("explore", "").replace("article", "").strip()
            return scrape_exploratory_articles_tool(query or "technology")
        else:
            return f"Agent processed: {prompt_text}\n\nYou can ask for:\n- Inspiration or ideas\n- Summaries\n- Exploratory articles"
    except Exception as error:
        return f"Agent response: {error}"


def fetch_scrape_results(query: str = "technology"):
    raw = scrape_exploratory_articles_tool(query)
    entries = []
    for line in raw.splitlines()[1:]:
        if line.startswith("- "):
            line = line[2:]
            if " — " in line:
                title, link = line.split(" — ", 1)
            else:
                title = line
                link = ""
            entries.append({"title": title.strip(), "link": link.strip(), "source": "Hacker News"})
    for entry in entries:
        if entry["link"] and not ExplorationArticle.query.filter_by(title=entry["title"]).first():
            db.session.add(ExplorationArticle(title=entry["title"], link=entry["link"], source=entry["source"]))
    db.session.commit()
    return ExplorationArticle.query.order_by(ExplorationArticle.created_at.desc()).limit(12).all()


@app.route("/health")
def health():
    """Health check endpoint for cloud deployments."""
    return {"status": "ok", "message": "Service is running"}, 200


@app.route("/")
def index():
    videos = LearningVideo.query.order_by(LearningVideo.created_at.desc()).limit(4).all()
    posts = ForumPost.query.order_by(ForumPost.created_at.desc()).limit(4).all()
    tickets = SupportTicket.query.order_by(SupportTicket.created_at.desc()).limit(4).all()
    events = Event.query.order_by(Event.created_at.desc()).limit(4).all()
    materials = LearningMaterial.query.order_by(LearningMaterial.created_at.desc()).limit(4).all()
    articles = ExplorationArticle.query.order_by(ExplorationArticle.created_at.desc()).limit(4).all()
    return render_template(
        "index.html",
        videos=videos,
        posts=posts,
        tickets=tickets,
        events=events,
        materials=materials,
        articles=articles,
    )


@app.route("/videos", methods=["GET", "POST"])
def videos():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        topic = request.form.get("topic", "").strip()
        summary = request.form.get("summary", "").strip()
        description = request.form.get("description", "").strip()
        if not title or not topic or not summary:
            flash("Title, topic, and summary are required.", "warning")
        else:
            db.session.add(LearningVideo(title=title, topic=topic, summary=summary, description=description))
            db.session.commit()
            flash("Learning video saved successfully.", "success")
            return redirect(url_for("videos"))
    videos = LearningVideo.query.order_by(LearningVideo.created_at.desc()).all()
    return render_template("videos.html", videos=videos)


@app.route("/forum", methods=["GET", "POST"])
def forum():
    if request.method == "POST":
        author = request.form.get("author", "").strip()
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        if not author or not title or not content:
            flash("Author, title, and content are required.", "warning")
        else:
            db.session.add(ForumPost(author=author, title=title, content=content))
            db.session.commit()
            flash("Forum post created successfully.", "success")
            return redirect(url_for("forum"))
    posts = ForumPost.query.order_by(ForumPost.created_at.desc()).all()
    return render_template("forum.html", posts=posts)


@app.route("/support", methods=["GET", "POST"])
def support():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        issue = request.form.get("issue", "").strip()
        if not name or not issue:
            flash("Name and issue are required.", "warning")
        else:
            db.session.add(SupportTicket(name=name, issue=issue))
            db.session.commit()
            flash("Support ticket submitted.", "success")
            return redirect(url_for("support"))
    tickets = SupportTicket.query.order_by(SupportTicket.created_at.desc()).all()
    return render_template("support.html", tickets=tickets)


@app.route("/events", methods=["GET", "POST"])
def events():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        date = request.form.get("date", "").strip()
        location = request.form.get("location", "").strip()
        details = request.form.get("details", "").strip()
        if not title or not date:
            flash("Event title and date are required.", "warning")
        else:
            db.session.add(Event(title=title, date=date, location=location, details=details))
            db.session.commit()
            flash("Event added successfully.", "success")
            return redirect(url_for("events"))
    events = Event.query.order_by(Event.created_at.desc()).all()
    return render_template("events.html", events=events)


@app.route("/materials", methods=["GET", "POST"])
def materials():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        link = request.form.get("link", "").strip()
        description = request.form.get("description", "").strip()
        if not title or not description:
            flash("Title and description are required.", "warning")
        else:
            db.session.add(LearningMaterial(title=title, link=link, description=description))
            db.session.commit()
            flash("Learning material saved.", "success")
            return redirect(url_for("materials"))
    materials = LearningMaterial.query.order_by(LearningMaterial.created_at.desc()).all()
    return render_template("materials.html", materials=materials)


@app.route("/inspiration", methods=["GET", "POST"])
def inspiration():
    inspiration_text = None
    if request.method == "POST":
        topic = request.form.get("topic", "").strip()
        if topic:
            inspiration_text = generate_inspiration_tool(topic)
        else:
            flash("Tell us the topic to get inspiration.", "warning")
    return render_template("inspiration.html", inspiration_text=inspiration_text)


@app.route("/explore", methods=["GET", "POST"])
def explore():
    query = request.form.get("query", "technology") if request.method == "POST" else "technology"
    articles = fetch_scrape_results(query)
    return render_template("explore.html", articles=articles, query=query)


@app.route("/assistant", methods=["GET", "POST"])
def assistant():
    agent_result = None
    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()
        if prompt:
            agent_result = run_agent(prompt)
        else:
            flash("Enter a prompt for the agent.", "warning")
    return render_template("assistant.html", result=agent_result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug_mode, threaded=True)