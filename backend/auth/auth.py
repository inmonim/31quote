from datetime import datetime, timezone, timedelta

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from env import ENV

ALGORITHM = ENV['ALGORITHM']
SECRET_KEY = ENV['SECRET_KEY']
ACCESS_TOKEN_EXPIRE_MINUTES = int(ENV['ACCESS_TOKEN_EXPIRE_MINUTES'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> int:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception
    if user_id is None:
        raise credentials_exception

    return user_id
