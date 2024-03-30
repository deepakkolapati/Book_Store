from celery import Celery, Task,shared_task
from users.routes import app as flask_app
from flask_mail import Message
from settings import settings
from . import mail

def celery_init_app(app) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.conf.enable_utc = False
    celery_app.conf.timezone = 'Asia/Kolkata'
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

app=flask_app
celery=celery_init_app(app)

@shared_task
def celery_send_mail(username,email,token,context):
    msg=Message(f"Hello {username}", sender=f"{settings.sender}" , recipients=[email])
    body={"register":"Welcome to Book_Store.\n Pls click on the link to verify {url}{token}".format(
        url="http://127.0.0.1:5000/api/user?token=",token=token),
          "reset":"Welcome to Book_Store.\n Pls click on the link to  reset your password  {url}{token}".format(
        url="http://127.0.0.1:5000/api/?token=",token=token)}
    msg.body=body[context].format(token=token)
    mail.send(msg)