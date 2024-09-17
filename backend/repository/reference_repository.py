from sqlalchemy.orm import Session

from util import dto_to_model

from model import Reference, ReferenceType
from DTO import CreateReferenceDTO, CreateReferenceTypeDTO

class ReferenceRepository:
    
    def __init__(self, db : Session):
        self.db = db
    
    def create_reference_type(self, data : CreateReferenceTypeDTO) -> ReferenceType:
        reference_type = dto_to_model(data, ReferenceType)
        self.db.add(reference_type)
        self.db.commit()
        return reference_type
    
    def create_reference(self, data : CreateReferenceDTO) -> Reference:
        reference = dto_to_model(data, Reference)
        self.db.add(reference)
        self.db.commit()
        return reference
    
    def get_reference_type(self, reference_type_id : int) -> ReferenceType | None:
        reference_type = self.db.query(ReferenceType).get(reference_type_id)
        return reference_type
    
    def get_reference(self, reference_id : int) -> Reference | None:
        reference = self.db.query(Reference).get(reference_id)
        return reference
    
    def find_references(self, search_text : str) -> list[Reference]:
        result = self.db.query(Reference).filter(Reference.reference_name.like(f"%{search_text}%")).all()
        return result
    
    def get_all_reference_types(self) -> list[ReferenceType]:
        result = self.db.query(ReferenceType).all()
        return result