from pydantic import BaseModel, Field


class RequestTokenDTO(BaseModel):
    
    access_token : str | None = None
    refresh_token : str

class ResponseTokenDTO(BaseModel):
    
    user_name : str | None = None
    access_token : str
    refresh_token : str
    token_type : str = "bearer"

class ResponseNicknameDTO(BaseModel):
    
    nickname : str = Field(examples=["생각하는 소크라테스 12345"])