#!/usr/bin/env python3
"""Main module."""
import requests


url = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """Test register_user."""
    data = {"email": email, "password": password}
    response = requests.post(f'{url}/users', data=data)
    message = {"email": email, "message": "user created"}

    assert response.status_code == 200
    assert response.json() == message


def log_in_wrong_password(email: str, password: str) -> None:
    """Test log_in_wrong_password."""
    data = {"email": email, "password": password}
    response = requests.post(f'{url}/sessions', data=data)

    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test log_in."""
    data = {"email": email, "password": password}
    response = requests.post(f'{url}/sessions', data=data)
    message = {"email": email, "message": "logged in"}

    # print(response.status_code)
    assert response.status_code == 200
    assert response.json() == message

    session_id = response.cookies.get("session_id")

    return session_id


def profile_unlogged() -> None:
    """Test profile_unlogged."""
    cookies = {"session_id": ""}
    response = requests.get(f'{url}/profile', cookies=cookies)

    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test profile_logged."""
    cookies = {"session_id": session_id}
    response = requests.get(f'{url}/profile', cookies=cookies)
    message = {"email": EMAIL}

    assert response.status_code == 200
    assert response.json() == message


def log_out(session_id: str) -> None:
    """Test log_out."""
    cookies = {"session_id": session_id}
    response = requests.delete(f'{url}/sessions', cookies=cookies)
    message = {"message": "Bienvenue"}

    assert response.status_code == 200
    assert response.json() == message


def reset_password_token(email: str) -> str:
    """Test reset_password_token."""
    data = {"email": email}
    response = requests.post(f'{url}/reset_password', data=data)
    reset_token = response.json().get("reset_token")
    message = {"email": email, "reset_token": reset_token}

    assert response.status_code == 200
    assert response.json() == message

    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test update_password."""
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password}
    response = requests.put(f'{url}/reset_password', data=data)
    message = {"email": email, "message": "Password updated"}

    assert response.status_code == 200
    assert response.json() == message


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    # log_in(EMAIL, NEW_PASSWD)
