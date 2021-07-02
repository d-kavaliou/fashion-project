FROM python:3.8.1-slim

COPY /requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --compile -r requirements.txt && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/* /tmp/* /var/tmp/*

COPY /app /app

EXPOSE 5000 6379 5672

CMD uvicorn api:api --host 0.0.0.0 --port 5000