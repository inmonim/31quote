from pydantic import BaseModel

class CreateCategoryDTO(BaseModel):
    
    category : str