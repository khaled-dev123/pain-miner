import httpx
from datetime import datetime

ALGOLIA_URL = "https://hn.algolia.com/api/v1/search"

async def scrape_hn(keywords: list[str], limit: int = 50) -> list[dict]:
    results = []

    async with httpx.AsyncClient(timeout=10) as client:
        for keyword in keywords:
            params = {
                "query": keyword,
                "hitsPerPage": limit
            }

            response = await client.get(ALGOLIA_URL, params=params)
            response.raise_for_status()
            data = response.json()

            for hit in data.get("hits", []):
                text = (
                    hit.get("comment_text") or
                    hit.get("story_text") or
                    hit.get("title") or
                    ""
                )

                results.append({
                    "source": "hackernews",
                    "title": hit.get("title", ""),
                    "body": text[:500],
                    "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                    "score": hit.get("points", 0),
                    "author": hit.get("author", ""),
                    "scraped_at": datetime.utcnow().isoformat(),
                    "keyword_matched": keyword
                })

    return results