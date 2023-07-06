import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.auth import include_auth_router, fastapi_users
from app.config import BACK_HOST, BACK_PORT
from app.models.models import User


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

current_user = fastapi_users.current_user()


@app.head("/")
def head_root():
    return {"Hello": "World", "Method": "head"}


@app.get("/")
def get_root():
    return {"Hello": "World", "Method": "get"}


@app.post("/")
def post_root(ddd):
    return {"Hello": "World", "Method": "post"}


@app.get("/current-user")
def protected_route(user: User = Depends(current_user)):
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

    uvicorn.run("app.main:app", host=BACK_HOST, port=BACK_PORT, reload=True)
