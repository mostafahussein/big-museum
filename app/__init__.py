from celery import Celery
from flask import Flask

from app import config


app = Flask(__name__)
app.config.from_object(config)
app.secret_key = app.config['SECRET_KEY']

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from app import views
