# 🚀 Pain Miner

**Pain Miner** is a startup idea discovery tool that helps entrepreneurs, indie hackers, and developers uncover real user problems from communities across the internet.

Instead of brainstorming ideas from scratch, Pain Miner finds actual complaints, frustrations, unmet needs, and feature requests posted by users on platforms like Reddit, Hacker News, and Product Hunt.

---

## ✨ Features

* 🔍 Search for pain-point keywords across multiple platforms
* 🧠 Discover startup opportunities from real user frustrations
* 📊 View results in a clean table interface
* 📁 Export findings to CSV for further analysis
* 🎯 Multi-platform search support
* ⚡ Fast scraping powered by FastAPI
* ✅ Input validation and loading feedback
* 🔑 Reddit API credential setup guide

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

### Scraping & Data Sources

* PRAW (Reddit API)
* Algolia Search API (Hacker News)
* Product Hunt GraphQL API
* BeautifulSoup
* HTTPX

---

## 🌐 Supported Platforms

### Reddit

Searches posts and discussions using Reddit's API via PRAW.

**Requires:**

* Reddit Client ID
* Reddit Client Secret

### Hacker News

Searches discussions using the public Algolia Hacker News API.

**Requires:**

* No authentication

### Product Hunt

Searches product discussions and launches through the Product Hunt GraphQL API.

**Requires:**

* Product Hunt API Token

---

## 💡 Example Keywords

Pain Miner works best with phrases that indicate frustration, inefficiency, or unmet needs:

```text
i wish
no tool for
manually doing
frustrated with
hate using
looking for
need a way to
takes too long
```

Example:

```text
i wish
manually doing
no tool for
```

---

## 📋 Results

Each result contains:

| Field           | Description                         |
| --------------- | ----------------------------------- |
| Source          | Platform where the result was found |
| Title           | Post title or discussion title      |
| Score           | Popularity score/upvotes            |
| Matched Keyword | Keyword that triggered the match    |
| Link            | Direct URL to the original content  |

---

## 📁 Project Structure

```bash
pain-miner/
├── backend/
│   ├── scrapers/
│   │   ├── hackernews.py
│   │   ├── reddit.py
│   │   └── producthunt.py
│   ├── main.py
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   └── App.jsx
    ├── package.json
    └── vite.config.js
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/pain-miner.git
cd pain-miner
```

---

### 2. Backend Setup

```bash
cd backend

python -m venv venv

source venv/bin/activate
# Windows:
# venv\Scripts\activate

pip install -r requirements.txt
```

Start the API:

```bash
uvicorn main:app --reload
```

Backend will run on:

```text
http://localhost:8000
```

---

### 3. Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend will run on:

```text
http://localhost:5173
```

---

## 🔑 Reddit API Setup

1. Visit:
   [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
2. Click **Create App**
3. Select **Script**
4. Copy:
   * Client ID
   * Client Secret
5. Enter them in the Pain Miner UI

---

## 📤 CSV Export

After scraping completes, click **Export CSV** to download all collected results for analysis in:

* Excel
* Google Sheets
* Notion
* Airtable

---

## 🚀 Deployment

### Frontend

Deploy on Vercel:

```bash
vercel
```

### Backend

Deploy on Railway:

```bash
railway up
```

---

## 🎯 Use Cases

* Discover startup ideas
* Validate market demand
* Find SaaS opportunities
* Research customer pain points
* Generate product ideas
* Analyze community frustrations
* Build problem-first businesses

---

## 🔮 Future Improvements

* AI-powered pain point clustering
* Sentiment analysis
* Automatic startup idea generation
* Trend detection
* Save searches
* User authentication
* Database storage
* Email alerts
* Additional data sources (X, GitHub Issues, Indie Hackers)

---

## 📄 License

MIT License

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

Feel free to fork the project and submit a pull request.

---

## ⭐ Support

If you find this project useful, consider giving it a star on GitHub.

It helps others discover the project and motivates future development.
