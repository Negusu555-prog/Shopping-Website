<<<<<<< HEAD
from pydantic import BaseSettings
from typing import Optional


# class Config(BaseSettings):
#     MYSQL_USER: str = "root"
#     MYSQL_PASSWORD: str = "root_password"
#     MYSQL_DATABASE: str = "main"
#     MYSQL_HOST: str = "localhost"
#     MYSQL_PORT: str = "3306"
#     DATABASE_URL: str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

class Config(BaseSettings):
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_HOST: str
    MYSQL_PORT: str
    OPENAI_API_KEY: str

    @property
    def DATABASE_URL(self):
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    class Config:
        env_file = "env"
=======
from pydantic import BaseSettings
from typing import Optional


class Config(BaseSettings):
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "root_password"
    MYSQL_DATABASE: str = "main"
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: str = "3306"
    DATABASE_URL: str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
>>>>>>> 7222ba1b59b8f654c5bb751768b4493b1004fb18
