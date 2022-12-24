FROM python:3.8-slim
RUN pip install pipenv
WORKDIR /app
COPY . .
RUN pipenv install
