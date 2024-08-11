from books import db

class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title=db.Column(db.String(50), nullable = False)
    author=db.Column(db.String(50), nullable = False)
    price=db.Column(db.Integer, nullable = False)
    quantity=db.Column(db.Integer, nullable = False)
    userid=db.Column(db.Integer, nullable = False)

    @property
    def json(self):
        return {
            'id':self.id,
            'title':self.title,
            'author':self.author,
            'price':self.price,
            'quantity':self.quantity,
            'userid':self.userid
        }
    