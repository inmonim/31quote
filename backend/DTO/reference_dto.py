from pydantic import BaseModel

class CreateReferenceTypeDTO(BaseModel):
    
    reference_id : int | None = None
    reference_type : str


class CreateReferenceDTO(BaseModel):
    
    reference_name : str
    year : int | None = None
    reference_type_id : int
    
    
class ResponseReferenceTypeDTO(BaseModel):
    
    reference_type_id : int
    reference_type : str
    
    class Config:
        from_attributes = True


class ResponseReferenceDTO(BaseModel):
    
    reference_id : int
    reference_name : str
    year : int | None = None
    reference_type : ResponseReferenceTypeDTO
    
    class Config:
        from_attributes = True