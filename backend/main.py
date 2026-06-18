from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from scrapers.devto import scrape_devto
from scrapers.arxiv import scrape_arxiv
from scrapers.hackernews import scrape_hn
from scrapers.reddit import scrape_reddit
from scrapers.producthunt import scrape_producthunt

app = FastAPI(title="Pain Miner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScrapeRequest(BaseModel):
    keywords: list[str]
    platforms: list[str]
    reddit_client_id: Optional[str] = None
    reddit_client_secret: Optional[str] = None
    reddit_user_agent: Optional[str] = "pain-miner/1.0"
    producthunt_api_key: Optional[str] = None
    limit: Optional[int] = 50

@app.post("/scrape")
async def scrape(req: ScrapeRequest):
    results = []
    errors = {}

    if "hn" in req.platforms:
        try:
            data = await scrape_hn(req.keywords, req.limit)
            results.extend(data)
        except Exception as e:
            errors["hn"] = str(e)

    if "reddit" in req.platforms:
        if not req.reddit_client_id or not req.reddit_client_secret:
            errors["reddit"] = "Missing Reddit credentials"
        else:
            try:
                data = await scrape_reddit(
                    req.keywords, req.limit,
                    req.reddit_client_id,
                    req.reddit_client_secret,
                    req.reddit_user_agent
                )
                results.extend(data)
            except Exception as e:
                errors["reddit"] = str(e)

    if "producthunt" in req.platforms:
        try:
            data = await scrape_producthunt(req.keywords, req.limit, req.producthunt_api_key)
            results.extend(data)
        except Exception as e:
            errors["producthunt"] = str(e)

    if "devto" in req.platforms:
        try:
           data = await scrape_devto(req.keywords, req.limit)
           results.extend(data)
        except Exception as e:
           errors["devto"] = str(e)
    if "arxiv" in req.platforms:
        try:
           data = await scrape_arxiv(req.keywords, req.limit)
           results.extend(data)
        except Exception as e:
           errors["arxiv"] = str(e)

    return {
        "total": len(results),
        "results": results,
        "errors": errors
    }

@app.get("/health")
def health():
    return {"status": "ok"}