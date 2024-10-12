from fastapi import APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from util import get_db
from DTO import ResponseNicknameDTO, ResponseTokenDTO, RequestTokenDTO

from auth import get_current_user
from service import UserManageService

router = APIRouter()

user_manage_service = UserManageService()

@router.post('/', status_code=201, summary="유저 생성")
async def create_user(user_data : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)) -> ResponseNicknameDTO:
    
    nickname = await user_manage_service.create_user(user_data, db)
    
    return nickname


@router.post('/login', status_code=200, summary="로그인")
async def login(user_data : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)) -> ResponseTokenDTO:
    
    token_response = await user_manage_service.login(user_data, db)
    
    return token_response

@router.post('/token_refresh', status_code=200, summary="토큰 재발급", description="반드시 refreshToken을 보낼 것.")
async def toekn_refresh(authorization: str = Header(None), user = Depends(get_current_user)) -> ResponseTokenDTO:
    
    token_dto = RequestTokenDTO(refresh_token=authorization[7:])
    
    token_response = await user_manage_service.token_refresh(token_dto, user)
    
    return token_response

@router.patch('/logout', status_code=202, summary="로그아웃")
async def logout(tokens : RequestTokenDTO, user = Depends(get_current_user)) -> None:
    
    await user_manage_service.logout(tokens)
    
    return None