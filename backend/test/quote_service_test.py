from unittest.mock import AsyncMock
from service import QuoteService
from model import Quote, Category
from DTO import ResponseQuoteDTO

import pytest

@pytest.fixture
def mock_repo(mocker):
    # repository의 get_category_random_quote 메서드를 비동기로 Mock 처리
    return mocker.patch("repository.quote_repository.quote_repo.get_category_random_quote", new_callable=AsyncMock)

@pytest.mark.asyncio
async def test_get_category_random_quote(mock_repo):
    # mock 데이터를 설정
    mock_repo.return_value = Quote(**{
        "quote_id": 1,
        "ko_sentence": "테스트 한국어 문장",
        "en_sentence": "Test English Sentence",
        "category": Category(**{"category_id": 1, "category": "테스트 카테고리"}),
        "speaker": None,
        "reference": None
    })
    
    # QuoteService 인스턴스 생성
    service = QuoteService()
    
    # 실제 테스트할 category_id
    category_id = 1
    
    # 테스트 대상 메서드 호출
    result = await service.get_category_random_quote(category_id)
    
    # 결과 검증 (ResponseQuoteDTO로 변환된 데이터)
    assert isinstance(result, ResponseQuoteDTO)
    assert result.ko_sentence == "테스트 한국어 문장"
    assert result.en_sentence == "Test English Sentence"
    assert result.category.category == "테스트 카테고리"