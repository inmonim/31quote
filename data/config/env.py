import os

def convert_to_int(value: str | None):
    if value is None:
        raise ValueError("None 값은 숫자로 변환할 수 없습니다.")
    return int(value)

if os.environ.get("31QUOTE_DEPLOY_MODE") == "deploy":
    DB_HOST = os.environ.get("DB_HOST")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_USERNAME = os.environ.get("DB_USERNAME")
    DB_TABLE = os.environ.get("DB_TABLE")
    DB_PORT = os.environ.get("DB_PORT")
    
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

else:
    from dotenv import dotenv_values
    
    env = dotenv_values(os.path.dirname(os.path.abspath(__file__))+"/.env")
    
    DB_HOST = env.get("DB_HOST")
    DB_PASSWORD = env.get("DB_PASSWORD")
    DB_USERNAME = env.get("DB_USERNAME")
    DB_TABLE = env.get("DB_TABLE")
    DB_PORT = env.get("DB_PORT")
    
    OPENAI_API_KEY = env.get("OPENAI_API_KEY")
    
    del env