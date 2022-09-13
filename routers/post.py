from fastapi import HTTPException, status, UploadFile, File
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from auth.oauth2 import get_current_user
from db.database import get_db
from .schemas import PostDisplay, PostBase
from db import db_post
from typing import List

from datetime import datetime
import shutil

from routers.schemas import UserAuth


router = APIRouter(
    prefix="/post",
    tags=['post']
)

images_url_types = ['absolute','relative']

@router.post('/', response_model=PostDisplay)
def create(request:PostBase, db:Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    if request.image_url_type  not in images_url_types:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='image url type can only be absolute or relative')
    return db_post.create(request, db)

@router.get('/', response_model=List[PostDisplay])
def getall(db:Session = Depends(get_db)):
    return db_post.get_all(db)


@router.post('/images/')
def upload_image(image:UploadFile = File(), current_user: UserAuth = Depends(get_current_user)):
    time = datetime.now().strftime("%d%m%Y%H%M%S")
    filename = time.join(image.filename.rsplit('.',1))
    path = f'images/{filename}'

    with open(path,'w+b') as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return {'filename': path}


@router.delete('/{id}/')
def delete(id:int, db:Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_post.delete_post(id,db,current_user.id)