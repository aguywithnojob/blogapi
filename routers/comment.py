from webbrowser import get
from fastapi import Depends, APIRouter
from db.database import get_db
from .schemas import CommentBase, UserAuth
from sqlalchemy.orm.session import Session
from db import db_comments
from typing import List
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/comment',
    tags=['comment']
)

@router.post('/')
def create(request: CommentBase, db: Session=Depends(get_db), current_user: UserAuth = Depends(get_current_user) ):
    return db_comments.create(request, db)

@router.get('post/{post_id}/')
def get_comment_by_post_id(post_id:int ,db:Session = Depends(get_db)):
    return db_comments.get_all(post_id, db)