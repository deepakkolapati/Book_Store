from core import create_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app= create_app("book_users")
db=SQLAlchemy()
migrate=Migrate()
db.init_app(app)
migrate.init_app(app,db)
