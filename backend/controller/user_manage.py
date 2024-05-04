from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from DTO.user import CreateUserDataDTO, LoginDataDTO
from DTO.auth import Token

from view.user_manage import (create_user, login_user,
                            #   google_login, get_google_login_url
                              )

router = APIRouter()

@router.post('/createUser')
def create_user_controller(user_data : CreateUserDataDTO, db : Session = Depends(get_db)):
    
    user_id = create_user(user_data, db)
    
    result = {'user_id' : user_id,
              'detail' : '유저 생성 완료'}

    return JSONResponse(result,
                            201)

@router.post('/login')
def login_controller(login_data : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    
    result_data = login_user(login_data, db)
    user_id = result_data['user_id']
    token : Token = result_data['token']
    
    result = {'user_id' : user_id,
              'access_token' : token.access_token,
              'token_type' : token.token_type,
              'detail' : '로그인 성공'}
    
    return JSONResponse(result,
                        200)



# @router.get("/login/google")
# async def login_google():
    
#     url = get_google_login_url()
    
#     result = {'url' : url}
    
#     return JSONResponse(result,
#                         200)

# @router.post('/GoogleLogin')
# def google_login_controller(form_data : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    
#     user_id = google_login(form_data, db)
    
#     result = {'user_id' : user_id,
#               'detail' : '로그인 성공'}
    
#     return JSONResponse(result,
#                         200)