FROM python:2.7

RUN apt-get update && \
    apt-get install -y \
	nginx \
	supervisor
RUN pip install -U pip setuptools

# install uwsgi now because it takes a little while
RUN pip install uwsgi

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/default
COPY supervisor-app.conf /etc/supervisor/conf.d/

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code, this will cause Docker's caching mechanism
# to prevent re-installinig (all your) dependencies when you made a change a line or two in your app.

RUN mkdir /home/docker/
RUN mkdir /home/docker/api/
RUN mkdir /home/docker/api/app/

COPY ./app/requirements.txt /home/docker/api/app/
RUN pip install -r /home/docker/api/app/requirements.txt

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log
