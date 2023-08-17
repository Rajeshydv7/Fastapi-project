from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from . database import engine, SessionLocal
from sqlalchemy.orm import Session
app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog',status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destory(id,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return {'Done'}

@app.put('/blog{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id, request:schemas.Blog, db: Session = Depends(get_db)):
    # print(request)
    # import sys

    # sys.exit()
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    
    update_data = request.dict(exclude_unset=True)
    # note_query.filter(models.Note.id == noteId).update(update_data,
    #                                                    synchronize_session=False)
    blog.update(update_data)
    db.commit()
    # db.commit()
    # db.refresh(db_note)
    return 'updated'


@app.get('/blog')
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',status_code=200)
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not avilable")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'detail': f"Blog with the id {id} is not avilable"}
    
    return blog


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app",port=8000)