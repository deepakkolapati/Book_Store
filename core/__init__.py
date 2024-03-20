from flask import Flask
from flask_mail import Mail
from settings import settings

mail=Mail()

def create_app(database):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.database_url.format(database=database)
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = settings.mail_port
    app.config['MAIL_USERNAME'] = settings.sender
    app.config['MAIL_PASSWORD'] = settings.mail_password
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail.init_app(app)
    return app


