from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from DTO.user import CreateUserDataDTO, LoginDataDTO
from model.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = 'auto')

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_pw, hashed_pw):
    return pwd_context.verify(plain_pw, hashed_pw)

def create_user(user_data : CreateUserDataDTO, db : Session):
    
    nickname = user_data.nickname
    login_id = user_data.login_id
    password = user_data.password

    if db.query(User).filter(User.nickname == nickname).count():
        raise HTTPException(409, '중복된 닉네임')

    elif db.query(User).filter(User.login_id == login_id).count():
        raise HTTPException(409, '중복된 아이디')
    
    new_user = User(
        nickname = nickname,
        login_id = login_id,
        password = get_password_hash(password)
    )
    
    db.add(new_user)
    db.commit()

    return new_user.user_id

def login_user(login_user_data : LoginDataDTO, db: Session):
    
    login_id = login_user_data.login_id
    plain_pw = login_user_data.password
    
    user = db.query(User).filter(User.login_id == login_id).first()
    
    if not user:
        raise HTTPException(401, '찾을 수 없는 아이디')
    
    hashed_pw = user.password
    
    if verify_password(plain_pw, hashed_pw) == False:
        raise HTTPException(401, '비밀번호 불일치')
    
    return user.user_id