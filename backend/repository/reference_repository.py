from util import session_injection, dto_to_model

from model import Reference, ReferenceType
from DTO import CreateReferenceDTO, CreateReferenceTypeDTO

class ReferenceRepository:
    
    def __init__(self):
        pass
    
    async def create_reference_type(self, data : CreateReferenceTypeDTO) -> ReferenceType:
        db = await session_injection()
        reference_type = dto_to_model(data, ReferenceType)
        db.add(reference_type)
        db.commit()
        return reference_type
    
    async def create_reference(self, data : CreateReferenceDTO) -> Reference:
        db = await session_injection()
        reference = dto_to_model(data, Reference)
        db.add(reference)
        db.commit()
        return reference
    
    async def get_reference_type(self, reference_type_id : int) -> ReferenceType | None:
        db = await session_injection()
        reference_type = db.query(ReferenceType).get(reference_type_id)
        return reference_type
    
    async def get_reference(self, reference_id : int) -> Reference | None:
        db = await session_injection()
        reference = db.query(Reference).get(reference_id)
        return reference
    
    async def find_references(self, search_text : str) -> list[Reference]:
        db = await session_injection()
        result = db.query(Reference).filter(Reference.reference_name.like(f"%{search_text}%")).all()
        return result
    
    async def get_all_reference_types(self) -> list[ReferenceType]:
        db = await session_injection()
        result = db.query(ReferenceType).all()
        return result


reference_repo = ReferenceRepository()