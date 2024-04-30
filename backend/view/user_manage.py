from sqlalchemy.orm import Session

from DTO.user import CreateUserData
from model.user import User


def create_user(user_data : CreateUserData, db : Session):

    new_user = User(
        nickname = user_data.nickname,
        login_id = user_data.login_id,
        password = user_data.password
    )
    
    db.add(new_user)
    
    db.commit()

    return new_user.user_id