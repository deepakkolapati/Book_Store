from core import create_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db=SQLAlchemy()
migrate=Migrate()

app=create_app("book_cart")
db.init_app(app)
migrate.init_app(app,db)
