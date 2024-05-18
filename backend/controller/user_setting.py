from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder as jse

from database import get_db
from auth.auth import get_current_user
from DTO.user_setting import CategoryDTO
from service import user_setting

router = APIRouter()

@router.get('/getAllCategory')
async def get_all_category(db : Session = Depends(get_db)):
    
    category_list = user_setting.get_all_category_list(db)
    
    return JSONResponse(jse(category_list),
                        200)


@router.get('/getUserCategory')
async def get_user_category(user_id : int = Depends(get_current_user), db : Session = Depends(get_db)) -> list[CategoryDTO]:
    
    user_category_result = user_setting.get_uses_category_list(db, user_id)
    
    if not len(user_category_result):
        return JSONResponse({'message' : 'not found checked category'},
                            200)
    
    return JSONResponse(jse(user_category_result),
                        200)


@router.put('/updateUserCategory')
async def update_user_category(checked_category_id : list[int],
                               user_id : int = Depends(get_current_user),
                               db : Session = Depends(get_db)) -> list[CategoryDTO]:
    
    user_category_result = user_setting.update_users_category(db, user_id, checked_category_id)

    if not len(user_category_result):
        return JSONResponse({'message' : 'not found checked category'},
                            200)
    
    return JSONResponse(jse(user_category_result),
                        200)