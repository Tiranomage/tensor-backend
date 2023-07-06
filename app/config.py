import os
from distutils.util import strtobool
from dotenv import load_dotenv
# Файл настроек должен быть скопирован в приложение FastApi из docker-compose проекта
load_dotenv('../.env')

DATABASE_NAME = os.environ.get('DATABASE_NAME', 'postgres')
DATABASE_USER = os.environ.get('DATABASE_USER', 'postgres')
DATABASE_PASS = os.environ.get('DATABASE_PASS', 'postgres')
DATABASE_PORT = int(os.environ.get('DATABASE_PORT', 5432))
DATABASE_HOST = os.environ.get('DATABASE_PORT', 'localhost')
DATABASE_ECHO = strtobool(os.environ.get('DATABASE_ECHO', 'false'))

DATABASE_URL = f'postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'

BACK_HOST = os.environ.get('BACK_HOST', 'localhost')
BACK_PORT = int(os.environ.get('BACK_PORT', 8081))

JWT_SECRET = os.environ.get('BACK_JWT_SECRET', 'SECRET')
