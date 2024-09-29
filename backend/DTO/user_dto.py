from pydantic import BaseModel, Field

class TokenResponseDTO(BaseModel):
    
    user_name : str
    access_token : str
    refresh_token : str
    token_type : str = "bearer"