from sqlalchemy.orm import Session

from model.quote import UserCheckedCategory, QuoteCategory
from DTO.user_setting import CategoryDTO


class UserSettingRepositry:
    
    def __init__(self, db : Session):
        self.db = db
    
    
    def get_users_checked_category_id_list(self, user_id : int) -> list[int]:
        checked_category = self.db.query(UserCheckedCategory
                                         ).filter(UserCheckedCategory.user_id == user_id)
        
        category_id_list = [obj.category_id for obj in checked_category]
        
        return category_id_list
    
    
    def get_users_checked_category_list(self, user_id : int) -> list[CategoryDTO]:
        
        user_category_id_list = self.get_users_checked_category_id_list(user_id)
        
        category_list_obj = self.db.query(QuoteCategory).filter(QuoteCategory.category_id.in_(user_category_id_list))

        category_list = [CategoryDTO(**vars(category_obj)) for category_obj in category_list_obj]
        
        return category_list
    
    
    def delete_users_checked_cateogry(self, user_id : int, category_id : int):
        
        try:
            user_cateogry_obj = self.db.query(UserCheckedCategory
                                              ).filter(UserCheckedCategory.user_id == user_id,
                                                       UserCheckedCategory.category_id == category_id)
            user_cateogry_obj.delete()

        except:
            return False
        
        return True
    
    
    def delete_users_checked_category_list(self, user_id : int, category_id_list : list[int]) -> bool:
        
        try:
            user_cateogry_obj = self.db.query(UserCheckedCategory
                                        ).filter(UserCheckedCategory.user_id == user_id,
                                                UserCheckedCategory.category_id.in_(category_id_list))
            user_cateogry_obj.delete()
            self.db.commit()

        except:
            return False
        
        return True
    
    
    def add_user_checked_cateogry_list(self, user_id : int, category_id_list : list[int]) -> bool:
        
        category_dict = [{'user_id' : user_id, 'category_id' : ci } for ci in category_id_list]
        
        try:
            self.db.bulk_insert_mappings(UserCheckedCategory, category_dict)
            self.db.commit()
        
        except Exception as e:
            return False
        
        return True