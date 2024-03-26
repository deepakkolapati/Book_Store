from books import app,db
from flask_restx import Api,Resource,fields
from flask import request
from core.utils import JWT, authorize_user
from users.models import Users
from schemas.book_schema import BookSchema
from books.models import Books
from jwt import PyJWTError
from sqlalchemy.exc import IntegrityError
from flask import g

api=Api(app=app, prefix = "/api",
        authorizations={'apiKey': {
                'type': 'apiKey',
                'in': 'header',
                'required': True,
                'name': 'Authorization'
            }},
        title = 'Book_Inventory', doc = "/docs",default="Book",default_label="Inventory")

@api.route("/books")
class BookApi(Resource):

    method_decorators = [authorize_user]

    @api.doc(body=api.model('create',{
        "title":fields.String(),"author":fields.String(),"price":fields.Integer(),"quantity":fields.Integer()}))
    def post(self):
        try:
            if not g.user['issuperuser']:
                return {"message": "Access denied to perform this operation", "status": 403}, 403
            serializer=BookSchema(**request.json)
            data=serializer.model_dump()
            book=Books(**data)
            db.session.add(book)
            db.session.commit()
            return {"message": "Book added successfully", "status" : 201, "data": book.json},201
        except PyJWTError:
            return {'message':"Invalid token", "status": 401},401
        except ValueError as e:
            return {"message": str(e), "status": 400},400
        except IntegrityError as e:
            return {"message": str(e), "status": 409},409
        except Exception as e:
            return {"message": str(e), "status":500},500
        
    def get(self, *args, **kwargs):
        try:
            books=Books.query.all()
            data=[book.json for book in books]
            return {"message": "Books fetched successfully", "status":200, "data": data},200
        except Exception as e:
            return {"message": str(e), "status": 500},500
        
    def delete(self, *args, **kwargs):
        try:
            if not g.user['issuperuser']:
                return {"message": "Access denied to perform this operation", "status": 403}, 403
            bookid=request.args.get("id")
            book=Books.query.filter_by(id=bookid,userid=kwargs['userid']).first()
            db.session.delete(book)
            db.session.commit()
            return {"message": "Book deleted successfully", "status": 204},204
        except Exception as e:
            return {"message": str(e), "status": 500},500
        
    def put(self):
        try:
            if not g.user['issuperuser']:
                return {"message": "Access denied to perform this operation", "status": 403}, 403
            id= request.args.get('id')
            userid=g.user['id']
            book=Books.query.filter_by(id=id,userid=userid).first()
            serializer=BookSchema(**request.json)
            data=serializer.model_dump()
            [setattr(book,key,value)  for key,value in data.items()]
            db.session.commit()
            return {"message": "Book updated successfully", "status": 200},200
        except ValueError as e:
            return {"message": str(e), "status": 400},400
        except Exception as e:
            return {"message": str(e), "status": 500}, 500

        




