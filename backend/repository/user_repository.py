from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from model import User, Role

user_repo = None

class UserRepository:
  
    def __init__(self):
        pass
    
    async def create_user(self, db: Session, user_data : OAuth2PasswordRequestForm, nickname: str) -> bool:
        user = User(nickname = nickname,
                    login_id=user_data.username,
                    password=user_data.password,
                    role_id=1)
        
        db.add(user)
        db.commit()
        return True
    
    async def get_user_by_login_id(self, db : Session, login_id: str) -> User | None:
        user = db.query(User).filter(User.login_id == login_id).first()
        return user
    
    
    async def get_Role(self, db: Session, role_id: int ) -> Role | None:
        role = db.query(Role).get(role_id)
        return role

if __name__ != "__main__":
    user_repo = UserRepository()