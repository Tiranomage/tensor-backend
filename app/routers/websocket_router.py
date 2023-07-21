"""
Подключение к вебсокету происходит по пути "ws://localhost/websocket/?token="

Тип данных для message - json.
{
    "text": str,
    "user_id": uuid.UUID,
    "chat_id": uuid.UUID,
    "external": dict|None
}
"""
import jwt
import uuid

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocket
from fastapi.websockets import WebSocketDisconnect
from sqlalchemy import select

from app.config import app_settings
from app.models.db import async_session_maker as async_session
from app.models.models import UserChats

# html = """
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Chat</title>
#     </head>
#     <body>
#         <h1>WebSocket Chat</h1>
#         <form action="" onsubmit="sendMessage(event)">
#             <label>Chat ID: <input type="text" id="chatId" autocomplete="off" value="3e039cb0-2e43-466d-8699-a2d61d85a765"/></label>
#             <button onclick="connect(event)">Connect</button>
#             <hr>
#             <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
#             <button>Send</button>
#         </form>
#         <ul id='messages'>
#         </ul>
#         <script>
#
#         var ws = null;
#             function connect(event) {
#                 var token = localStorage.getItem("token")
#                 ws = new WebSocket("ws://localhost:8080/websocket/?token=" + token);
#                 ws.onmessage = function(event) {
#                     var messages = document.getElementById('messages')
#                     var message = document.createElement('li')
#                     var content = document.createTextNode(event.data)
#                     message.appendChild(content)
#                     messages.appendChild(message)
#                 };
#                 event.preventDefault()
#             }
#             function sendMessage(event) {
#                 var input = localStorage.getItem("message")
#                 ws.send(input)
#                 event.preventDefault()
#             }
#         </script>
#     </body>
# </html>
# """

ws_router = APIRouter(prefix="/websocket", tags=["websocket"])


class ConnectionManager:
    def __init__(self):
        # вид хранения {user_id:websocket}
        self.active_connections: dict[uuid.UUID:WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: uuid.UUID):
        await websocket.accept()
        self.active_connections.update({user_id: websocket})

    def disconnect(self, websocket: WebSocket):
        for user_id, user_socket in self.active_connections.items():
            if websocket in user_socket:
                del self.active_connections[user_id]

    async def broadcast(self, text: str, from_user_id: uuid.UUID, chat_id: uuid.UUID, external:dict|None, db_users: list):
        # формируем json
        message = {
            "text": text,
            "user_id": from_user_id,
            "chat_id": chat_id,
            "external": external
        }

        # приводим к одинаковому виду
        # т.к. db_users возвращает list[UUID('dda273...')], а active_connections.keys list['dda273...']
        # иначе intersection возвращает пустой массив
        db_users_set = set(map(lambda x: str(x), db_users))

        # получаем set пересечений
        active_users_in_chat = db_users_set.intersection(set(self.active_connections.keys()))

        for user_id in list(active_users_in_chat):
            # отправителю сообщение по сокету не шлём
            if from_user_id != user_id:
                user_socket = self.active_connections[user_id]
                await user_socket.send_json(message)
                #print(f"message: {message} was delivered to {user_id}")


manager = ConnectionManager()


# @ws_router.get("/")
# async def get():
#     return HTMLResponse(html)


@ws_router.websocket("/")
async def websocket_endpoint(
        websocket: WebSocket,
        token: str | None,
):
    """
    data: MessageCreate

    """
    # user = {"email": "user@example.com", "password": "string"}

    data_decoded = jwt.decode(jwt=token, key=app_settings.JWT_SECRET, audience=["fastapi-users:auth"],
                              algorithms=['HS256'])

    expire_on = data_decoded['exp']
    user_id = data_decoded['sub']

    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()
            try:

                async with async_session() as session:
                    # получаем список пользователей по chat id
                    db_users_id = await session.scalars(
                        select(UserChats.user_id)
                        .where(UserChats.chat_id == data['chat_id'])
                    )
                    db_users = list(db_users_id)

                    # оформляем рассылку
                    if 'external' in data.keys():
                        await manager.broadcast(
                            text=data['text'],
                            chat_id=data['chat_id'],
                            from_user_id=user_id,
                            db_users=db_users,
                            external=data['external']
                        )
                    else:
                        await manager.broadcast(
                            text=data['text'],
                            chat_id=data['chat_id'],
                            from_user_id=user_id,
                            db_users=db_users,
                            external=None
                        )

            except Exception as e:
                print(e, 'ERROR something wrong with data or broadcast')

    except WebSocketDisconnect:
        manager.disconnect(websocket)
