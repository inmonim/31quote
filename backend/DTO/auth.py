from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    

class TokenSet(BaseModel):
    access_token : str
    refresh_token : str