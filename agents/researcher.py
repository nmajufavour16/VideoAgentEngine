from google import genai
from google.genai import types
from schemas.topic_schema import Topic
from config.settings import settings
import json

class ResearcherAgent:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def research_topic(self, topic_idea: str, dry_run: bool = False) -> Topic:
        print(f"[Researcher] Researching topic: {topic_idea}")
        
        if dry_run or not self.client:
            print("[Researcher] Dry-run enabled or no API key, returning dummy topic.")
            return Topic(
                title=topic_idea,
                hook=f"Did you know the secret behind {topic_idea}?",
                mechanism="It uses a magical process to resolve things quickly.",
                metaphor="Think of it like a post office for the internet.",
                complexity=5,
                recommended_format="single_voice"
            )

        prompt = f"""
        You are a Staff Software Architect researching topics for a tech video.
        Take the following topic idea and expand it into a structured video topic format.
        Provide a catchy hook, a brief mechanism explanation, a visual metaphor, 
        a complexity rating (1-10), and a recommended format (single_voice, dual_voice, or voiceless_diagram).
        
        Topic Idea: {topic_idea}
        """

        import time
        max_retries = 3
        base_delay = 3
        
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=Topic,
                    ),
                )
                
                # The response.text should be a JSON string that we can parse into our Pydantic model
                topic_data = json.loads(response.text)
                return Topic(**topic_data)
            except Exception as e:
                print(f"[Researcher] Error during API call (Attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    sleep_time = base_delay ** (attempt + 1)
                    print(f"[Researcher] Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                
        # Fallback if all retries fail
        return Topic(
            title=topic_idea,
            hook="Fallback hook",
            mechanism="Fallback mechanism",
            metaphor="Fallback metaphor",
            complexity=5,
            recommended_format="single_voice"
        )

researcher_agent = ResearcherAgent()
