from flask import Flask

def create_app(database):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://postgres:9033@localhost:5432/{database}"
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
    return app


