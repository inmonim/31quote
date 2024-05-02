from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_db
from DTO.user import CreateUserDataDTO, LoginDataDTO

from view.user_manage import create_user, login_user

router = APIRouter()

@router.post('/create_user')
async def create_user_controller(user_data : CreateUserDataDTO, db : Session = Depends(get_db)):
    
    user_id = create_user(user_data, db)
    
    result = {'user_id' : user_id,
              'detail' : '유저 생성 완료'}

    return JSONResponse(result,
                            201)

@router.post('/login')
async def login_controller(login_data : LoginDataDTO, db : Session = Depends(get_db)):
    
    user_id = login_user(login_data, db)
    
    result = {'user_id' : user_id,
              'detail' : '로그인 성공'}
    
    return JSONResponse(result,
                        200) 