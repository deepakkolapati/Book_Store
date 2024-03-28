import pytest 
from core import create_app
from users.models import db as user_db , Users
from users.routes import RegisterApi,LoginApi,ResetApi 
from books.models import db as book_db
from books.routes import BookApi
from cart.routes import CartApi,OrderCartApi
from cart.models import db as cart_db
from flask_restx import Api 

@pytest.fixture
def user_app(): 
    app = create_app( 'user' , 'test')
    user_db.init_app(app)
    with app.app_context():
        user_db.create_all()

    api = Api(app)
    api.add_resource(RegisterApi , '/api/user')
    api.add_resource(LoginApi, '/api/login')
    api.add_resource(ResetApi, '/api/reset')

    yield app 

    with app.app_context():
        user_db.drop_all()

@pytest.fixture
def book_app(): 
    app = create_app( 'book' , 'test')
    book_db.init_app(app)
    with app.app_context():
        book_db.create_all()

    api = Api(app)
    api.add_resource(BookApi , '/api/books')

    yield app 

    with app.app_context():
        book_db.drop_all()


@pytest.fixture
def cart_app():
    app = create_app( 'cart' , 'test')
    cart_db.init_app(app)
    with app.app_context():
        cart_db.create_all()
    api = Api(app)
    api.add_resource(CartApi , '/api/cart')
    api.add_resource(OrderCartApi, '/api/order')

    yield app
    
    with app.app_context():
        cart_db.drop_all()

@pytest.fixture
def user_client(user_app):
    return user_app.test_client()

@pytest.fixture
def book_client(book_app):
    return book_app.test_client()

@pytest.fixture
def cart_client(cart_app):
    return cart_app.test_client()

@pytest.fixture
def token(user_client, user_app):
    register_data = {
    "username":"Deepak",
    "email":"deepakkolapati@gmail.com",
    "password": "Kc5656$3ed",
    "superkey":"hf783hboef283920hdchbvb9822991"
}
    response = user_client.post(
        "/api/user",
        json=register_data,
        headers={"Content-Type": "application/json"},
    )
    # with user_app.app_context():
    #     user = Users.query.get(response.json["data"]["id"])
    #     user.isverified = True
    #     user_db.session.commit()
    login_data = { "username":"Deepak",    "password": "Kc5656$3ed"}
    response = user_client.post(
        "/api/login",
        json=login_data,
        headers={"Content-Type": "application/json"},
    )
    return response.json["token"]