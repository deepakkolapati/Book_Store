from users import db

class Users(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(15),nullable=False,unique=True)
    email=db.Column(db.String(255),nullable=False,unique=True)
    password=db.Column(db.String(255),nullable=False)
    superkey=db.Column(db.Boolean,default=False)
    isverified=db.Column(db.Boolean,default=False)

    @property
    def json(self):
        return {
            'id':self.id,
            'username':self.username,
            'email':self.email,
            'superkey':self.superkey,
            'isverified':self.isverified
        }

