import httpx
from datetime import datetime

DEVTO_API_URL = "https://dev.to/api/articles"

async def scrape_devto(keywords: list[str], limit: int = 50) -> list[dict]:
    results = []

    async with httpx.AsyncClient(timeout=10) as client:
        for keyword in keywords:
            # Dev.to supports tag search and title search
            params = {
                "per_page": limit,
                "tag": keyword.replace(" ", "")
            }

            response = await client.get(
                DEVTO_API_URL,
                params=params,
                headers={"User-Agent": "pain-miner/1.0"}
            )

            if response.status_code != 200:
                continue

            articles = response.json()

            for article in articles:
                results.append({
                    "source": "devto",
                    "title": article.get("title", ""),
                    "body": article.get("description", "")[:500],
                    "url": article.get("url", ""),
                    "score": article.get("positive_reactions_count", 0),
                    "author": article.get("user", {}).get("name", ""),
                    "scraped_at": datetime.utcnow().isoformat(),
                    "keyword_matched": keyword
                })

    return results