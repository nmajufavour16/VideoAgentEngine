import random
from config.constants import TOPIC_SEEDS

class ScraperService:
    def __init__(self):
        pass

    def get_trending_topics(self, count: int = 3) -> list[str]:
        """
        Simulates scraping by returning random broad tech topics.
        In a real scenario, this could hit Hacker News API, Dev.to, or GitHub Trending.
        """
        # Ensure we don't sample more than available
        sample_count = min(count, len(TOPIC_SEEDS))
        return random.sample(TOPIC_SEEDS, sample_count)

scraper_service = ScraperService()
