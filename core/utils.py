import jwt
from core import mail
from flask_mail import Message
from settings import settings

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
