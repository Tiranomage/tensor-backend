import uvicorn

from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.auth import include_auth_router, current_active_user
from app.config import app_settings
from app.models.models import User, Category, Chat

from app.routers.chat_routers import chat_router, message_router
from app.routers.websocket_router import ws_router
from app.routers.category_router import category_router, tag_router


app = FastAPI(
    title='API Template'
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роуты из внешних источников
include_auth_router(app)

app.include_router(chat_router)
app.include_router(message_router)
app.include_router(category_router)
app.include_router(tag_router)
app.include_router(ws_router)


# @app.on_event("startup")
# async def startup():
#     await database.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )


@app.head("/")
def head_root():
    return {"Hello": "World", "Method": "head"}


@app.get("/")
def get_root():
    return {"Hello": "World", "Method": "get"}


@app.post("/")
def post_root():
    return {"Hello": "World", "Method": "post"}


@app.get("/current-user")
def protected_route(user: User = Depends(current_active_user)):
    return {user}


if __name__ == "__main__":
    # hero_1 = User.validate({'username':"Deadpond", 'email':"Pedro@Parqueador.ru"})
    # hero_2 = User(username="Spider-Boy", email="Pedro@Parqueador.ru")
    # hero_3 = User(username="Rusty-Man", secret_name="Tommy Sharp", age=48)
    #
    # print(hero_1.email)
    # print(hero_1)
    # print(hero_2)
    # print(hero_3)

    uvicorn.run("app.main:app", host=app_settings.HOST, port=app_settings.PORT, reload=True)
