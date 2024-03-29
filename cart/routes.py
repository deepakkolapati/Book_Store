from cart import app,db
from flask_restx import Api,Resource,fields
from flask import request
from core.utils import authorize_user
from cart.models import Cart,CartItems
from schemas.cart_schema import ItemSchema
from flask import g
import requests as http
import json

api=Api(app=app,
        prefix="/api",
        authorizations={'apiKey': {
                'type': 'apiKey',
                'in': 'header',
                'required': True,
                'name': 'Authorization'}},
        doc="/docs",title="Book_Cart",default="Book",default_label="Cart")


@api.route("/cart")
class CartApi(Resource):
    
    method_decorators=[authorize_user]
    @api.expect(api.model('Add/deleteItems',{'bookid':fields.Integer(),'quantity':fields.Integer()}))
    def post(self):
        try:
            serializer=ItemSchema(**request.json)
            data=serializer.model_dump()
            bookid= data['bookid']
            response=http.get(f'http://127.0.0.1:7000/getBook?id={bookid}')
            if response.status_code >= 400:
                return {"message": "Book not found", "status":404},404
            book=response.json()
            userid=g.user['id']
            cart= Cart.query.filter_by(userid=userid,is_ordered=False).first()
            if not cart:
                cart=Cart(userid=userid)
                db.session.add(cart)
                db.session.commit()
            cart_item = CartItems.query.filter_by(cart_id=cart.id,book_id=book['id']).first()
            if not cart_item:
                cart_item=CartItems(cart_id=cart.id,book_id=book['id'])
                db.session.add(cart_item)
                db.session.commit()
            cart_item.quantity=data['quantity']
            cart_item.price=book['price']
            db.session.commit()
            cart.total_quantity=sum([item.quantity for item in cart.items])
            cart.total_price=sum([item.quantity*item.price for item in cart.items])
            db.session.commit()
            return {"message": "Book added to cart successfully", "status": 201,"data": cart_item.json},201
        except ValueError as e:
            return {"message": str(e), "status": 400},400
        except Exception as e:
            print(e)
            return {"message": str(e), "status": 500},500
        

    def get(self,*args,**kwargs):
        try:
            user_id=g.user['id']
            cart= Cart.query.filter_by(userid=user_id,is_ordered=False).first()
            if not cart:
                return {"message": "Cart not found", "status":404},404
            items=cart.items
            items_data=[item.json for item in items]
            return {"message": "Cart fetched successfully","status":200,"cart_data":cart.json,
                    "items_data":items_data}
        except Exception as e:
            return {"message": str(e), "status": 500},500


    @api.doc(params={'id':"Enter the cart id to be deleted"})
    def delete(self,*args,**kwargs):
        try:
            user_id=g.user['id']
            cart_id=request.args.get('id')
            if not cart_id:
                return {"message": "Cart id not found", "status":404},404
            cart= Cart.query.filter_by(id=cart_id,userid=user_id).first()
            for item in cart.items:
                db.session.delete(item)
            db.session.delete(cart)
            db.session.commit()
            return {"message": "Cart deleted successfully", "status": 204},204
        except Exception as e:
            return {"message": str(e), "status": 500},500


@api.route('/order')     
class OrderCartApi(Resource):
    method_decorators=[authorize_user]
    def post(self,*args,**kwargs):
        try:
            user_id=g.user['id']
            cart=Cart.query.filter_by(userid=user_id,is_ordered=False).first()
            if not cart:
                return {"message": "Cart not found", "status":404},404
            items= cart.items
            cart_data={}
            headers = {'Content-Type': 'application/json'}
            for item in items:
                cart_data[item.book_id]=item.quantity
            validate_response=http.post('http://127.0.0.1:7000/validateBooks',json=cart_data,headers=headers)
            if validate_response.status_code >= 400:
                return validate_response.json()
            order_response=http.patch("http://127.0.0.1:7000/updateBooks",json=cart_data,headers=headers)
            cart.is_ordered=True
            db.session.commit()
            return {"message": "Cart ordered successfully", "status":200},200
        except Exception as e:
            return {"message":str(e),"status": 500},500

    @api.doc(params={"id":"Cart id to be canceled"})
    def delete(self,*args,**kwargs):
        try:
            user_id=g.user["id"]
            id=request.args.get("id")
            cart=Cart.query.filter_by(userid=user_id,is_ordered=True,id=id).first()
            if not cart:
                return {"message": "Cart not found", "status":404},404
            headers = {'Content-Type': 'application/json'}
            items=cart.items
            cart_data={}
            for item in items:
                cart_data[item.book_id]=-1*item.quantity
            order_response=http.patch("http://127.0.0.1:7000/updateBooks",json=cart_data,headers=headers)
            for item in cart.items:
                db.session.delete(item)
                db.session.commit()
            db.session.delete(cart)
            db.session.commit()
            return {"message": "Ordered cancelled successfully", "status":204},204
        except Exception as e:
            return {"message": str(e), "status": 500},500

            
            
            


            




            
            

