#!/usr/bin/env python3
"""
Defines a User Model with its
object attributes.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    User Class
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=True)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self):
        """
        prints object representation of User Object
        """
        return "<User(email='%s', session_id='%s', reset_token='%s')>" % (
            self.email, self.session_id, self.reset_token)
