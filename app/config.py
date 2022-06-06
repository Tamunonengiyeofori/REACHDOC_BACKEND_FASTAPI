#THIS FILE HANDLES PYDANTIC VALIDATION OF ENVIRONMENT VARIABLES 

from pydantic import BaseSettings
# create a validation model for environment variables

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    #tell pydantic to import all environment variables from the .env files.
    class Config:
        env_file = ".env"
        
settings = Settings()