from util import get_db
from DTO import ResponseQuoteDTO
from util import r
from repository import quote_repo, category_repo


class ServerSetup:
    
    def __init__(self, redis = r):
        self.r = redis
        print("서버 생성")
        
    async def mount_redis_data(self):
        """
        Redis에 quote데이터 전체를 캐싱
        
        category_id : [quote_id_1, quote_id_2...]
        이 형식으로 카테고리마다 하위 quote_id를 리스트 형식으로 넣음
        
        quote_id : {"summary" : "예시" ... }
        위 형식으로 quote_id에 해당하는 데이터를 json형식으로 value에 삽입
        """
        
        if not self.r.connect:
            return False
        
        db = await anext(get_db())
        
        category_list = await category_repo.get_all_category(db)
        category_dict = {int(category.category_id) : [] for category in category_list}
        
        # set category len
        await r.add_category_range(len(category_list))
        
        quote_list = await quote_repo.get_all_quote(db)
        quote_dto_list = [ResponseQuoteDTO.model_validate(quote) for quote in quote_list]
        
        # dict id 삽입 및 redis 캐싱
        for i in range(len(quote_dto_list)):
            quote = quote_dto_list[i]
            category_id = quote.category.category_id
            
            category_dict[category_id].append(quote.quote_id)
            await r.add_quote_id_to_quote(quote.quote_id, quote.model_dump_json())
        
        # category_id - list[quote_id] 캐싱
        for k, v in category_dict.items():
            await r.add_category_id_to_quote_id(k, v)
        
        # test
        x = await r.get_quote_by_category(1)
        c = await r.get_category_id_range()
        
        return True