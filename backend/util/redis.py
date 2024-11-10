import asyncio
import random
import json
import redis.asyncio as aioredis

from DTO import RequestTokenDTO, ResponseQuoteDTO
from config import REDIS_DB, REDIS_HOST, REDIS_PORT, REFRESH_TOKEN_EXPIRE_MINUTES, ACCESS_TOKEN_EXPIRE_MINUTES

class _R:
    
    def __init__(self):
        self.__r = aioredis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, socket_timeout=1)
        self.connect = True
    
    async def _initalize(self):
        try:
            x = await self.__r.ping()
            print(x)
            print("Redis 연결 성공")
        except:
            self.__r = None
            self.connect = False
            print("Redis 연결 실패!!!")
        finally:
            return self

    async def add_blacklist(self, tokens : RequestTokenDTO) -> bool:
        
        try:
            if tokens.access_token:
                await self.__r.set(tokens.access_token, "blacklist", ex = ACCESS_TOKEN_EXPIRE_MINUTES)
            await self.__r.set(tokens.refresh_token, "blacklist", ex = REFRESH_TOKEN_EXPIRE_MINUTES)
        except:
            return False
        
        return True
    
    async def match_token(self, token : str) -> bool:
        
        if await self.__r.get(token):
            return True
        
        return False
    
    
    async def add_category_id_to_quote_id(self, category_id : int, quote_ids : list[int]):
        """
        c_10 : [q_1, q_2, q_3] 형식으로 데이터 저장
        
        카테고리마다 가지고 있는 quote의 id를 찾기 위해 활용
        """
        category_key = f"c_{category_id}"
        quote_values = [f"q_{quote_id}" for quote_id in quote_ids]
        await self.__r.rpush(category_key, *quote_values)
    

    async def add_quote_id_to_quote(self, quote_id : int, quote_data : json):
        """
        q_1 : {"quote_id" : 1, "ko_sentence" : "예시"...} 형식으로 데이터 저장
        """
        quote_key = f"q_{quote_id}"
        await self.__r.set(quote_key, quote_data)


    async def get_quote_by_category(self, category_id : int):
        """
        category_id 기반으로 하위 quote_id list의 길이를 구한 뒤,
        
        랜덤으로 한 개의 idx(quote_id)를 뽑음
    
        이를 통해 다시 quote를 조회하여 반환함
        """
        category_key = f"c_{category_id}"
        
        c_len = await self.__r.llen(category_key)
        random_idx = random.randint(0, c_len-1)
        random_quote_id = await self.__r.lindex(category_key, random_idx)
        
        quote_raw = await self.__r.get(random_quote_id)
        quote = ResponseQuoteDTO.model_validate_json(quote_raw)
        
        return quote
    
    
    async def add_category_range(self, c_len):
        await self.__r.set("c_len", c_len)
    
    async def get_category_id_range(self) -> int:
        """
        category_id의 범위를 가져옴
        """
        c_len = await self.__r.get("c_len")
        
        return int(c_len)
    
    async def flush_db(self):
        try:
            await self.__r.flushdb()
            return True
        except:
            return False

async def redist_connect_test(r : _R):
    return await r._initalize()

r = _R()
r = asyncio.run(redist_connect_test(r))