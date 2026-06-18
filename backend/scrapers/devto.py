import httpx
from datetime import datetime

DEVTO_API_URL = "https://dev.to/api/articles"

async def scrape_devto(keywords: list[str], limit: int = 50) -> list[dict]:
    results = []

    async with httpx.AsyncClient(timeout=10) as client:
        for keyword in keywords:
            params = {
                "per_page": limit,
                "top": 1
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
                title = article.get("title", "")
                description = article.get("description", "")

                # filter by keyword manually
                if keyword.lower() not in title.lower() and keyword.lower() not in description.lower():
                    continue

                results.append({
                    "source": "devto",
                    "title": title,
                    "body": description[:500],
                    "url": article.get("url", ""),
                    "score": article.get("positive_reactions_count", 0),
                    "author": article.get("user", {}).get("name", ""),
                    "scraped_at": datetime.utcnow().isoformat(),
                    "keyword_matched": keyword
                })

    return results