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
        
        import re
        safe_title = re.sub(r'[^a-zA-Z0-9_\-]', '', payload.title.replace(' ', '_'))
        
        # 1. Generate audio and calculate timings
        if payload.scenes:
            for scene in payload.scenes:
                if scene.speaker != "None" and scene.spoken_text:
                    ai_voice = scene.voice_id
                    if ai_voice and len(ai_voice) > 15:
                        voice_id = ai_voice
                    else:
                        voice_id = VOICE_IDS.get(scene.speaker, VOICE_IDS["Lead"])
                        
                    audio_filename = f"{safe_title}_scene_{scene.scene_id}.mp3"
                    audio_path = os.path.join(settings.REMOTION_DIR, "public", "assets", audio_filename)
                    
                    print(f"  -> Generating audio for Scene {scene.scene_id} ({scene.speaker})")
                    duration_sec = await elevenlabs_client.generate_audio(
                        text=scene.spoken_text,
                        voice_id=voice_id,
                        output_path=audio_path,
                        dry_run=dry_run
                    )
                    
                    if duration_sec is not None:
                        scene.audio_file_path = f"assets/{audio_filename}"
                        scene.duration_frames = int(duration_sec * settings.DEFAULT_FPS)
                    else:
                        scene.audio_file_path = None
                        word_count = len(scene.spoken_text.split())
                        scene.duration_frames = int(max(1.0, word_count / 2.5) * settings.DEFAULT_FPS)
                else:
                    # Voiceless diagram scenes or no-speaker scenes get a fixed duration
                    scene.duration_frames = scene.duration_frames or (5 * settings.DEFAULT_FPS)
                    
        # 2. Write data.json and named json
        topic_json_path = os.path.join(settings.REMOTION_DIR, "public", f"{safe_title}.json")
        print(f"[Producer] Writing payload to {settings.DATA_JSON_PATH} and {topic_json_path}")
        os.makedirs(os.path.dirname(settings.DATA_JSON_PATH), exist_ok=True)
        payload_json = payload.model_dump_json(indent=2)
        with open(settings.DATA_JSON_PATH, "w") as f:
            f.write(payload_json)
        with open(topic_json_path, "w") as f:
            f.write(payload_json)
            
        if dry_run:
            print("[Producer] Dry-run complete. Skipping Remotion render.")
            return

        # 3. Trigger Remotion CLI
        print("[Producer] Triggering Remotion render...")
        out_file = f"out/reel_{safe_title}.mp4"
        npx_cmd = "npx.cmd" if os.name == "nt" else "npx"
        cmd = [
            npx_cmd, "remotion", "render", 
            "src/index.ts", "TechReel", out_file,
            f"--props=./public/{safe_title}.json"
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
