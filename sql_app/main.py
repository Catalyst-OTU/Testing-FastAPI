from typing import List
from fastapi import Depends, FastAPI, HTTPException, status,File, UploadFile
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
import  cloudinary
import cloudinary.uploader
import shutil
from passlib.context import CryptContext
from sql_app.crud import *
from sql_app.schemas import User
from sql_app.database import *


database = Database()
engine = database.get_db_connection()
db = database.get_db_session(engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = username
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db),form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/users/")
def create_user(
    user: UserCreate, db: Session = Depends(get_db)
):
    return create_user(db=db, user=user)

@app.post("/posts/",status_code=status.HTTP_201_CREATED)
def create_post(
    title:str,body:str,file: UploadFile = File(...), db: Session = Depends(get_db),current_user: User = Depends(get_current_user)
):
    user_id=current_user.id

    result = cloudinary.uploader.upload(file.file)
    url = result.get("url")

    return create_post(db=db,user_id=user_id,title=title,body=body,url=url)

@app.get("/posts/")
def post_list(db: Session = Depends(get_db)):
    return post_list(db=db)

@app.post("/posts/{post_id}/comment",response_model=CommentList)
def create_comment(
        comment:CommentBase ,post_id:int,db:Session = Depends(get_db)
):
    return  create_comment(db=db,post_id=post_id,comment=comment)

@app.get("/posts/{post_id}")
def post_detail(post_id:int,db: Session = Depends(get_db)):
    post =get_post(db=db, id=post_id)
    comment = db.query(Comment).filter(Comment.post_id == post_id)
    active_comment = comment.filter(Comment.is_active == True).all()

    if post is None:
        raise HTTPException(status_code=404,detail="post does not exist")
    return {"post":post,"active_comment":active_comment}


# @app.post("/items/", response_model=Item)
# def create_item_for_user(
#     item: ItemCreate, db: Session = Depends(get_db)
# ):
#     return create_user_item(db=db, item=item)
#
#
# @app.get("/items/", response_model=List[Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = get_items(db, skip=skip, limit=limit)
#     return items