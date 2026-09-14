# Video Agent Engine

A fully autonomous, production-ready Multi-Agent Video Generation Pipeline. This system autonomously researches tech topics, authors structured video scenes (JSON payloads), generates word-level synced voiceovers via the ElevenLabs API, and renders high-density motion graphics using Remotion (React/TypeScript).

## System Architecture

The pipeline consists of three core AI agents:

1. **Researcher Agent**: Discovers high-signal tech topics and curates them into a core concept with a hook, mechanism, visual metaphor, and complexity rating.
2. **Director Agent**: Transforms the researched topic into a strictly validated Remotion scene schema (JSON). It intelligently selects the best format: `single_voice`, `dual_voice`, or `voiceless_diagram`.
3. **Producer Agent**: Synthesizes audio using ElevenLabs, synchronizes timestamps, outputs the final payload to `data.json`, and triggers the Remotion renderer to compile the final `.mp4`.

## Project Structure

```text
VideoAgentEngine/
+-- agents/             # Agent logic (Researcher, Director, Producer)
+-- config/             # Settings and constants
+-- schemas/            # Pydantic models enforcing strict JSON outputs
+-- services/           # External API clients (ElevenLabs, Scraper)
+-- remotion-app/       # React/Tailwind motion graphics engine
+-- orchestrator.py     # Main CLI entrypoint
+-- requirements.txt    # Python dependencies
+-- .env.example        # Environment variable template
```

## Prerequisites

- **Python 3.11/3.12+**
- **Node.js** (v18+)
- **API Keys**: Google Gemini API key and ElevenLabs API key.

## Installation

1. **Set up the Python Environment:**
   ```bash
   # Create and activate a virtual environment
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Set up the Remotion Application:**
   ```bash
   cd remotion-app
   npm install
   ```

3. **Configure API Keys:**
   - Copy `.env.example` to `.env` in the root directory.
   - Add your `GEMINI_API_KEY` and `ELEVENLABS_API_KEY`.

## Usage

The system provides a CLI (`orchestrator.py`) with multiple modes:

### Full Autonomous Run
Let the Researcher pick a trending topic, run it through the Director and Producer, and generate the final MP4 video.
```bash
python orchestrator.py --auto
```

### Specific Topic Run
Skip the Researcher and pass a direct topic to the Director.
```bash
python orchestrator.py --topic "How OAuth 2.0 Works"
```

### Dry-Run Mode (Free / Testing)
Generates the structured JSON payload without making paid ElevenLabs API calls or executing the heavy Remotion CPU render. 
```bash
python orchestrator.py --auto --dry-run
```

## Previewing Generated Videos

If you run the pipeline in `--dry-run` mode, you can still preview the generated scene layout visually by starting the Remotion Studio.

1. Ensure the Python pipeline has written the `data.json` file to `remotion-app/public/data.json`.
2. Open a terminal in the `remotion-app` directory.
3. Start the studio preview:
   ```bash
   npm start
   ```
4. This will open a browser window at `http://localhost:3000` where you can play, scrub, and inspect the video timeline before committing to a full render.
