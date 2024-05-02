from fastapi import HTTPException
from sqlalchemy.orm import Session
import bcrypt

from DTO.user import CreateUserDataDTO
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