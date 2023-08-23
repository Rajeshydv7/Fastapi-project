from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
router = APIRouter(
    tags=['blogs']
)

get_db = database.get_db

@router.get('/blog',response_model=list[schemas.ShowBlog])
def all(db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post('/blog',status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    new_blog = models.Blog(title=request.title, body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destory(id,db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return {'Done'}

@router.put('/blog{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id, request:schemas.Blog, db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    
    update_data = request.dict(exclude_unset=True)
    # note_query.filter(models.Note.id == noteId).update(update_data,
    #                                                   synchronize_session=False)
    blog.update(update_data)
    db.commit()
    return 'updated'


@router.get('/blog/{id}',status_code=200, response_model=schemas.ShowBlog)
def show(id, db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not avilable")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'detail': f"Blog with the id {id} is not avilable"}
    
    return blog

