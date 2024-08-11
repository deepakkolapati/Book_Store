from users import db
from passlib.hash import pbkdf2_sha256
from core.utils import JWT
from datetime import datetime,timedelta

class Users(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(15),nullable=False,unique=True)
    email=db.Column(db.String(255),nullable=False,unique=True)
    password=db.Column(db.String(255),nullable=False)
    issuperuser=db.Column(db.Boolean,default=False)
    isverified=db.Column(db.Boolean,default=False)

    @property
    def json(self):
        return {
            'id':self.id,
            'username':self.username,
            'email':self.email,
            'issuperuser':self.issuperuser,
            'isverified':self.isverified
        }
    
    def __init__(self,username,email,password,issuperuser):
        self.username = username
        self.email = email
        self.password = pbkdf2_sha256.hash(password)
        self.issuperuser = issuperuser
       
        

    def verify_password(self,raw_password):
        return pbkdf2_sha256.verify(raw_password, self.password)
    

    def token(self,aud=None,exp=15):
        payload={"userid":self.id,"exp": datetime.utcnow() + timedelta(minutes=exp)}
        if aud:
            payload.update({"aud":aud})
        return JWT.to_encode(payload)

    def set_password(self,value):
        self.password=pbkdf2_sha256.hash(value)
        

