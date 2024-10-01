from datetime import datetime, timezone, timedelta
import time
import pytz

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from util import r
from config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, SECRET_KEY

_tz = pytz.timezone('Asia/Seoul')

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(_tz) + timedelta(seconds=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(_tz) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(_oauth2_scheme)) -> tuple[int, int]:
    if await r.match_token(token):
        raise _credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        current_now = time.time()
        
        if exp < current_now:
            raise _credentials_exception
        
        user_id = int(payload.get("sub"))
        role_id = payload.get("role")
        if not user_id and not role_id:
            raise _credentials_exception
    except JWTError as e:
        raise _credentials_exception

    return (user_id, role_id)