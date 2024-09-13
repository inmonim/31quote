from sqlalchemy.orm import Session

from util import dto_to_model

from model import Reference, ReferenceType
from DTO import CreateReferenceDTO, CreateReferenceTypeDTO

class ReferenceRepository:
    
    def __init__(self, db : Session):
        self.db = db
    
    def create_reference_type(self, data : CreateReferenceTypeDTO) -> int:
        reference_type = dto_to_model(data, ReferenceType)
        self.db.add(reference_type)
        self.db.commit()
        return reference_type.reference_type_id
    
    def create_reference(self, data : CreateReferenceDTO) -> int:
        reference = dto_to_model(data, Reference)
        self.db.add(reference)
        self.db.commit()
        return reference.reference_id
    
    def get_reference_type(self, reference_type_id : int) -> ReferenceType:
        reference_type = self.db.query(ReferenceType).get(reference_type_id)
        return reference_type
    
    def get_reference(self, reference_id : int) -> Reference:
        reference = self.db.query(Reference).get(reference_id)
        return reference