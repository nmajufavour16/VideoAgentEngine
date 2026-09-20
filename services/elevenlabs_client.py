import os
import asyncio
from elevenlabs.client import AsyncElevenLabs
from elevenlabs import save
from config.settings import settings

class ElevenLabsClient:
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        if self.api_key:
            self.client = AsyncElevenLabs(api_key=self.api_key)
        else:
            self.client = None

    async def generate_audio(self, text: str, voice_id: str, output_path: str, dry_run: bool = False) -> float:
        """
        Generates audio using ElevenLabs and saves it to output_path.
        Returns the duration of the audio in seconds.
        """
        if dry_run or not self.client:
            print(f"[ElevenLabs Mock] Would generate audio for voice '{voice_id}': {text}")
            # Mock duration: assuming roughly 150 words per minute (2.5 words per second)
            word_count = len(text.split())
            mock_duration = max(1.0, word_count / 2.5)
            # Create an empty file to satisfy path requirements
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w") as f:
                f.write("mock audio data")
            return mock_duration

        print(f"[ElevenLabs] Generating audio for voice '{voice_id}'...")
        try:
            # We use the default model 'eleven_multilingual_v2' as it is natural
            audio_generator = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_multilingual_v2"
            )
            
            # Since generate returns an async generator, we need to consume it
            audio_bytes = b""
            async for chunk in audio_generator:
                audio_bytes += chunk
                
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(audio_bytes)
                
            # For accurate duration, we'd ideally parse the audio file.
            # Using a rough approximation here, but production would use librosa or mutagen
            word_count = len(text.split())
            duration = max(1.0, word_count / 2.5) # Approximate fallback
            
            return duration
        except Exception as e:
            print(f"Error generating audio: {e}")
            return None

elevenlabs_client = ElevenLabsClient()
