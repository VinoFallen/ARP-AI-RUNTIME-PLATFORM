# api/v1/auth.py  (add to main.py includes)
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from core.auth import create_access_token
 
router = APIRouter()
 
FAKE_USERS = {'dev': 'password'}  # replace with DB in Module 4
 
@router.post('/token')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    if FAKE_USERS.get(form.username) != form.password:
        raise HTTPException(status_code=400, detail='Incorrect credentials')
    token = create_access_token({'sub': form.username})
    return {'access_token': token, 'token_type': 'bearer'}
