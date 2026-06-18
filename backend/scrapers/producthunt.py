import httpx
from datetime import datetime

PH_API_URL = "https://api.producthunt.com/v2/api/graphql"

async def scrape_producthunt(keywords: list[str], limit: int = 50, api_key: str = None) -> list[dict]:
    if not api_key:
        raise Exception("Product Hunt API key is required")

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
                    "Authorization": f"Bearer {api_key}"
                }
            )

            if response.status_code != 200:
                continue

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