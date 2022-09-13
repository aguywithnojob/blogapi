from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from routers.schemas import PostBase
from .models import DbPost
from datetime import datetime

def create(request: PostBase, db:Session):
    new_post = DbPost(
        image_url = request.image_url,
        image_url_type = request.image_url_type,
        caption = request.caption,
        timestamp = datetime.now(),
        user_id = request.creator_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_all(db:Session):
    print('QUEYRRYR ==== >', db.query(DbPost).all())
    return db.query(DbPost).all()

def delete_post(id:int, db: Session, user_id:int):
    post = db.query(DbPost).filter(DbPost.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} not found.')
    
    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Only post creator can delete it.')

    db.delete(post)
    db.commit()
    return "Ok"