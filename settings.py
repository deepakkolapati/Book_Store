from pydantic_settings import SettingsConfigDict, BaseSettings
from logging.config import dictConfig

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    superkey:str
    sender: str
    mail_password: str 
    mail_port: int
    host: str
    database_url: str
   
settings=Settings()
    

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s]: %(filename)s: %(levelname)s: %(lineno)d: %(message)s",
                "datefmt": "%m/%d/%Y %I:%M:%S %p",
                "style": "%",
            },
            "console": {"format": "%(message)s"},
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "console",
            },
            "file": {
                "level": "WARNING",
                "class": "logging.FileHandler",
                "filename": "bookstore.log",
                "formatter": "default",
            },
        },
        # "root": {"level": "INFO", "handlers": ["console"]},
        "loggers": {
            "": {"level": "DEBUG", "handlers": ["file", "console"], "propagate": True}
        },
    }
)