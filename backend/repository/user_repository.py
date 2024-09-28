from fastapi.security import OAuth2PasswordRequestForm

from util import session_injection
from model import User, Role

user_repo = None

class UserRepository:
  
    def __init__(self):
        pass
    
    async def create_user(self, user_data : OAuth2PasswordRequestForm) -> int:
        db = await session_injection()
        user = User(login_id=user_data.username,
                    password=user_data.password,
                    role_id=1)
        
        db.add(user)
        db.commit()
        return user.user_id

if __name__ != "__main__":
    user_repo = UserRepository()