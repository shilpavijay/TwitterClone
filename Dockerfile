FROM python:3.7-alpine
RUN apk update && apk add bash
RUN apk add gcc libc-dev linux-headers mariadb-dev
RUN pip install django djangorestframework django-rest-swagger PyJWT==1.7.1 gunicorn mysqlclient
COPY TwitterClone /app/TwitterClone
COPY TUsers /app/TUsers
COPY Tweets /app/Tweets
COPY manage.py /app
COPY wait-for-mysql.sh /app
WORKDIR /app
EXPOSE 8000
CMD ["gunicorn","TwitterClone.wsgi","--bind=0.0.0.0:8000"]