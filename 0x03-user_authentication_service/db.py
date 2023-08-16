#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, password: str) -> User:
        """
        Add new user
        :param email: Unique User's email
        :type email: string
        :param password: User's login password
        :type password: string
        :return: User object
        :rtype: User
        """
        new_user = User(email=f"{email}", hashed_password=f"{password}")
        self._session.add(new_user)
        self.save()
        return new_user

    def save(self) -> None:
        """
            commits all changes of current database session
        """
        self._session.commit()

    def find_user_by(self, **kwargs) -> User:
        """
        Return exactly one result or raise an exception.
        :kwargs: key value pair
        :returns: User object
        :rtype: User
        """

        key = kwargs.keys()
        result = None
        # vars(User))
        user_keys = User.__dict__.keys()
        # print(key)
        key = list(key)[0]
        if key in list(user_keys):
            # if key == 'email':
            result = self._session.query(User).filter(
                getattr(User, key) == kwargs.get(f'{key}')).one()
            # elif key == 'id':
            #     result = self._session.query(User).filter(User.id == kwargs.get(f'{key}')).one()
        else:
            raise InvalidRequestError

        return result

    def update_user(self, id, **kwargs) -> None:
        """
       Updates User Instance Objects
        :param id: user_id
        :type id: integer
        :param kwargs: key Value pairs to be updated
        :type kwargs: dict
        :return: None
        :rtype: None
        """
        find_user = self.find_user_by(id=id)

        # Check if all keys in kwargs are in the class dictionary
        user_keys = set(User.__dict__.keys())
        update_keys = set(kwargs.keys())
        if not update_keys.issubset(user_keys):
            raise ValueError(
                "One or more keys in kwargs are not valid attributes of User.")

        # Update with new values
        for key, value in kwargs.items():
            setattr(find_user, key, value)

        self.save()
        return None
