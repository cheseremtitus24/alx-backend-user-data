#!/usr/bin/env python3
"""
Authentication module that performs secure
hashing of passwords using the bcrypt module
reset of password & Update of a Password, Session
handling using a primitive cookie setting.

requires bcrypt installed with :
pip install bcrypt
"""
import base64
import binascii
import uuid
import bcrypt
from sqlalchemy.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    Securely Hashes a Plain text password
    :param password: password to be hashed
    :type password: string
    :return: hashed password
    :rtype: bytes
    """
    salt = bcrypt.gensalt()
    bytes_hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return bytes_hashed_password


def _generate_uuid() -> str:
    """
    Generated Unique Byte string
    :return: unique string representation
    :rtype: string
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize Auth class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Creates a new User
        :param email: user's email
        :type email: string
        :param password: login password to be hashed
        :type password: string
        :return: User object
        :rtype: Obj
        """
        # raise ValueError if user's email already exists
        try:
            # Raises ``sqlalchemy.orm.exc.NoResultFound`` if the query selects
            #         no rows.
            result = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound as e:
            # Clear to register a new User
            # hash their password
            hashed_pwd = _hash_password(password)
            # print(type(hashed_pwd))
            string_hashed_password = hashed_pwd.decode('utf-8')
            # print(type(string_hashed_password))
            new_user = self._db.add_user(email, string_hashed_password)
            return new_user


    def valid_login(self, email: str, password: str) -> bool:
        """
        Verifies for Correct Password for auth
        :param email: username
        :type email: string
        :param password: hashed password
        :type password: string
        :return: true on success else false
        :rtype: bool
        """
        retval = False
        # Find User Using email
        try:
            # Raises ``sqlalchemy.orm.exc.NoResultFound`` if the query selects
            #         no rows.
            result = self._db.find_user_by(email=email)
        except NoResultFound as e:
            # User not found
            return retval
        else:
            # User Found, Verify that password matches
            stored_hashed_password = result.hashed_password
            # print(type(stored_hashed_password))
            hashed_password_as_bytes = stored_hashed_password.encode('utf-8')
            # print(type(hashed_password_as_bytes))
            if bcrypt.checkpw(
                    password.encode('utf-8'),
                    hashed_password_as_bytes):
                retval = True
                return retval
            else:
                # Password Does not Match or is Invalid
                return retval
        return retval

    def create_session(self, email: str) -> str:
        """
        creates a uniquely generated session string then
         updates user's object instance

        :param email: user's login email
        :type email: string
        :return: generated session_id
        :rtype: string
        """
        session_id = None
        # Find User Using email
        try:
            # Raises ``sqlalchemy.orm.exc.NoResultFound`` if the query selects
            #         no rows.
            result = self._db.find_user_by(email=email)
        except NoResultFound as e:
            # User not found
            return session_id
        else:
            # User Found, Generate user's session ID
            # Update User's session_id
            try:
                session_id = _generate_uuid()
                self._db.update_user(result.id, session_id=session_id)
            except ValueError as e:
                return session_id
        return session_id

    def get_user_from_session_id(self, session_id):
        """
        Gets User Object
        :param session_id:
        :type session_id:
        :return:
        :rtype:
        """
        retval = None
        if not session_id:
            # Handle case when session_id is None
            return retval

        try:
            # Raises ``sqlalchemy.orm.exc.NoResultFound`` if the query selects
            #         no rows.
            result = self._db.find_user_by(session_id=session_id)
        except NoResultFound as e:
            # User not found
            return retval
        else:
            # User Found, Return User Object
            return result

    def destroy_session(self, user_id: int) -> None:
        """
        Updates the session_id field of User object by setting it to None
        :param user_id: User_id
        :type user_id: integer
        :return: Nothing
        :rtype: None
        """
        session_id = None
        # Find User Using email
        try:
            # Raises ``sqlalchemy.orm.exc.NoResultFound`` if the query selects
            #         no rows.
            result = self._db.find_user_by(id=user_id)
        except NoResultFound as e:
            # User not found
            # raise NoResultFound
            return session_id
        else:
            # User Found,
            # Update User's session_id to None
            try:
                self._db.update_user(result.id, session_id=session_id)
            except ValueError as e:
                return session_id
        return session_id

    def get_reset_password_token(self, email: str) -> str:
        """
        Retrieves user by email then generates a reset token
        and updates user object with generated token

        :param email: unique user's email
        :type email: string
        :return: generated token
        :rtype: string
        """
        # raise ValueError if user's email already exists
        reset_token_uuid = ""
        try:
            # Raises ``sqlalchemy.orm.exc.NoResultFound`` if the query selects
            #         no rows.
            result = self._db.find_user_by(email=email)
        except NoResultFound as e:
            # User Does not Exist Raise a Value Error
            raise ValueError(f"User {email} does not exist")
        else:
            # No error Reported.
            if result:
                # User Exists therefore lets generate a UUID
                reset_token_uuid = _generate_uuid()
                # Update the Use's reset_token
                self._db.update_user(result.id, reset_token=reset_token_uuid)
        # return the generated token to calling function
        return reset_token_uuid

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Uses the saved instance reset token to reset/update user's
        forgotten Password

        :param reset_token: required token to validate for legin pswd reset
        :type reset_token: string
        :param password: New password to set
        :type password:
        :return:
        :rtype:
        """
        if not reset_token or not password:
            # Handle case when reset_token or password is  None
            raise ValueError()
        try:
            # Raises ``sqlalchemy.orm.exc.NoResultFound`` if the query selects
            #         no rows.
            result = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound as e:
            # User not found
            raise ValueError("reset_token not found")
        else:
            # User Object found
            hashed_password = _hash_password(password)
            # Update user's hashed password
            self._db.update_user(result.id, password=hashed_password)
            # set reset_token to None
            self._db.update_user(result.id, reset_token=None)
