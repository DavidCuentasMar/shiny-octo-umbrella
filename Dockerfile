from python:3.7-alpine
WORKDIR /app
COPY . /app
RUN pip install -r /app/requirements.txt