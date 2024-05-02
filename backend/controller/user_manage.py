from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_db
from DTO.user import CreateUserDataDTO

from view.user_manage import create_user

router = APIRouter()

@router.post('/create_user')
async def create_user_controller(user_data : CreateUserDataDTO, db : Session = Depends(get_db)):
    
    user_id = create_user(user_data, db)
    
    result = {'user_id' : user_id}

    return JSONResponse(result,
                            201)