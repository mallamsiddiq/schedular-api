

FROM python:3.10


ENV PYTHONUNBUFFERED 1


RUN mkdir /newsite


WORKDIR /newsite


ADD . /newsite/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD gunicorn newsite.wsgi:application --bind 0.0.0.0:$PORT