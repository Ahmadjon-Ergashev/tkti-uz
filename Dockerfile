FROM python:latest

WORKDIR /usr/src/app

ENV PYTHONDONTWRITENYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y wkhtmltopdf
RUN pip install --upgrade pip

COPY requirements.txt /usr/src/app

RUN python -m pip install daphne
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /usr/src/app