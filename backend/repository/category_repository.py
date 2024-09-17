from sqlalchemy.orm import Session

from model import Category

from DTO import CreateCategoryDTO

class CategoryRepository:
    
    def __init__(self, db : Session):
        self.db = db
    
    def create_category(self, data : CreateCategoryDTO) -> Category:
        category = Category(category_id = data.categroy_id,
                            category = data.category)
        self.db.add(category)
        self.db.commit()
        return category
    
    def get_category(self, category_id : int) -> Category | None:
        category = self.db.query(Category).get(category_id)
        return category
    
    def find_categories(self, search_text : str) -> list[Category]:
        categories = self.db.query(Category).filter(Category.category.like(f"%{search_text}%")).all()
        
        return categories