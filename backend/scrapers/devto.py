import httpx
import re
from datetime import datetime

DEVTO_API_URL = "https://dev.to/api/articles"

async def scrape_devto(keywords: list[str], limit: int = 50) -> list[dict]:
    results = []

    async with httpx.AsyncClient(timeout=15) as client:
        all_articles = []
        for page in range(1, 6):  # fetch ~500 articles for better coverage
            response = await client.get(
                DEVTO_API_URL,
                params={"per_page": 100, "page": page},
                headers={"User-Agent": "pain-miner/1.0"}
            )
            if response.status_code != 200:
                break
            batch = response.json()
            if not batch:
                break
            all_articles.extend(batch)

        for keyword in keywords:
            pattern = re.compile(r'\b' + re.escape(keyword.lower()) + r'\b')
            count = 0
            for article in all_articles:
                if count >= limit:
                    break
                title = article.get("title", "")
                description = article.get("description", "") or ""
                combined = f"{title} {description}".lower()

                if pattern.search(combined):
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
                    count += 1

    return results