from fastapi import APIRouter

from view.quote import get_one_random_quote

router = APIRouter()


@router.get('/test')
async def quote_hello():
    one_quote = get_one_random_quote()
    return one_quote