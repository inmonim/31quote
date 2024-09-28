from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordRequestForm

from repository import user_repo


class UserManageService:
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"])
        
        self.user_repo = user_repo
    
    async def create_user(self, user_data : OAuth2PasswordRequestForm) -> int:
        user_data.password = self.pwd_context.hash(user_data.password)
        user_id = await self.user_repo.create_user(user_data)
        
        return user_id