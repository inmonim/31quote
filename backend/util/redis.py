import redis.asyncio as aioredis

from DTO import RequestTokenDTO
from config import REDIS_DB, REDIS_HOST, REDIS_PORT, REFRESH_TOKEN_EXPIRE_MINUTES, ACCESS_TOKEN_EXPIRE_MINUTES

def convert_to_int(value: str | None):
    if value is None:
        raise ValueError("None 값은 숫자로 변환할 수 없습니다.")
    return int(value)

class _R:
    
    def __init__(self):
        self.__r = aioredis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        print("Redis 연결 성공")

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


r = _R()