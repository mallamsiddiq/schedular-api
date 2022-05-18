

FROM python:3.10


ENV PYTHONUNBUFFERED 1


RUN mkdir /schedularqualis


WORKDIR /schedularqualis


ADD . /schedularqualis/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD gunicorn schedularqualis.wsgi:application --bind 0.0.0.0:$PORT
