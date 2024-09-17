from datetime import timedelta

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from DTO.user import CreateUserDataDTO, UserDataDTO
from DTO.auth import Token
from repository.user_manage import UserRepository
from model.user import User, UserProfile
from auth.auth import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = 'auto')


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_pw, hashed_pw):
    return pwd_context.verify(plain_pw, hashed_pw)


def create_user(user_data : CreateUserDataDTO, db : Session) -> str:
    
    user_repo = UserRepository(db)
    
    nickname = user_data.nickname
    login_id = user_data.login_id
    password = user_data.password

    if user_repo.check_duplicated_nickname(nickname):
        raise HTTPException(409, '중복된 닉네임')

    elif user_repo.check_duplicated_login_id(login_id):
        raise HTTPException(409, '중복된 아이디')
    
    new_profile_obj = UserProfile(
        nickname = nickname,
        login_id = login_id,
        password = get_password_hash(password)
    )
    
    new_user_id = user_repo.create_profile(new_profile_obj)
    
    new_user_obj = User(
        user_id = new_user_id,
        nickname = nickname
    )
    
    user_repo.create_user(new_user_obj)

    return nickname


def login_user(login_user_data : OAuth2PasswordRequestForm, db : Session) -> UserDataDTO:
    
    user_repo = UserRepository(db)
    
    login_id = login_user_data.username
    plain_pw = login_user_data.password
    
    login_valied_data = user_repo.get_login_validation_value(login_id)
    
    user_id = login_valied_data.user_id
    nickname = login_valied_data.nickname
    hashed_pw = login_valied_data.hashed_pwd
    
    if not hashed_pw:
        raise HTTPException(401, '찾을 수 없는 아이디')
    
    if verify_password(plain_pw, hashed_pw) == False:
        raise HTTPException(401, '비밀번호 불일치')
    
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user_id)}, expires_delta=3600
    )
    
    login_result = UserDataDTO(user_id=user_id,
                                nickname=nickname,
                                access_token=access_token,
                                token_type="bearer")
    
    return login_result









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