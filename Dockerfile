FROM python:3.8.3

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /flask-starter

WORKDIR /flask-starter

ADD ./requirements.txt /flask-starter

ADD ./src /flask-starter

RUN pip install gunicorn==20.1.0 -i https://mirrors.cloud.tencent.com/pypi/simple

RUN pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple

CMD [ "gunicorn", "--bind" , "0.0.0.0:8080", "main:app"]