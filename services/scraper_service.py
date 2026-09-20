import urllib.request
import json
import random
from config.constants import TOPIC_SEEDS

class ScraperService:
    def __init__(self):
        pass

    def get_trending_topics(self, count: int = 3) -> list[str]:
        """
        Scrapes real trending topics from Hacker News API.
        Falls back to hardcoded seeds if the API fails.
        """
        try:
            # Fetch top story IDs
            req = urllib.request.Request(
                'https://hacker-news.firebaseio.com/v0/topstories.json',
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                story_ids = json.loads(response.read().decode())
            
            topics = []
            # Only fetch up to the requested count to avoid rate limiting or slow execution
            for story_id in story_ids[:count * 2]: # Fetch a bit more in case some are empty/bad
                if len(topics) >= count:
                    break
                
                story_req = urllib.request.Request(
                    f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json',
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                with urllib.request.urlopen(story_req, timeout=5) as story_resp:
                    story = json.loads(story_resp.read().decode())
                    if story and 'title' in story:
                        topics.append(story['title'])
            
            if topics:
                return topics
        except Exception as e:
            print(f"[Scraper] Failed to fetch from Hacker News API: {e}. Falling back to constants.")
            
        # Fallback if network fails
        sample_count = min(count, len(TOPIC_SEEDS))
        return random.sample(TOPIC_SEEDS, sample_count)

scraper_service = ScraperService()
