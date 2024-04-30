from pydantic import BaseModel

class CreateUserData(BaseModel):
    nickname : str
    login_id : str
    password : str