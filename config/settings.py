import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    
    # Defaults
    DEFAULT_FPS = 30
    DEFAULT_FORMAT = "single_voice"
    REMOTION_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "remotion-app")
    DATA_JSON_PATH = os.path.join(REMOTION_DIR, "public", "data.json")

settings = Settings()
