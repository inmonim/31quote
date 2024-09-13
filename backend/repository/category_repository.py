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
    
    def get_category(self, category_id : int) -> Category:
        category = self.db.query(Category).get(category_id)
        return category