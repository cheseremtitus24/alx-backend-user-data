#!/usr/bin/env python3
"""
Implements the Authentication Base Class
"""
from typing import List, TypeVar
from flask import request
import re


class Auth:
    """
    Base Class for Authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """checks that path is not in excluded paths so that it can
        enforce authentication as a requirement
        """
        if not path or not excluded_paths:
            return True
        if path in excluded_paths:
            return False
        if path + '/' in excluded_paths:
            return False
        pattern = r"^(?:[\w\-_./]+/)*[\w\-_.]+$"
        match = re.match(pattern, path)
        if match:
            for excluded_path in excluded_paths:
                if re.match(excluded_path, path):
                    return False
                return True
        return True

    def authorization_header(self, request=None) -> str:
        """Returns the authorization header that was received in request"""
        if not request:
            return None

        # Returns the value of the header request Authorization
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Base function of how to handle user authentication"""
        return None
