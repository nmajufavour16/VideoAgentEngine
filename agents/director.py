from google import genai
from google.genai import types
from schemas.topic_schema import Topic
from schemas.video_schema import VideoPayload
from config.settings import settings
import json

class DirectorAgent:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def direct_video(self, topic: Topic, dry_run: bool = False) -> VideoPayload:
        """
        Takes a researched topic and authors a structured VideoPayload using the LLM.
        """
        print(f"[Director] Directing video for topic: {topic.title} using format {topic.recommended_format}")
        
        if dry_run or not self.client:
            print("[Director] Dry-run enabled or no API key, returning dummy VideoPayload.")
            return self._get_dummy_payload(topic)

        prompt = f"""
        You are an expert technical Video Director. 
        Create a detailed VideoPayload for a short-form tech video.
        
        Topic Title: {topic.title}
        Hook: {topic.hook}
        Mechanism: {topic.mechanism}
        Metaphor: {topic.metaphor}
        Requested Format: {topic.recommended_format}
        
        Follow the provided JSON schema strictly. Be creative with the design system and scene UIs.
        Ensure you populate scenes, entities, and timeline steps appropriately for the format.
        
        CRITICAL VISUAL INSTRUCTIONS:
        - Do not just use 'title_hook'. Actively use rich layouts like 'table_view', 'icon_grid', and 'bullet_list' where appropriate (e.g. comparing things -> table, listing features -> bullet points, architecture -> icon grid).
        - For 'icon_grid' and other scenes, use valid lucide-react icon names in the 'icon_list' (e.g., 'Database', 'Server', 'Shield', 'Cloud', 'Zap').
        - For 'table_view', populate 'table_headers' (list of strings) and 'table_rows' (list of list of strings).
        - Keep animations (timeline steps) logical and visually appealing.
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
                        response_schema=VideoPayload,
                    ),
                )
                
                payload_data = json.loads(response.text)
                return VideoPayload(**payload_data)
            except Exception as e:
                print(f"[Director] Error during API call (Attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    sleep_time = base_delay ** (attempt + 1)
                    print(f"[Director] Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)

        return self._get_dummy_payload(topic)

    def _get_dummy_payload(self, topic: Topic) -> VideoPayload:
        return VideoPayload(
            title=topic.title,
            topic_badge="Tech Basics",
            format=topic.recommended_format, # type: ignore
            design_system={
                "mode": "dark",
                "background": "#121212",
                "text_primary": "#FFFFFF",
                "accent_color": "#BB86FC",
                "font_family": "Inter, sans-serif"
            },
            scenes=[
                {
                    "scene_id": 1,
                    "layout_type": "title_hook",
                    "speaker": "Lead",
                    "voice_id": "nPczCjzI2devNBz1zQrb",
                    "spoken_text": topic.hook,
                    "display_text": topic.title,
                    "ui_elements": {
                        "headline": None,
                        "sub_badge": None,
                        "diagram_type": None,
                        "left_node": None,
                        "right_node": None,
                        "action_type": None,
                        "highlight_words": [],
                        "table_headers": None,
                        "table_rows": None,
                        "icon_list": None,
                        "bullet_points": None
                    },
                    "duration_frames": 150,
                    "audio_file_path": None
                }
            ],
            entities=[],
            timeline=[]
        )

director_agent = DirectorAgent()
