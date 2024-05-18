from datetime import datetime, timezone, timedelta

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from env import ENV

ALGORITHM = ENV['ALGORITHM']
SECRET_KEY = ENV['SECRET_KEY']
ACCESS_TOKEN_EXPIRE_MINUTES = int(ENV['ACCESS_TOKEN_EXPIRE_MINUTES'])
REFRESH_TOKEN_EXPIRE_MINUTES = int(ENV['REFRESH_TOKEN_EXPIRE_MINUTES'])

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/login")

def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> int:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: int = REFRESH_TOKEN_EXPIRE_MINUTES) -> int:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt_without_exp_verification(token: str):
    try:
        # exp 검사를 비활성화하는 옵션 설정
        options = {"verify_exp": False}
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options=options)
        user_id = payload.get('sub')
        return user_id
    except JWTError as e:
        print(f"Decoding error: {e}")
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options = {"verify_exp": True})
        user_id = payload.get("sub")
    except JWTError as e:
        print(f"Decoding error: {e}")
        raise credentials_exception
    if user_id is None:
        raise credentials_exception
    return int(user_id)


def reissuance_access_token(access_token: str, refresh_token: str, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    
    exp_access_token_user_id = decode_jwt_without_exp_verification(access_token)
    
    try:
        refresh_token_data = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = refresh_token_data.get("sub")
        if exp_access_token_user_id != user_id:
            raise HTTPException(401, {'detail' : 'distorted token'})
    except JWTError as e:
        print(f"Decoding error: {e}")
        raise credentials_exception
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    acc_token_data = {'sub': user_id, 'exp' : expire}
    
    encoded_jwt = jwt.encode(acc_token_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt