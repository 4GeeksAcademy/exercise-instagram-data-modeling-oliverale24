import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Comment(Base):
    __tablename__ = 'comment'
    comment_text = Column(String(50))
    author_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), primary_key=True, nullable=False)
    post = relationship('Post', back_populates='comments')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    comments = relationship('Comment', back_populates='post')
    comments = relationship('Media', back_populates='post')

class Follower(Base):
    __tablename__ = 'follower'
    user_from_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('user.id'), nullable=False)

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum)
    url = Column(String(50))
    post_id = Column(Integer, ForeignKey('post.id'), primary_key=True, nullable=False)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    firstname = Column(String(50))
    lastname = Column(String(50), nullable=False)
    email = Column(String(50), unique=True)
    followers = relationship('Follower', foreign_keys=[Follower.user_to_id])
    following = relationship('Follower', foreign_keys=[Follower.user_from_id])
    posts = relationship('Post', backref='user')
    author = relationship('Comment', foreign_keys=[Comment.author_id])

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
