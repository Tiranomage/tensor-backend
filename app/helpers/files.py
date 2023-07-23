import os
import uuid
from http.client import REQUEST_ENTITY_TOO_LARGE

from fastapi import UploadFile, APIRouter, HTTPException, Depends

from app.auth import current_user
from app.config import app_settings
from app.models.models import User

files_router = APIRouter(tags=['current'])


@files_router.post("/files")
async def create_upload_files(
        files: list[UploadFile],
        user: User = Depends(current_user),
):
    result = []
    for file in files:
        try:
            if file.size > app_settings.MAX_FILE_SIZE:
                raise HTTPException(status_code=REQUEST_ENTITY_TOO_LARGE,
                                    detail=f'Maximum file size limit ({app_settings.MAX_FILE_SIZE} bytes) exceeded')

            _, extension = os.path.splitext(file.filename)
            static_filename = f'{user.id}_{str(uuid.uuid4())}{extension.lower()}'
            result.append(static_filename)

            static_location = os.path.join(app_settings.STATIC, static_filename)
            static_link = f'{app_settings.STATIC_LINK}/{static_filename}'
            with open(static_location, "wb+") as file_object:
                contents = await file.read()
                file_object.write(contents)

            result.append({
                'old': file.filename,
                'new': static_filename,
                'link': static_link
            })
        except Exception as error:
            result.append({
                'old': file.filename,
                'error': error
            })

    return result
