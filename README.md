# 🚀 Pain Miner

**Pain Miner** is a startup idea discovery platform that helps entrepreneurs, indie hackers, and developers uncover real market opportunities by mining user frustrations from online communities.

Instead of guessing what to build, Pain Miner searches platforms like Reddit, Hacker News, arXiv, Dev.to and Product Hunt for complaints, feature requests, inefficiencies, and unmet needs. The collected insights can be analyzed and exported for startup validation and product research.

## 🌐 Live Demo

👉 [https://pain-miner-omega.vercel.app/](https://pain-miner-omega.vercel.app/)

---

## ✨ Features

* 🔍 Search pain-point keywords across multiple platforms
* 🧠 Discover startup ideas from real user frustrations
* 📊 Clean results dashboard
* 📁 CSV export for further analysis
* 🎯 Multi-platform search support (5 platforms)
* ⚡ FastAPI-powered async backend
* 🔑 Reddit API integration
* ✅ Input validation and loading states
* 💡 Keyword suggestions and autocomplete

---

## 🛠 Tech Stack

### Frontend

* React
* Vite
* JavaScript
* CSS

### Backend

* FastAPI
* Python

### Data Sources

* Reddit (PRAW API)
* Hacker News (Algolia API)
* Product Hunt (GraphQL API)
* Dev.to (REST API)
* arXiv (Atom XML API)

### Scraping Tools

* HTTPX
* BeautifulSoup
* PRAW

---

## 🌍 Supported Platforms

| Platform     | Method             | Auth Required |
| ------------ | ------------------ | ------------- |
| Hacker News  | Algolia Search API | ❌ No         |
| Reddit       | PRAW API           | ✅ Yes        |
| Product Hunt | GraphQL API        | ✅ Yes        |
| Dev.to       | REST API           | ❌ No         |
| arXiv        | Atom XML API       | ❌ No         |

---

## 💡 Example Searches

Pain Miner performs best when searching for frustration-oriented phrases:

```text
i wish
no tool for
manually doing
frustrated with
hate using
takes too long
need a way to
looking for
```

---

## 📊 Output

Each result includes:

| Field           | Description                       |
| --------------- | --------------------------------- |
| Source          | Platform where the post was found |
| Title           | Post title                        |
| Score           | Upvotes / popularity score        |
| Matched Keyword | Trigger keyword                   |
| Link            | Original post URL                 |

---

## 📂 Project Structure

```bash
pain-miner/
├── backend/
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── hackernews.py
│   │   ├── reddit.py
│   │   ├── producthunt.py
│   │   ├── devto.py
│   │   └── arxiv.py
│   ├── main.py
│   ├── requirements.txt
│   ├── Procfile
│   └── railway.toml
│
└── frontend/
    ├── src/
    │   └── App.jsx
    ├── index.html
    ├── package.json
    └── vite.config.js
```

---

## ⚙️ Local Development

### Clone Repository

```bash
git clone https://github.com/khaled-dev123/pain-miner.git
cd pain-miner
```

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
# Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs on `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

---

## 🔑 Reddit API Setup

1. Visit [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
2. Click **Create App** → select **Script**
3. Set redirect URI to `http://localhost:8080`
4. Copy **Client ID** and **Client Secret**
5. Paste them into Pain Miner dashboard

---

## 📤 Export Results

All search results can be exported as CSV and imported into:

* Excel / Google Sheets
* Airtable / Notion
* Data analysis pipelines

---

## 🚀 Deployment

| Service  | Platform | URL                                          |
| -------- | -------- | -------------------------------------------- |
| Frontend | Vercel   | https://pain-miner-omega.vercel.app          |
| Backend  | Railway  | https://pain-miner-production.up.railway.app |

---

## 🎯 Use Cases

* Startup idea generation
* SaaS opportunity discovery
* Market research
* Customer pain-point analysis
* Product validation
* Feature request mining
* Academic research gap discovery (via arXiv)
* Trend spotting

---

## 🔮 Future Roadmap

* AI-powered pain point clustering
* Classification model to filter noise
* Automatic startup idea generation
* Sentiment analysis
* Trend detection
* User accounts and search history
* Email alerts
* GitHub Issues support
* Indie Hackers integration
* Medium integration

---

## 🤝 Contributing

Contributions, issues, and pull requests are welcome. Feel free to fork the project and improve it.

---

## 📄 License

MIT License

---

## ⭐ Support

If you find this project useful, consider starring the repository.

**Building great startups starts with finding real problems.**
