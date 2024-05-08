from sqlalchemy.orm import Session

from DTO.user import CreateUserDataDTO, LoginDataDTO, LoginValidationDTO
from model.user import User, UserProfile

class UserRepository:
    
    def __init__(self, db : Session):
        self.db = db
        
    
    def check_duplicated_nickname(self, nickname : str) -> bool:
        
        if self.db.query(UserProfile).filter(UserProfile.nickname == nickname).count():
            return True
        return False
    
    
    def check_duplicated_login_id(self, login_id : str) -> bool:

        if self.db.query(UserProfile).filter(UserProfile.login_id == login_id).count():
            return True
        return False
    
    
    def create_profile(self, user_profile_data : UserProfile) -> int | bool:
        
        try:
            self.db.add(user_profile_data)
            self.db.commit()
            
            user_id = user_profile_data.user_id
        except:
            return False
        
        return user_id
    
    
    def create_user(self, user_data : User) -> bool:
        
        try:
            self.db.add(user_data)
            self.db.commit()
        except:
            return False
        
        return True
    
    
    def get_login_validation_value(self, login_id) -> LoginValidationDTO | bool:
        
        user = self.db.query(UserProfile).filter(UserProfile.login_id == login_id).first()
        if not user:
            return False
        
        login_validation_value = LoginValidationDTO(user_id = user.user_id,
                                                    nickname = user.nickname,
                                                    hashed_pwd = user.password)
        
        return login_validation_value