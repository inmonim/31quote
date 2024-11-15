

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from util import get_db
from DTO import ResponseCategoryDTO


from service import CategoryService

router = APIRouter()

category_service = CategoryService()


@router.get("/category_list", status_code=200, summary="카테고리 목록 반환")
async def get_category_list(db : Session = Depends(get_db)) -> list[ResponseCategoryDTO]:
    """
    카테고리 리스트 반환
    
    Returnes:
        list[category_id]
    """
    
    category = await category_service.get_category_list(db)
    
    return category