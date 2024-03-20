from pydantic_settings import SettingsConfigDict, BaseSettings

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    superkey:str
    sender: str
    mail_password: str 
    mail_port: int
    host: str
    database_url: str
   
settings=Settings()
    