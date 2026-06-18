import httpx
import os
from datetime import datetime

PH_API_URL = "https://api.producthunt.com/v2/api/graphql"

async def scrape_producthunt(keywords: list[str], limit: int = 50, api_key: str = None) -> list[dict]:
    access_token = api_key or os.getenv("PRODUCTHUNT_ACCESS_TOKEN")
    
    if not access_token:
        raise Exception("Product Hunt access token is required")

    results = []

    async with httpx.AsyncClient(timeout=10) as client:
        for keyword in keywords:
            query = """
            query($query: String!) {
                posts(first: 20, order: VOTES, search: { query: $query }) {
                    edges {
                        node {
                            name
                            tagline
                            description
                            url
                            votesCount
                            createdAt
                        }
                    }
                }
            }
            """

            response = await client.post(
                PH_API_URL,
                json={"query": query, "variables": {"query": keyword}},
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json"
                }
            )

            if response.status_code != 200:
                raise Exception(f"Product Hunt API error: {response.status_code}")

            data = response.json()
            edges = data.get("data", {}).get("posts", {}).get("edges", [])

            for edge in edges:
                node = edge.get("node", {})
                results.append({
                    "source": "producthunt",
                    "title": node.get("name", ""),
                    "body": node.get("description") or node.get("tagline", ""),
                    "url": node.get("url", ""),
                    "score": node.get("votesCount", 0),
                    "author": "",
                    "scraped_at": datetime.utcnow().isoformat(),
                    "keyword_matched": keyword
                })

    return results