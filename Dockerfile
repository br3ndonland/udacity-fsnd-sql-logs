FROM python:3.7-alpine
LABEL app=news
WORKDIR /app
COPY . /app
RUN apk update; apk add build-base postgresql postgresql-dev libpq
RUN python -m pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile