from datetime import datetime

from dateutil.parser import parse

# from passlib.context import CryptContext
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# password = pwd_context.hash('password')
password = '$2b$12$lVLTTayL8HD6KogfHpao7ucnpXEt6I0C/kyjd683hv1rDm77ytGH6'

created_at: datetime = parse('2023-07-01 00:00:00')
today: datetime = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
dt_format: str = '%Y-%m-%d %H:%M:%S%z'

dt_fields = {
    'created_at': created_at,
    'updated_at': created_at,
    'deleted_at': None
}

dt_fields2 = {
    'created_at': created_at,
    # 'updated_at': created_at,
    'deleted_at': None
}
