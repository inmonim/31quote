from fastapi import HTTPException
from sqlalchemy.orm import Session
import bcrypt

from DTO.user import CreateUserDataDTO, LoginDataDTO
from model.user import User


def create_user(user_data : CreateUserDataDTO, db : Session):
    
    nickname = user_data.nickname
    login_id = user_data.login_id
    password = user_data.password
    
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)

    if db.query(User).filter(User.nickname == nickname).count():
        raise HTTPException(409, '중복된 닉네임')

    elif db.query(User).filter(User.login_id == login_id).count():
        raise HTTPException(409, '중복된 아이디')
    
    new_user = User(
        nickname = nickname,
        login_id = login_id,
        password = hashed_pw
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
    
    if bcrypt.checkpw(plain_pw.encode('utf-8'), hashed_pw.encode('utf-8')) == False:
        raise HTTPException(401, '비밀번호 불일치')
    
    return user.user_id