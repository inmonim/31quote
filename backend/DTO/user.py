from pydantic import BaseModel, Field

class CreateUserDataDTO(BaseModel):

    nickname : str = Field(..., min_length=2, max_length=20, example="소크라테스")
    login_id : str = Field(..., min_length=6, max_length=20, pattern=r"^[a-zA-Z0-9]{6,}$",
                          description="id는 6자 이상 20자 이하", example="31quote") 
    password: str = Field(..., min_length=8, max_length=20, pattern=r"^[a-zA-Z0-9\d!@#$%^&*]{8,}$",
                          description="비밀번호는 영문과 숫자를 포함해 8자 이상 20자 이하", example="quote321")


class LoginDataDTO(BaseModel):
    
    login_id : str = Field(..., min_length=6, max_length=20, pattern=r"^[a-zA-Z0-9]{6,}$",
                          description="id는 6자 이상 20자 이하", example="31quote") 
    password: str = Field(..., min_length=8, max_length=20, pattern=r"^[a-zA-Z0-9\d!@#$%^&*]{8,}$",
                          description="비밀번호는 영문과 숫자를 포함해 8자 이상 20자 이하", example="quote321")