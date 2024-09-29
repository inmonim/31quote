from passlib.context import CryptContext

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from auth import create_access_token, create_refresh_token
from util import session_injection, gen_random_nickname
from repository import user_repo
from DTO import TokenResponseDTO

class UserManageService:
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"])
        
        self.user_repo = user_repo
    
    
    async def create_user(self, user_data : OAuth2PasswordRequestForm) -> int:
        db = await session_injection()
        
        user = await self.user_repo.get_user_by_login_id(db, user_data.username)
        
        if user:
            raise HTTPException(409, "duplicate username")
        
        user_data.password = self.pwd_context.hash(user_data.password)
        
        user_id = await self.user_repo.create_user(db, user_data, gen_random_nickname())
        
        return user_id
    
    
    async def login(self, user_data : OAuth2PasswordRequestForm) -> TokenResponseDTO:
        db = await session_injection()
        
        login_id, password = user_data.username, user_data.password
        user = await self.user_repo.get_user_by_login_id(db, login_id)
        
        if not user or self.pwd_context.verify(password, user.password) == False:
            raise HTTPException(404, "User Not Found")
        
        access_token = create_access_token({"sub": str(user.user_id), "role": str(user.role_id)})
        refresh_token = create_refresh_token({"sub": str(user.user_id), "role": str(user.role_id)})
        
        token_response = TokenResponseDTO(user_name=user.nickname,
                                          access_token=access_token,
                                          refresh_token=refresh_token)
        
        return token_response