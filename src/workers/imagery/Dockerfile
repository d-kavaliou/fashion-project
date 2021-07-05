FROM python:3.7-slim

COPY /requirements.txt /tmp/requirements.txt

WORKDIR /workers

RUN apt-get update -yqq && \
    apt-get -yqq install libsndfile1 --no-install-recommends && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --compile -r /tmp/requirements.txt && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/* /tmp/* /var/tmp/*

COPY /app /workers/app
COPY worker.py /workers/worker.py
COPY config.yml /workers/config.yml

EXPOSE 6379 5672