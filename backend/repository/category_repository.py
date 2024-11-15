from sqlalchemy.orm import Session

from model import Category

from DTO import CreateCategoryDTO

class CategoryRepository:
    
    def __init__(self):
        print("category repository 생성")
        pass
    
    async def create_category(self, data : CreateCategoryDTO, db: Session) -> Category:
        category = Category(category_id = data.categroy_id,
                            category = data.category)
        db.add(category)
        db.commit()
        return category
    
    async def get_category(self, category_id : int, db: Session) -> Category | None:
        category = db.query(Category).get(category_id)
        return category
    
    async def find_categories(self, search_text : str, db: Session) -> list[Category]:
        categories = db.query(Category).filter(Category.category.like(f"%{search_text}%")).all()
        
        return categories
    
    async def get_all_category(self, db: Session) -> list[Category]:
        categories = db.query(Category).all()
        
        return categories


category_repo = CategoryRepository()