import os

if os.environ.get("31QUOTE_DEPLOY_MODE") == "PROD":
    pass

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
    ACCESS_TOKEN_EXPIRE_MINUTES = env.get('ACCESS_TOKEN_EXPIRE_MINUTES')
    REFRESH_TOKEN_EXPIRE_MINUTES = env.get('REFRESH_TOKEN_EXPIRE_MINUTES')
    
    del env