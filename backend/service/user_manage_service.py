from passlib.context import CryptContext

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from auth import create_access_token, create_refresh_token, get_current_user
from util import session_injection, gen_random_nickname, r
from repository import user_repo
from DTO import ResponseNicknameDTO, ResponseTokenDTO, RequestTokenDTO

class UserManageService:
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"])
        
        self.user_repo = user_repo
    
    
    async def create_user(self, user_data : OAuth2PasswordRequestForm) -> ResponseNicknameDTO:
        db = await session_injection()
        
        user = await self.user_repo.get_user_by_login_id(db, user_data.username)
        
        if user:
            raise HTTPException(409, "duplicate user id")
        
        user_data.password = self.pwd_context.hash(user_data.password)
        
        nickname = gen_random_nickname()
        
        is_created = await self.user_repo.create_user(db, user_data, nickname)
        
        if not is_created:
            raise HTTPException(400, "Failed create user")
        
        return ResponseNicknameDTO(nickname=nickname)
    
    
    async def login(self, user_data : OAuth2PasswordRequestForm) -> ResponseTokenDTO:
        db = await session_injection()
        
        login_id, password = user_data.username, user_data.password
        user = await self.user_repo.get_user_by_login_id(db, login_id)
        
        if not user or self.pwd_context.verify(password, user.password) == False:
            raise HTTPException(404, "User Not Found")
        
        access_token = create_access_token({"sub": str(user.user_id), "role": str(user.role_id)})
        refresh_token = create_refresh_token({"sub": str(user.user_id), "role": str(user.role_id)})
        
        token_response = ResponseTokenDTO(user_name=user.nickname,
                                          access_token=access_token,
                                          refresh_token=refresh_token)
        
        return token_response
    
    
    async def token_refresh(self, tokens : RequestTokenDTO, user):
        
        user_id, role_id = user
        
        access_token = create_access_token({"sub": str(user_id), "role": str(role_id)})
        refresh_token = create_refresh_token({"sub": str(user_id), "role": str(role_id)})
        
        token_response = ResponseTokenDTO(access_token=access_token,
                                          refresh_token=refresh_token)
        
        if not await r.add_blacklist(tokens):
            raise HTTPException(500, "Redis Error")
        
        return token_response
    
    
    async def logout(self, tokens : RequestTokenDTO):

        if not await r.add_blacklist(tokens):
            raise HTTPException(500, "Redis Error")