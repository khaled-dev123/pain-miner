import httpx
from datetime import datetime
import xml.etree.ElementTree as ET

ARXIV_API_URL = "http://export.arxiv.org/api/query"

async def scrape_arxiv(keywords: list[str], limit: int = 50) -> list[dict]:
    results = []

    async with httpx.AsyncClient(timeout=15) as client:
        for keyword in keywords:
            params = {
                "search_query": f"all:{keyword}",
                "start": 0,
                "max_results": limit,
                "sortBy": "relevance",
                "sortOrder": "descending"
            }

            response = await client.get(ARXIV_API_URL, params=params)

            if response.status_code != 200:
                continue

            root = ET.fromstring(response.text)
            namespace = {"atom": "http://www.w3.org/2005/Atom"}

            for entry in root.findall("atom:entry", namespace):
                title = entry.find("atom:title", namespace)
                summary = entry.find("atom:summary", namespace)
                url = entry.find("atom:id", namespace)
                authors = entry.findall("atom:author", namespace)

                first_author = ""
                if authors:
                    name = authors[0].find("atom:name", namespace)
                    first_author = name.text if name is not None else ""

                results.append({
                    "source": "arxiv",
                    "title": title.text.strip() if title is not None else "",
                    "body": summary.text.strip()[:500] if summary is not None else "",
                    "url": url.text.strip() if url is not None else "",
                    "score": 0,
                    "author": first_author,
                    "scraped_at": datetime.utcnow().isoformat(),
                    "keyword_matched": keyword
                })

    return results