from fastapi import HTTPException
from sqlalchemy.orm import Session

from repository.user_setting import UserSettingRepositry
from DTO.user_setting import CategoryDTO


def get_category_list_by_user(db : Session, user_id : int) -> list[CategoryDTO]:
    
    user_setting_repo = UserSettingRepositry(db)
    
    category_list = user_setting_repo.get_users_checked_category_list(user_id)
    
    return category_list


def update_users_category(db : Session, user_id : int, checked_category_list : list[int]) -> list[CategoryDTO]:
    
    user_setting_repo = UserSettingRepositry(db)
    
    before_category_id_list = user_setting_repo.get_users_checked_category_id_list(user_id)
    
    # 삭제할 카테고리와 추가할 카테고리 가려내기
    before_category_set = set(before_category_id_list)
    
    add_category_list = []
    
    for ci in checked_category_list:
        # 이전 카테고리 셋에 없으면 추가
        if ci not in before_category_set:
            add_category_list.append(ci)
        
        # 이전 카테고리 셋에 있으면 셋에서 삭제
        else:
            before_category_set.remove(ci)
    
    # 남은 카테고리 셋(선택되지 않음)은 삭제 예정 리스트
    delete_category_list = list(before_category_set)
    
    if delete_category_list:
        delete_plag = user_setting_repo.delete_users_checked_category_list(user_id, delete_category_list)
        if delete_plag == False:
            raise HTTPException(500, "failed delete users category")
    
    if add_category_list:
        add_plag = user_setting_repo.add_user_checked_cateogry_list(user_id, add_category_list)
        if add_plag == False:
            raise HTTPException(500, "failed add users category")
    
    
    updated_users_category_list = get_category_list_by_user(db, user_id)
    
    return updated_users_category_list