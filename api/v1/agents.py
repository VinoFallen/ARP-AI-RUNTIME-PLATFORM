# Agents Endpoints
# api/v1/agents.py
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from core.auth import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address
import asyncio
from agents.graph import agent_graph
 
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
 
async def token_stream(prompt: str):
    # Stub: replace with real LLM call in Module 2
    words = f'Echo: {prompt}'.split()
    for word in words:
        yield f'data: {word}\n\n'
        await asyncio.sleep(0.05)
    yield 'data: [DONE]\n\n'
 
@router.post('/chat')
@limiter.limit('20/minute')
async def chat(request: Request, prompt: str, user=Depends(get_current_user)):
    async def generate():
        state = {'task': prompt, 'messages': [], 'iteration': 0,
                 'research_output': '', 'final_output': '', 'next_agent': ''}
        result = await agent_graph.ainvoke(state)
        output = result.get('final_output', 'No output generated.')
        for word in output.split():
            yield f'data: {word} \n\n'
        yield 'data: [DONE]\n\n'
    return StreamingResponse(generate(), media_type='text/event-stream')
