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
