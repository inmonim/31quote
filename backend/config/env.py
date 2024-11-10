import os

def convert_to_int(value: str | None):
    if value is None:
        raise ValueError("None 값은 숫자로 변환할 수 없습니다.")
    return int(value)

if os.environ.get("31QUOTE_DEPLOY_MODE") == "DEPLOY":
    DB_HOST = os.environ.get("DB_HOST")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_USERNAME = os.environ.get("DB_USERNAME")
    DB_TABLE = os.environ.get("DB_TABLE")
    DB_PORT = os.environ.get("DB_PORT")
    
    ADMIN_ID = os.environ.get('ADMIN_ID')
    ALGORITHM = os.environ.get('ALGORITHM')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES = convert_to_int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))
    REFRESH_TOKEN_EXPIRE_MINUTES = convert_to_int(os.environ.get('REFRESH_TOKEN_EXPIRE_MINUTES'))
    
    REDIS_HOST = os.environ.get("REDIS_HOST")
    REDIS_PORT = os.environ.get("REDIS_PORT")
    REDIS_DB = os.environ.get("REDIS_DB")

else:
    from dotenv import dotenv_values
    
    env = dotenv_values(os.path.dirname(os.path.abspath(__file__))+"/dev.env")
    
    DB_HOST = env.get("DB_HOST")
    DB_PASSWORD = env.get("DB_PASSWORD")
    DB_USERNAME = env.get("DB_USERNAME")
    DB_TABLE = env.get("DB_TABLE")
    DB_PORT = env.get("DB_PORT")
    
    ADMIN_ID = env.get('ADMIN_ID')
    ALGORITHM = env.get('ALGORITHM')
    SECRET_KEY = env.get('SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES = convert_to_int(env.get('ACCESS_TOKEN_EXPIRE_MINUTES'))
    REFRESH_TOKEN_EXPIRE_MINUTES = convert_to_int(env.get('REFRESH_TOKEN_EXPIRE_MINUTES'))
    
    REDIS_HOST = env.get("REDIS_HOST")
    REDIS_PORT = env.get("REDIS_PORT")
    REDIS_DB = env.get("REDIS_DB")
    
    del env