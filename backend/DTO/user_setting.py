from pydantic import BaseModel

class CategoryDTO(BaseModel):
    category_id : int
    category : str