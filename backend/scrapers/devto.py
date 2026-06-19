import httpx
from datetime import datetime

DEVTO_API_URL = "https://dev.to/api/articles"

async def scrape_devto(keywords: list[str], limit: int = 50) -> list[dict]:
    results = []

    async with httpx.AsyncClient(timeout=15) as client:
        # fetch a large pool of recent articles once
        all_articles = []
        for page in range(1, 4):  # fetch ~300 articles
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

        # now filter by each keyword
        for keyword in keywords:
            kw_lower = keyword.lower()
            count = 0
            for article in all_articles:
                if count >= limit:
                    break
                title = article.get("title", "")
                description = article.get("description", "") or ""

                if kw_lower in title.lower() or kw_lower in description.lower():
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