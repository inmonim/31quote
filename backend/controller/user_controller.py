from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from service import UserManageService

router = APIRouter()

user_manage_service = UserManageService()

@router.post('/', status_code=201, summary="유저 생성")
async def create_user(user_data : OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)) -> int:
    
    user_id = await user_manage_service.create_user(user_data)
    
    return user_id