from celery import Celery
from flask import Flask

from app import config


app = Flask(__name__)
app.config.from_object(config)
app.secret_key = app.config['SECRET_KEY']

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from app.views import views as views_blueprint

app.register_blueprint(views_blueprint)

if __name__ == '__main__':
    app.run()
