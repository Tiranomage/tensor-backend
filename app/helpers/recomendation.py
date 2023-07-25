import uuid
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from app.auth import current_user
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_category import crud_user_tags
from app.crud.crud_user import crud_user
from app.helpers.tags import helper_update_user_tags
from app.models.db import get_async_session
from app.models.models import User

recomendations_router = APIRouter(prefix='/recomendations', tags=['recomendations'])

# todo добавить не только пользователей, но и чаты.
# todo убрать из списка пользователей тех, с кем была коммуникация.
@recomendations_router.get("/get_recomended_users", response_model=None)
async def get_recomended_users(
        offset: int = 0,
        limit: int = 1000,
        user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)): #-> list[User]:
    new_recomended_users = []

    # получаем теги текущего пользователя
    user_tags = (await db.scalars(user.tags.statement)).all()
    #print(user_tags)
    length_cur_user_tags = len(user_tags)
    set_cur_user_tags_ids_to_compare = set(tag.id for tag in user_tags)


    # # получаем всех пользователей (а ещё убрать пользователей с которыми уже есть личный чат)
    all_users_tags_dict = {}
    all_users = await crud_user.get_multi(db=db, offset=offset,
                                          limit=limit)

    # теги, складываем в словарь по пользователю
    for other_user in all_users:
        # чтобы в рекомендации случайно не попал сам пользователь
        if other_user.id != user.id:
            others_tags = (await db.scalars(other_user.tags.statement)).all()
            all_users_tags_dict[other_user.id] = others_tags


    # проходимся по словарю и для каждого пользователя считаем процент совместимости
    for other_user_id, other_tags_list in all_users_tags_dict.items():
        other_tags_set = set(tag.id for tag in other_tags_list)
        max_tag_count = max(length_cur_user_tags, len(other_tags_list))
        intersections = len(set_cur_user_tags_ids_to_compare.intersection(other_tags_set))
        percent = intersections/max_tag_count
        new_recomended_users.append((other_user_id, percent))

    # способ представления данных в new_recomended_users -> [(user_id:percent)]
    # сортируем по проценту
    new_recomended_users.sort(key=lambda x: x[1], reverse=True)

    # формируем список пользователей по их id
    result_list = [await crud_user.get(db=db,model_id=i[0]) for i in new_recomended_users]
    return result_list

# todo написать метод для возвращения событий
# @recomendations_router.get("/get_recomended_events")
# def sort_events_by_recomendations(user:list, events:list[dict]):
#     matches = 0
#     new_events = []
#     for event in events:
#          u_set = set(user)
#          event_tags = event["tags"]
#          event_tag_count = len(event_tags)
#          intersections = len(u_set.intersection(set(event_tags)))
#          percent = intersections/event_tag_count
#          new_event = event
#          new_event.update({"percent":percent})
#          new_events.append(new_event)
#
#     return sorted(new_events,key=lambda x: x["percent"],reverse=True)



# #временный метод для обновления тегов пользователей
# from app.shemas import category as search_schemas
# @recomendations_router.post("/tags/{user_id}", response_model=list[search_schemas.UserTags])
# async def update_user_tags(
#         tags: list[str],  # list[search_schemas.TagCreate],
#         user_id: uuid.UUID,
#         session: AsyncSession = Depends(get_async_session)
# ):
#     user = await crud_user.get(db=session, model_id=user_id)
#     return await helper_update_user_tags(tags, user, session)