FROM ubuntu:14.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get -y install nginx sed python-pip python-dev uwsgi-plugin-python supervisor wget
RUN wget http://download.redis.io/redis-stable.tar.gz; tar xvzf redis-stable.tar.gz; cd redis-stable; make; make install

RUN mkdir -p /var/log/nginx/app/
RUN mkdir -p /var/log/uwsgi/
RUN mkdir -p /var/log/celery/

RUN rm /etc/nginx/sites-enabled/default
COPY flask.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf
COPY uwsgi.ini /var/www/app/
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

RUN mkdir -p /var/log/supervisor/
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY app /var/www/app/
COPY requirements.txt /var/www/app/requirements.txt
RUN pip install -r /var/www/app/requirements.txt

CMD ["/usr/bin/supervisord"]