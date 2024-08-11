import jwt
from core import mail
from flask_mail import Message
from settings import settings
from flask import request
import requests as http
from jwt.exceptions import PyJWTError
from flask import g

class JWT:

    key = "Book_Store"
    algorithm = "HS256"

    @classmethod
    def to_encode(cls,payload):
        return jwt.encode(payload=payload,key=cls.key,algorithm=cls.algorithm)
    
    @classmethod
    def to_decode(cls,enocded,aud):
        return jwt.decode(enocded,key=cls.key,algorithms=[cls.algorithm],audience=aud)
    


def send_mail(username,email,token,context):
    msg=Message(f"Hello {username}", sender=f"{settings.sender}" , recipients=[email])
    body={"register":"Welcome to Book_Store.\n Pls click on the link to verify {url}{token}".format(
        url="http://127.0.0.1:5000/api/user?token=",token=token),
          "reset":"Welcome to Book_Store.\n Pls click on the link to  reset your password  {url}{token}".format(
        url="http://127.0.0.1:5000/api/?token=",token=token)}
    msg.body=body[context].format(token=token)
    mail.send(msg)


def authorize_user(function):
    """
    This function is a decorator that is used to authorize the user before they 
    access any of the resources in the system.
    """
    def wrapper(*args, **kwargs):
        """
        This function is a wrapper that is used to wrap the original function and add authorization functionality.
        """
        try:
            token = request.headers.get('Authorization')
            if not token:
                return {'message': 'Token not found','status': 404}, 404
            payload = JWT.to_decode(token, aud='login')
            response = http.get(f'http://127.0.0.1:5000/getUser?user_id={payload.get('userid')}')
            if response.status_code >= 400:
                return {}, 401
            user = response.json()
            g.user = user
            if request.method in ['POST', 'PUT','PATCH']:
                request.json.update(userid=user['id'])
            else:
                kwargs.update(userid=user['id'])
        except PyJWTError:
            return {'msg': 'Invalid Token','status': 401}, 401
        except Exception as e:
            return {'msg' : str(e), 'status' :500}
        return function(*args, **kwargs)
    wrapper.__name__ == function.__name__
    return wrapper

