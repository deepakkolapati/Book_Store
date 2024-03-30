from flask import Flask
from flask_mail import Mail
from settings import settings

mail=Mail()

def create_app(database , mode='debug'):
    app = Flask(__name__)
    if mode == 'debug':
        app.config['SQLALCHEMY_DATABASE_URI'] = settings.database_url.format(database=database)
        app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
        app.config['DEBUG'] = True
        
    if mode == 'test':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
        app.config['TESTING'] = True
    app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://127.0.0.1:6379/0",
        result_backend="redis://127.0.0.1:6379/0",
        broker_connection_retry_on_startup=True,
        # task_ignore_result=True,
        redbeat_redis_url = "redis://localhost:6379/0",
        redbeat_lock_key = None,
        enable_utc=True,
        beat_max_loop_interval=5,
        beat_scheduler='redbeat.schedulers.RedBeatScheduler'
                 ),
        )
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = settings.mail_port
    app.config['MAIL_USERNAME'] = settings.sender
    app.config['MAIL_PASSWORD'] = settings.mail_password
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail.init_app(app)
    return app


