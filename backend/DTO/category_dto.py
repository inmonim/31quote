from pydantic import BaseModel, ConfigDict

class CreateCategoryDTO(BaseModel):
    
    categroy_id : str
    category : str

class ResponseCategoryDTO(BaseModel):
    
    category_id : int
    category : str
    
    model_config = ConfigDict(from_attributes=True)