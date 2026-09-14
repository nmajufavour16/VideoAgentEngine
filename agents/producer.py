import os
import json
import subprocess
import asyncio
from schemas.video_schema import VideoPayload
from services.elevenlabs_client import elevenlabs_client
from config.settings import settings
from config.constants import VOICE_IDS

class ProducerAgent:
    async def produce_video(self, payload: VideoPayload, dry_run: bool = False):
        """
        Orchestrates audio generation, asset synchronization, and Remotion CLI rendering.
        """
        print(f"[Producer] Producing video: {payload.title}")
        
        # 1. Generate audio and calculate timings
        if payload.scenes:
            for scene in payload.scenes:
                if scene.speaker != "None" and scene.spoken_text:
                    voice_id = scene.voice_id or VOICE_IDS.get(scene.speaker, VOICE_IDS["Lead"])
                    audio_filename = f"audio_scene_{scene.scene_id}.mp3"
                    audio_path = os.path.join(settings.REMOTION_DIR, "public", "assets", audio_filename)
                    
                    print(f"  -> Generating audio for Scene {scene.scene_id} ({scene.speaker})")
                    duration_sec = await elevenlabs_client.generate_audio(
                        text=scene.spoken_text,
                        voice_id=voice_id,
                        output_path=audio_path,
                        dry_run=dry_run
                    )
                    
                    scene.audio_file_path = f"/assets/{audio_filename}"
                    scene.duration_frames = int(duration_sec * settings.DEFAULT_FPS)
                else:
                    # Voiceless diagram scenes or no-speaker scenes get a fixed duration
                    scene.duration_frames = scene.duration_frames or (5 * settings.DEFAULT_FPS)
                    
        # 2. Write data.json
        print(f"[Producer] Writing payload to {settings.DATA_JSON_PATH}")
        os.makedirs(os.path.dirname(settings.DATA_JSON_PATH), exist_ok=True)
        with open(settings.DATA_JSON_PATH, "w") as f:
            f.write(payload.model_dump_json(indent=2))
            
        if dry_run:
            print("[Producer] Dry-run complete. Skipping Remotion render.")
            return

        # 3. Trigger Remotion CLI
        print("[Producer] Triggering Remotion render...")
        out_file = f"out/reel_{payload.title.replace(' ', '_')}.mp4"
        cmd = [
            "npx", "remotion", "render", 
            "src/index.ts", "TechReel", out_file,
            "--props=./public/data.json"
        ]
        
        try:
            # We run the command inside the remotion-app directory
            result = subprocess.run(
                cmd, 
                cwd=settings.REMOTION_DIR, 
                capture_output=True, 
                text=True,
                check=True
            )
            print("[Producer] Render success!")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print("[Producer] Render failed:")
            print(e.stderr)

producer_agent = ProducerAgent()
