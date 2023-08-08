#!/usr/bin/env python3
"""
Implements Basic Authentication that uses
username:password
"""
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    Basic Authentication class that uses Base64 encoding
    """

    def __init__(self) -> None:
        """Call to parent class to prevent overriding of initialization function"""
        super().__init__()

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts a base64 encode('username:password') that follows Basic and returns"""
        if not authorization_header:
            return None
        if type(authorization_header) not in [str]:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ", 1)[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes a base64 encoded string and returns a utf-8 compatible string"""
        decoded_string = None
        if not base64_authorization_header:
            return None
        if type(base64_authorization_header) not in [str]:
            return None
        try:
            decoded_string = base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except BaseException:
            return None
        else:
            return decoded_string

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """extracts and returns username & password delimited by a colon"""
        if not decoded_base64_authorization_header:
            return None, None
        if type(decoded_base64_authorization_header) not in [str]:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        username, password = decoded_base64_authorization_header.split(':', 1)
        return username, password

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """checks that username exists and that password is valid then returns the User object to caller"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Overload Auth and retrieves the User instance for a request
        and performs decoding of base64 encoded string in the header
        extractions username and password
         checks validity of the username
          checks validity of the password and performs matching
           finally returns  user Object to calling Function"""
        header = self.authorization_header(request)

        if not header:
            return None

        b64_header = self.extract_base64_authorization_header(header)

        if not b64_header:
            return None

        decoded = self.decode_base64_authorization_header(b64_header)

        if not decoded:
            return None

        email, pwd = self.extract_user_credentials(decoded)

        if not email or not pwd:
            return None

        return self.user_object_from_credentials(email, pwd)
