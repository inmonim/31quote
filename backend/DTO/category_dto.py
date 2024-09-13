from pydantic import BaseModel


class CreateCategoryDTO(BaseModel):
    
    categroy_id : str
    category : str

class ResponseCategoryDTO(BaseModel):
    
    category_id : int
    category : str