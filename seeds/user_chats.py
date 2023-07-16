from datetime import timedelta

from app.models.models import ChatType, UserRole
from .const import password, created_at, today, dt_format

users = [
    {
        'id': '5f4ebc21-db76-4ca2-989b-227b50d3be85',
        'username': 'superuser',
        'email': 'superuser@example.com',
        'hashed_password': password,
        'is_active': True,
        'is_superuser': True,
        'is_verified': True,
        'external': {},
        'created_at': created_at,
        'updated_at': created_at,
        'deleted_at': None
    },
    {
        'id': '7d8b6ca9-c556-49d4-a132-91ef00698d80',
        'username': 'user1',
        'email': 'user1@example.com',
        'hashed_password': password,
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
        'external': {},
        'created_at': created_at,
        'updated_at': created_at,
        'deleted_at': None
    },
    {
        'id': '7c0e9b3d-b741-402b-901d-cb3bd8d01627',
        'username': 'user2',
        'email': 'user2@example.com',
        'hashed_password': password,
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
        'external': {},
        'created_at': created_at,
        'updated_at': created_at,
        'deleted_at': None
    },
    {
        'id': 'e6f79f3b-47fa-4d24-8713-7adb4814c689',
        'username': 'user3',
        'email': 'user3@example.com',
        'hashed_password': password,
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
        'external': {},
        'created_at': created_at,
        'updated_at': created_at,
        'deleted_at': None
    },
    {
        'id': '45630130-eca4-45be-aec3-b1910b9e075f',
        'username': 'user4',
        'email': 'user4@example.com',
        'hashed_password': password,
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
        'external': {},
        'created_at': created_at,
        'updated_at': created_at,
        'deleted_at': None
    },
    {
        'id': '62349685-5276-464f-91e5-1dbc636dc420',
        'username': 'user5',
        'email': 'user5@example.com',
        'hashed_password': password,
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
        'external': {},
        'created_at': created_at,
        'updated_at': created_at,
        'deleted_at': None
    },
    {
        'id': 'ef2a5278-26d2-464e-95ce-c491b999f3bf',
        'username': 'user6',
        'email': 'user6@example.com',
        'hashed_password': password,
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
        'external': {},
        'created_at': created_at,
        'updated_at': created_at,
        'deleted_at': None
    },
    {
        'id': 'bbe07314-3183-4be9-b26f-892af73d2788',
        'username': 'user7',
        'email': 'user7@example.com',
        'hashed_password': password,
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
        'external': {},
        'created_at': created_at,
        'updated_at': created_at,
        'deleted_at': None
    },
    {
        'id': '7dc4e1b8-7cc1-4815-b3b9-050c268d0efb',
        'username': 'user8',
        'email': 'user8@example.com',
        'hashed_password': password,
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
        'external': {},
        'created_at': created_at,
        'updated_at': created_at,
        'deleted_at': None
    },
    {
        'id': '614eb932-f929-4edb-b9ee-f0a36a0c7926',
        'username': 'user9',
        'email': 'user9@example.com',
        'hashed_password': password,
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
        'external': {},
        'created_at': created_at,
        'updated_at': created_at,
        'deleted_at': None
    },
]

chats = [
    {
        'id': '233a2f62-64c6-4130-addf-eb2c62ced681',
        'parent_id': None,
        'type': ChatType.group.value,
        'external': {
            'title': 'Базовая студенческая группа',
            'description': 'Здесь студенты общаются',
        },
        'created_at': created_at,
        'updated_at': created_at,
        'deleted_at': None
    },
    {
        'id': '7990ad79-9bbc-44f2-8cce-2e091faf370f',
        'parent_id': '233a2f62-64c6-4130-addf-eb2c62ced681',
        'type': ChatType.event.value,
        'external': {
            'title': 'Встреча первая',
            'description': 'Здесь студенты обсуждают',
            'datetime': (today.replace(hour=16) + timedelta(days=10)).strftime(dt_format),
            'duration': 3600,
            'location': '(56.831645, 60.607778)'
        },
        'created_at': created_at,
        'updated_at': created_at,
        'deleted_at': None
    },
    {
        'id': '9dc5fd35-1828-4c81-abc4-7fb96dd6c563',
        'parent_id': '233a2f62-64c6-4130-addf-eb2c62ced681',
        'type': ChatType.event.value,
        'external': {
            'title': 'Встреча вторая',
            'description': 'Здесь студенты обсуждают',
            'datetime': (today.replace(hour=16) - timedelta(days=10)).strftime(dt_format),
            'duration': 3600,
            'location': '(56.831645, 60.607778)'
        },
        'created_at': created_at,
        'updated_at': created_at,
        'deleted_at': None
    },
]

user_chats = [
    {'user_id': users[1]['id'], 'chat_id': chats[0]['id'], 'role': UserRole.admin.value},
    {'user_id': users[2]['id'], 'chat_id': chats[0]['id'], 'role': UserRole.moderator.value},
    {'user_id': users[3]['id'], 'chat_id': chats[0]['id'], 'role': UserRole.moderator.value},
    {'user_id': users[4]['id'], 'chat_id': chats[0]['id'], 'role': UserRole.user.value},
    {'user_id': users[5]['id'], 'chat_id': chats[0]['id'], 'role': UserRole.user.value},
    {'user_id': users[6]['id'], 'chat_id': chats[0]['id'], 'role': UserRole.user.value},
    {'user_id': users[7]['id'], 'chat_id': chats[0]['id'], 'role': UserRole.user.value},
    {'user_id': users[8]['id'], 'chat_id': chats[0]['id'], 'role': UserRole.user.value},
    {'user_id': users[9]['id'], 'chat_id': chats[0]['id'], 'role': UserRole.user.value},
    {'user_id': users[1]['id'], 'chat_id': chats[1]['id'], 'role': UserRole.user.value},
    {'user_id': users[2]['id'], 'chat_id': chats[1]['id'], 'role': UserRole.user.value},
    {'user_id': users[3]['id'], 'chat_id': chats[1]['id'], 'role': UserRole.moderator.value},
    # {'user_id': users[4]['id'], 'chat_id': chats[1]['id'], 'role': UserRole.user.value},
    # {'user_id': users[5]['id'], 'chat_id': chats[1]['id'], 'role': UserRole.user.value},
    {'user_id': users[6]['id'], 'chat_id': chats[1]['id'], 'role': UserRole.user.value},
    {'user_id': users[7]['id'], 'chat_id': chats[1]['id'], 'role': UserRole.moderator.value},
    {'user_id': users[8]['id'], 'chat_id': chats[1]['id'], 'role': UserRole.user.value},
    {'user_id': users[9]['id'], 'chat_id': chats[1]['id'], 'role': UserRole.admin.value},
    {'user_id': users[1]['id'], 'chat_id': chats[2]['id'], 'role': UserRole.user.value},
    {'user_id': users[2]['id'], 'chat_id': chats[2]['id'], 'role': UserRole.moderator.value},
    # {'user_id': users[3]['id'], 'chat_id': chats[2]['id'], 'role': UserRole.moderator.value},
    # {'user_id': users[4]['id'], 'chat_id': chats[2]['id'], 'role': UserRole.user.value},
    {'user_id': users[5]['id'], 'chat_id': chats[2]['id'], 'role': UserRole.user.value},
    {'user_id': users[6]['id'], 'chat_id': chats[2]['id'], 'role': UserRole.admin.value},
    # {'user_id': users[7]['id'], 'chat_id': chats[2]['id'], 'role': UserRole.user.value},
    {'user_id': users[8]['id'], 'chat_id': chats[2]['id'], 'role': UserRole.user.value},
    {'user_id': users[9]['id'], 'chat_id': chats[2]['id'], 'role': UserRole.user.value},
]
