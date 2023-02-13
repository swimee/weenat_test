FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

WORKDIR /backend

ADD ./config/requirements.txt /backend/config/

RUN pip install --no-cache-dir --upgrade -r ./config/requirements.txt

COPY . .