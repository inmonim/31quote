from sqlalchemy.orm import Session

from model import Category

from DTO import CreateCategoryDTO

class CategoryRepository:
    
    def __init__(self):
        print("category repository 생성")
        pass
    
    async def create_category(self, db: Session, data : CreateCategoryDTO) -> Category:
        category = Category(category_id = data.categroy_id,
                            category = data.category)
        db.add(category)
        db.commit()
        return category
    
    async def get_category(self, db: Session, category_id : int) -> Category | None:
        category = db.query(Category).get(category_id)
        return category
    
    async def find_categories(self, db: Session, search_text : str) -> list[Category]:
        categories = db.query(Category).filter(Category.category.like(f"%{search_text}%")).all()
        
        return categories


category_repo = CategoryRepository()