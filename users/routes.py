from users import app, db
from flask_restx import Api, Resource, fields
from flask import request
from schemas.user_schema import UserSchema,UserNameSchema,UserPasswordSchema
from users.models import Users
from sqlalchemy.exc import IntegrityError
from core.utils import JWT,send_mail
from jwt import PyJWTError


api=Api(app=app, prefix = "/api", title = 'Book_User', doc = "/docs",default="Book",default_label="User")

@api.route("/user")
class RegisterApi(Resource):
    @api.expect(api.model('register',{'username':fields.String(),'email':fields.String(),
                          "password":fields.String(),"superkey":fields.String(required=False) }))
    def post(self):
        try:
            serializer=UserSchema(**request.json)
            data=serializer.model_dump()
            data["issuperuser"]=data.pop("superkey")
            user=Users(**data)
            db.session.add(user)
            db.session.commit()
            token=user.token('register',45)
            send_mail(user.username,user.email,token,"register")
            return {"message": "User Registered Successfully", "status": 201, "data": user.json,"token":token},201
        except ValueError as e:
            return {"message": str(e), "status": 400},400
        except IntegrityError as e:
            return {"message": "Username or email already exists", "status": 409},409
        except Exception as e:
            return {"message": str(e), "status": 500},500
    
    @api.doc(params={"token": "Jwt token to verify user"})
    def get(self):
        try:
            token = request.args.get("token")
            if not token:
                return {'message': 'Token not found', 'status': 404},404
            decoded=JWT.to_decode(token,'register')
            userid=decoded["userid"]
            user=Users.query.filter_by(id=userid).first()
            if not user:
                return {'message': 'User not found','status': 404},404
            user.isverified=True
            db.session.commit()
            return {"message": "User Verified Successfully", "status": 200},200
        except PyJWTError :
            return {"message": "Invalid Token", "status": 401}, 401
        except Exception as e:
            return {"message": str(e), "status": 500},500


@api.route("/login")
class LoginApi(Resource):
    @api.expect(api.model('login',{'username':fields.String(), "password":fields.String()}))
    def get(self):
        try:
            data = request.get_json()
            serializer = UserNameSchema(username=data["username"])
            user=Users.query.filter_by(username=data["username"]).first()
            if user and user.verify_password(data["password"]):
                token=user.token('login',45)
                return {"message": "Login Successful", "status": 200, "data": user.json,"token":token},200
            return {"message":"Username or Password is incorrect","status":401},401

        except ValueError as e:
            return {"message": "Username must contain minumum length of 3 and maximum length of 9", "status": 400},400
        
        except Exception as e:
            return {"message": str(e), "status": 500},500



@api.route("/reset")
class ResetApi(Resource):
    @api.expect(api.model('forgot',{"email":fields.String()}))
    def post(self):
        try:
            data=request.json
            user=Users.query.filter_by(email=data["email"]).first()
            if not user:
                return {"message": "User not found", "status": 404},404
            token=user.token('reset',15)
            send_mail(user.username,user.email,token,"reset")
            return {"message":"Mail sent successfully","status":200,"token":token},200
        except Exception as e:
            return {"message": str(e), "status": 500},500
        
    @api.doc(params={"token": "Jwt token for password reset"}, body=api.model('reset',
                {'newpassword':fields.String(), 'confirmpassword':fields.String()}))
    def put(self):
        try:
            token=request.args.get('token')
            if not token:
                return {'message': 'Token not found','status': 404},404
            decoded=JWT.to_decode(token,'reset')
            userid=decoded["userid"]
            user=Users.query.filter_by(id=userid).first()
            if not user:
                return {'message': 'User not found','status': 404},404
            data=request.json
            serializer=UserPasswordSchema(password=data['newpassword'])
            newpassword=serializer.model_dump()['password']
            confirmpassword=data['confirmpassword']
            if newpassword!=confirmpassword :
                raise ValueError("Password mismatch")
            user.set_password(newpassword)
            db.session.commit()
            return {'message': 'Password changed succesfully', 'status': 200},200
        except PyJWTError:
            return {'message':"Invalid token", "status": 401},401
        except ValueError as e:
            return {'message': str(e), "status":401},401
        except Exception as e:
            return {'message': str(e), "status":500},500



