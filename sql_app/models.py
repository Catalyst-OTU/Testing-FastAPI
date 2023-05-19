from sqlalchemy import Boolean, Column, ForeignKey, Integer,String,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType,URLType
import datetime
import sqlalchemy as db
from sql_app.database import *


class User(Base):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(DateTime,default=datetime.datetime.utcnow)
    email = db.Column(EmailType, unique=True)
    username = db.Column(db.String(255), nullable=True)
    hashed_password = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(255), nullable=True)
    #is_active = db.Column(Boolean,default=True)

    post = relationship("Post", back_populates="owner")

class Post(Base):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(DateTime,default=datetime.datetime.utcnow)
    is_active = db.Column(Boolean, default=True, nullable=True)
    title = db.Column(db.String(255), nullable=True)
    url = db.Column(URLType, nullable=True)
    body = db.Column(db.String(255), nullable=True)
    owner_id = db.Column(db.Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="post")
    post_comment = relationship("Comment", back_populates="post_related")

class   Comment(Base):
    __tablename__ ="comments"
    id = db.Column(db.Integer,primary_key=True)
    created_date = db.Column(DateTime,default=datetime.datetime.utcnow)
    is_active = db.Column(Boolean,default=True, nullable=True)
    name = db.Column(db.String(255), nullable=True)
    email = db.Column(EmailType, nullable=True)
    body= db.Column(db.String(255), nullable=True)
    post_id = db.Column(db.Integer,ForeignKey("posts.id"))

    post_related = relationship("Post" , back_populates="post_comment")