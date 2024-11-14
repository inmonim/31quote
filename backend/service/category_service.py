

from repository import category_repo
from DTO import ResponseCategoryDTO


class CategoryService:
    
    def __init__(self):
        self.category_repo = category_repo
        
    async def get_category_list(self, db) -> list[ResponseCategoryDTO]:
        
        category_list = await self.category_repo.get_all_category(db)
        
        category_response = [ResponseCategoryDTO.model_validate(c) for c in category_list]
        
        return category_response