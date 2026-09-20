# Default voices mapped to their ElevenLabs voice IDs.
# Using 'Brian' or similar natural defaults. You can update these with actual ElevenLabs IDs.
VOICE_IDS = {
    "Lead": "nPczCjzI2devNBz1zQrb",     # Example ElevenLabs ID (Brian)
    "Expert": "nPczCjzI2devNBz1zQrb",   # Valid fallback
    "Narrator": "nPczCjzI2devNBz1zQrb"  # Valid fallback
}

# The broad topics we want the researcher to select from
TOPIC_SEEDS = [
    "What actually happens when you type a URL into your browser? (DNS, TCP, HTTP, DOM).",
    "Client-Side vs. Server-Side Rendering. (Why frameworks like Next.js exist).",
    "State Management explained simply. (Props drilling vs. Global State).",
    "REST vs. GraphQL: Which should you use?",
    "How OAuth 2.0 actually works. (The 'Sign in with Google' magic).",
    "What is an API Gateway? (The bouncer of the internet).",
    "The true cost of Technical Debt.",
    "Why you should build an MVP (Minimum Viable Product) before writing complex code.",
    "Compiled vs. Interpreted Languages. (C++ vs. Python/JavaScript)."
]
