import praw
from datetime import datetime

SUBREDDITS = [
    "entrepreneur", "smallbusiness", "SaaS",
    "freelance", "automation", "startups"
]

async def scrape_reddit(
    keywords: list[str],
    limit: int,
    client_id: str,
    client_secret: str,
    user_agent: str
) -> list[dict]:

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

    results = []

    for keyword in keywords:
        for subreddit_name in SUBREDDITS:
            subreddit = reddit.subreddit(subreddit_name)
            posts = subreddit.search(keyword, limit=limit)

            for post in posts:
                results.append({
                    "source": "reddit",
                    "title": post.title,
                    "body": post.selftext[:500] if post.selftext else "",
                    "url": f"https://reddit.com{post.permalink}",
                    "score": post.score,
                    "author": str(post.author),
                    "scraped_at": datetime.utcnow().isoformat(),
                    "keyword_matched": keyword
                })

    return results