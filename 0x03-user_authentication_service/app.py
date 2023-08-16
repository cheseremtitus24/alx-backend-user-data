#!/usr/bin/env python3
"""
Main flask app with routes for a custom
user authentication System.
# secure by using sessions atop cookies to
make it more secure.
"""
from flask import Flask, jsonify, request, abort, make_response, redirect, url_for
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def index():
    """
    responds with a message
    :return: Dict
    :rtype: Json
    """
    data = {"message": "Bienvenue"}
    return jsonify(data)


@app.route('/users', methods=['POST'])
def add_user():
    """
    This is the Add a new User route endpoint.
    curl -XPOST localhost:5000/users -d 'email=bob@bob.com' -d 'password=mySuperPwd'

   {"email":f"{email}", "message":"user created"}

    :return: json dictionary
    :rtype: dict
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None:
        abort(400, 'Missing email')
    if password is None:
        abort(400, 'Missing password')
    try:

        user = AUTH.register_user(email, password)
        # print("successfully created a new user!")
    except ValueError as err:
        data = {"message": "email already registered"}
        return jsonify(data), 400
        # print("could not create a new user: {}".format(err))
    else:
        data = {"email": f"{email}", "message": "user created"}
        return jsonify(data), 201


@app.route('/sessions', methods=['POST'])
def login():
    """
    This is the Login route endpoint.
    curl -XPOST localhost:5000/sessions -d 'email=bob@bob.com' -d 'password=mySuperPwd' -v
    -- sets cookie and prints it.

    :return: json dictionary
    :rtype: dict
    """
    email = request.form.get('email')
    password = request.form.get('password')
    session_id = None
    data = dict()

    if email is None:
        abort(400, 'Missing email')
    if password is None:
        abort(400, 'Missing password')
    try:
        # check that authentication is valid
        if AUTH.valid_login(email, password):
            # create the User Session_id
            session_id = AUTH.create_session(email)
        else:
            # Failed to Authenticate
            abort(401)
    except BaseException as e:
        abort(500)
        # print("could not create a new user: {}".format(err))
    else:
        # nothing went wrong: Lets set the cookie in the response
        if session_id:
            data = {"email": f"{email}", "message": "logged in"}
            resp = make_response(jsonify(data))
            resp.set_cookie('session_id', f'{session_id}')
            return resp


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    This is the Logout route endpoint.
    Destroys set cookies then redirects to '/'
    # Use cookie retrieved from the Login command:
    curl --cookie "session_id=e60637cf-8d00-45d1-82bd-c9030ffa3e77" -XDELETE localhost:5000/sessions -v

    :return: json dictionary
    :rtype: dict
    """
    session_id = request.cookies.get('session_id')

    # check that authentication is valid
    user_obj = AUTH.get_user_from_session_id(session_id)
    # print(user_obj)
    if user_obj is None:
        # User with specified session_id does not exist
        abort(403)

    else:
        # Valid User Object has been Retrieved therefore lets destroy the
        # session
        AUTH.destroy_session(user_obj.id)
        # Redirect use to '/'
        return redirect(url_for('index'))


@app.route('/profile', methods=['GET'])
def profile():
    """
    This is the profile route endpoint.
    Retrieves set cookies then returns
    User's email attached to this session Cookie

    curl -XGET localhost:5000/profile --cookie "session_id=75c89af8-1729-44d9-a592-41b5e59de9a1"
    {"email": "bob@bob.com"}

    :return: json dictionary
    :rtype: dict
    """
    data = dict()
    session_id = request.cookies.get('session_id')

    if session_id is None:
        abort(400, 'Missing session_id')

    # check that authentication is valid
    user_obj = AUTH.get_user_from_session_id(session_id)
    if user_obj is None:
        # User with specified session_id does not exist
        abort(403)

    else:
        # No matching user found
        data = {"email": f"{user_obj.email}"}
        return jsonify(data), 200


@app.route('/reset_password', methods=['POST'])
def reset_password():
    """
    Sets a reset_cookie from reverse email check to retrieve
    current DB User.
    reset_cookie will enable for user password resets

    Sets a reset cookie and displays it in the response

   curl -XPOST localhost:5000/sessions -d 'email=bob@bob.com' -d 'password=mySuperPwd' -v
    -- sets cookie and prints it.
    {"email": f"{email}", "reset_token": f"{reset_token}"}

    :return: json
    :rtype: dict
    """
    email = request.form.get('email')
    data = dict()

    if email is None:
        abort(400, 'Missing email')
    valid_session = AUTH.create_session(email)
    if valid_session is None:
        # email is not registered therefore abort
        abort(403)
    else:
        # generate token
        reset_token = AUTH.get_reset_password_token(email)
        if reset_token:
            data = {"email": f"{email}", "reset_token": f"{reset_token}"}
        else:
            abort(500, "Failed to generate reset token")
    return jsonify(data)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """
    Uses form post reset_token to be used to update the user password
   curl -XPUT localhost:5000/reset_password -d 'email=bob@bob.com' -d 'new_password=mySuperPwd' -d 'reset_token=75c89af8-1729-44d9-a592-41b5e59de9a1' -v
   {"email": f"{email}", "message": "Password updated"}
    :return:
    :rtype:
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    data = dict()

    if email is None:
        abort(400, 'Missing email')
    if reset_token is None:
        abort(400, 'Missing reset_token')
    if new_password is None:
        abort(400, 'Missing new_password')
    try:
        update_result = AUTH.update_password(
            reset_token=reset_token, password=new_password)
        data = {"email": f"{email}", "message": "Password updated"}
    except ValueError as e:
        # reset token not found
        abort(403)
    else:
        # update was successfull
        return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
