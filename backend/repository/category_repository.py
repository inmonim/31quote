from sqlalchemy.orm import Session

from util import session_injection
from model import Category

from DTO import CreateCategoryDTO

class CategoryRepository:
    
    def __init__(self):
        print("category repository 생성")
        pass
    
    async def create_category(self, data : CreateCategoryDTO) -> Category:
        db = await session_injection()
        category = Category(category_id = data.categroy_id,
                            category = data.category)
        db.add(category)
        db.commit()
        return category
    
    async def get_category(self, category_id : int) -> Category | None:
        db = await session_injection()
        category = db.query(Category).get(category_id)
        return category
    
    async def find_categories(self, search_text : str) -> list[Category]:
        db = await session_injection()
        categories = db.query(Category).filter(Category.category.like(f"%{search_text}%")).all()
        
        return categories


category_repo = CategoryRepository()