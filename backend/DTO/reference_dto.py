from pydantic import BaseModel

from util import model_to_dto
from model import Reference, ReferenceType

class CreateReferenceTypeDTO(BaseModel):
    
    reference_id : int = None
    reference_type : str


class CreateReferenceDTO(BaseModel):
    
    reference_name : str
    year : int = None
    reference_type_id : int
    
    
class ResponseReferenceTypeDTO(BaseModel):
    
    reference_type_id : int
    reference_type : str


class ResponseReferenceDTO(BaseModel):
    
    reference_id : int
    reference_name : str
    year : int = None
    reference_type : ResponseReferenceTypeDTO
    
    @classmethod
    def from_model(cls, reference):
        return cls(reference_id = reference.reference_id,
                   reference_name = reference.reference_name,
                   year = reference.year,
                   reference_type = model_to_dto(reference.reference_type, ResponseReferenceTypeDTO))