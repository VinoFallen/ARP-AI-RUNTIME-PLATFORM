# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from core.logging import setup_logging
from api.v1 import agents, rag, admin
 
setup_logging()
 
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title='AI Runtime Platform', version='1.0.0')
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(CORSMiddleware, allow_origins=['*'],
                   allow_methods=['*'], allow_headers=['*'])
 
app.include_router(agents.router, prefix='/v1/agents', tags=['agents'])
#app.include_router(rag.router,    prefix='/v1/rag',    tags=['rag'])
#app.include_router(admin.router,  prefix='/v1/admin',  tags=['admin'])
 
@app.get('/health')
async def health(): return {'status': 'ok', 'version': '1.0.0'}
 
@app.get('/ready')
async def ready(): return {'status': 'ready'}
