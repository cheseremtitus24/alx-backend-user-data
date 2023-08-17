User Authentication Service.
In the industry, you should not implement your own authentication system and use a module or framework 
that doing it for you (like in Python-Flask: [Flask-User]{https://flask-user.readthedocs.io/en/latest/}). 
Here, for the learning purpose, we will walk through each step of this 
mechanism to understand it by doing.

Create new User:
curl -XPOST localhost:5000/users -d 'email=bob@bob.com' -d 'password=mySuperPwd'

Set Cookies:
curl -XPOST localhost:5000/sessions -d 'email=bob@bob.com' -d 'password=mySuperPwd' -v 

send curl request with cookies set: 
curl --cookie "session_id=e60637cf-8d00-45d1-82bd-c9030ffa3e77" -XDELETE localhost:5000/sessions -v

# request Password Reset
curl -XPOST localhost:5000/reset_password -d 'email=bob@bob.com'
{
  "email": "bob@bob.com", 
  "reset_token": "62761ee4-91da-4a67-aab3-b698a051196f"
}

# Use the token to reset the password by setting a new one
curl -XPUT localhost:5000/reset_password -d 'email=bob@bob.com' -d 'new_password=newpwd' -d 'reset_token=1bcb731a-f288-4cc6-a438-09b64c6c34bf' -v 

