from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from DTO.user import CreateUserDataDTO
from DTO.auth import TokenData, Token
from model.user import User
from auth.auth import create_access_token

from env import ENV
GOOGLE_CLIENT_ID = ENV['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = ENV['GOOGLE_CLIENT_SECRET']
GOOGLE_REDIRECT_URI = ENV['GOOGLE_REDIRECT_URI']

ACCESS_TOKEN_EXPIRE_MINUTES = int(ENV['ACCESS_TOKEN_EXPIRE_MINUTES'])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = 'auto')


def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_pw, hashed_pw):
    return pwd_context.verify(plain_pw, hashed_pw)

def create_user(user_data : CreateUserDataDTO, db : Session):
    
    nickname = user_data.nickname
    login_id = user_data.login_id
    password = user_data.password

    if db.query(User).filter(User.nickname == nickname).exists():
        raise HTTPException(409, '중복된 닉네임')

    elif db.query(User).filter(User.login_id == login_id).exists():
        raise HTTPException(409, '중복된 아이디')
    
    new_user = User(
        nickname = nickname,
        login_id = login_id,
        password = get_password_hash(password)
    )
    
    db.add(new_user)
    db.commit()

    return new_user.user_id


def login_user(login_user_data : OAuth2PasswordRequestForm , db: Session):
    
    login_id = login_user_data.username
    plain_pw = login_user_data.password
    
    user = db.query(User).filter(User.login_id == login_id).first()
    
    hashed_pw = user.password
    
    if not user:
        raise HTTPException(401, '찾을 수 없는 아이디')
    
    if verify_password(plain_pw, hashed_pw) == False:
        raise HTTPException(401, '비밀번호 불일치')
    
    user_id = user.user_id
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user_id)}, expires_delta=access_token_expires
    )
    return {'user_id' : user_id,
            'token' : Token(access_token=access_token, token_type="bearer")}










# def google_login(form_data : OAuth2PasswordRequestForm, db : Session):
    
#     login_id = form_data.username
#     plain_pw = form_data.password
    
#     user = db.query(User).filter(User.login_id == login_id).first()
    
#     hashed_pw = user.password
    
#     if not user:
#         raise HTTPException(401, '찾을 수 없는 아이디')
    
#     if verify_password(plain_pw, hashed_pw) == False:
#         raise HTTPException(401, '비밀번호 불일치')
    
#     return user.user_id


# def get_google_login_url():
#     return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"