FROM python:2.7-slim

COPY . /home/weather-generator

WORKDIR /home/weather-generator

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    chmod 755 run.sh