# agents/nodes/writer.py
from core.providers import get_provider

async def writer_node(state: dict) -> dict:
    provider = get_provider()
    output = await provider.complete(
        prompt=f'Task: {state["task"]}\nResearch: {state["research_output"]}\nWrite a clear response.',
        system='You are a skilled writer. Use the research provided.'
    )
    return {**state, 'final_output': output}