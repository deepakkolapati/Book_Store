from cart import db

class Cart(db.Model):
    __tablename__='cart'
    id = db.Column(db.Integer,primary_key=True)
    userid=db.Column(db.Integer,nullable=False)
    total_price = db.Column(db.Integer,default=0)
    total_quantity = db.Column(db.Integer,default=0)
    is_ordered=db.Column(db.Boolean,default=False)
    ordered_at=db.Column(db.DateTime)
    items=db.relationship('CartItems',back_populates="cart")

    @property
    def json(self):
        return {
            'id':self.id,
            'userid':self.userid,
            'total_amount':self.total_price,
            'total_quantity':self.total_quantity,
            'is_ordered':self.is_ordered,
            'ordered_at':self.ordered_at
        }

class CartItems(db.Model):
    __tablename__='cart_items'
    id=db.Column(db.Integer, primary_key=True)
    cart_id=db.Column(db.Integer,db.ForeignKey('cart.id',ondelete='CASCADE'),nullable=False)
    book_id=db.Column(db.Integer,nullable=False)
    quantity=db.Column(db.Integer,default=0)
    price=db.Column(db.Integer,default=0)
    cart=db.relationship('Cart',back_populates="items")

    @property
    def json(self):
        return {
            'id':self.id,
            'cart_id':self.cart_id,
            'book_id':self.book_id,
            'quantity':self.quantity,
            'price':self.price
        }
