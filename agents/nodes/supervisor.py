# agents/nodes/supervisor.py
from core.providers import get_provider
 
async def supervisor_node(state: dict) -> dict:
    provider = get_provider()
    decision = await provider.complete(
        prompt=f"""You are a supervisor. The user's task is: {state['task']}
Decide which agent should handle this. Reply with exactly one word:
RESEARCH (if information gathering is needed),
WRITE (if we have enough info and need a response),
or DONE (if the task is complete).
Current research: {state.get('research_output', 'none yet')}""",
    )
    decision = decision.strip().upper()
    next_map = {'RESEARCH': 'research', 'WRITE': 'writer', 'DONE': END}
    return {**state, 'next_agent': next_map.get(decision, END),
            'iteration': state.get('iteration', 0) + 1}
 