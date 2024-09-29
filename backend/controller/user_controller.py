from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from DTO import TokenResponseDTO

from service import UserManageService

router = APIRouter()

user_manage_service = UserManageService()

@router.post('/', status_code=201, summary="유저 생성")
async def create_user(user_data : OAuth2PasswordRequestForm = Depends()) -> int:
    
    user_id = await user_manage_service.create_user(user_data)
    
    return user_id


@router.post('/login', status_code=200, summary="로그인")
async def login(user_data : OAuth2PasswordRequestForm = Depends()) -> TokenResponseDTO:
    
    token_response = await user_manage_service.login(user_data)
    
    return token_response