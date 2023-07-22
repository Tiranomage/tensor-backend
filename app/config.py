import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    class Config:
        # Костыль для поиска переменных при запуске и приложения и тестов
        env_file = '../.env' if os.path.isfile('../.env') else '.env'
        env_file_encoding = 'utf-8'

        case_sensitive = True
        allow_mutation = False


class AppSettings(Settings):
    HOST: str = Field(default='localhost')
    PORT: int = Field(default=8080)
    JWT_SECRET: str = Field(default='SECRET')
    JWT_LIFETIME: int = Field(default=86400)
    USER_MANAGER_SECRET: str = Field(default='SECRET')
    STATIC: str = Field(default='../static')
    STATIC_LINK: str = Field(default='static')
    MAX_FILE_SIZE: int = Field(default=1024 * 1024 * 50)  # = 50MB

    class Config:
        env_prefix = 'BACK_'


class DatabaseSettings(Settings):
    HOST: str = Field(default='localhost')
    NAME: str = Field(default='postgres')
    USER: str = Field(default='postgres')
    PASS: str = Field(default='postgres')
    PORT: int = Field(default=5432)
    ECHO: bool = Field(default=False)

    @property
    def database_url(self) -> str:
        return f'postgresql+asyncpg://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}?async_fallback=True'

    class Config:
        env_prefix = 'DATABASE_'


class TestDatabaseSettings(DatabaseSettings):
    class Config:
        env_prefix = 'TEST_DB_'


class MinioSettings(Settings):
    ACCESS_KEY: str = Field(default='SECRET')
    SECRET_KEY: str = Field(default='SECRET')
    ROOT_USER: str = Field(default='minio')
    ROOT_PASS: str = Field(default='minio')
    PORT: int = Field(default=9000)
    CONSOLE: int = Field(default=9090)

    class Config:
        env_prefix = 'MINIO_'


database_settings = DatabaseSettings()
test_database_settings = TestDatabaseSettings()
app_settings = AppSettings()
minio_settings = MinioSettings()
