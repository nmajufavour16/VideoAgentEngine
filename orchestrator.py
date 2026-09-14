import asyncio
import typer
from services.scraper_service import scraper_service
from agents.researcher import researcher_agent
from agents.director import director_agent
from agents.producer import producer_agent

app = typer.Typer()

@app.command()
def run_pipeline(
    auto: bool = typer.Option(False, "--auto", help="Run full pipeline automatically from trending topics"),
    topic: str = typer.Option(None, "--topic", help="Specific topic to start with (skips scraper)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Generate JSON payload without paid API calls or rendering")
):
    """
    Main CLI entrypoint for the Multi-Agent Video Generation Pipeline.
    """
    print("=== Starting Video Agent Engine ===")
    
    selected_topic_idea = None
    if topic:
        selected_topic_idea = topic
    elif auto:
        trending = scraper_service.get_trending_topics(1)
        if trending:
            selected_topic_idea = trending[0]
            print(f"[*] Scraper found trending topic: {selected_topic_idea}")
    else:
        print("[!] Must provide --auto or --topic. Use --help for options.")
        raise typer.Exit()
        
    if not selected_topic_idea:
        print("[!] No topic selected.")
        raise typer.Exit()

    # Phase 1: Researcher
    print("\n--- Phase 1: Research ---")
    researched_topic = researcher_agent.research_topic(selected_topic_idea, dry_run=dry_run)
    print(f"Researched Topic: {researched_topic.title} (Format: {researched_topic.recommended_format})")
    
    # Phase 2: Director
    print("\n--- Phase 2: Direction ---")
    video_payload = director_agent.direct_video(researched_topic, dry_run=dry_run)
    print(f"Video Payload Generated with {len(video_payload.scenes or [])} scenes.")
    
    # Phase 3: Producer
    print("\n--- Phase 3: Production ---")
    asyncio.run(producer_agent.produce_video(video_payload, dry_run=dry_run))
    
    print("\n=== Pipeline Complete ===")

if __name__ == "__main__":
    app()
