from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from DTO.user import CreateUserData

from view.user_manage import create_user

router = APIRouter()

@router.post('/create_user')
async def create_user_controller(user_data : CreateUserData, db : Session = Depends(get_db)):
    
    try:
        user_id = create_user(user_data, db)
    except Exception as e:
        raise HTTPException(400, detail=e)
    
    return {'make_user' : user_id}