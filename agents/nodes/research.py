# agents/nodes/research.py
from core.providers import get_provider

async def research_node(state: dict) -> dict:
    provider = get_provider()
    research = await provider.complete(
        prompt=f'Research and summarize key facts about: {state["task"]}',
        system='You are a research assistant. Be factual and concise.'
    )
    return {**state, 'research_output': research}
 