from sqlalchemy.orm import Session

from util import dto_to_model

from model import Reference, ReferenceType
from DTO import CreateReferenceDTO, CreateReferenceTypeDTO

class ReferenceRepository:
    
    def __init__(self):
        pass
    
    async def create_reference_type(self, db: Session,  data : CreateReferenceTypeDTO) -> ReferenceType:
        reference_type = dto_to_model(data, ReferenceType)
        db.add(reference_type)
        db.commit()
        return reference_type
    
    async def create_reference(self, db: Session,  data : CreateReferenceDTO) -> Reference:
        reference = dto_to_model(data, Reference)
        db.add(reference)
        db.commit()
        return reference
    
    async def get_reference_type(self, db: Session,  reference_type_id : int) -> ReferenceType | None:
        reference_type = db.query(ReferenceType).get(reference_type_id)
        return reference_type
    
    async def get_reference(self, db: Session,  reference_id : int) -> Reference | None:
        reference = db.query(Reference).get(reference_id)
        return reference
    
    async def find_references(self, db: Session,  search_text : str) -> list[Reference]:
        result = db.query(Reference).filter(Reference.reference_name.like(f"%{search_text}%")).all()
        return result
    
    async def get_all_reference_types(self, db: Session, ) -> list[ReferenceType]:
        result = db.query(ReferenceType).all()
        return result


reference_repo = ReferenceRepository()