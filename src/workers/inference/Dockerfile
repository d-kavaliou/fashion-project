FROM pytorch:1.9.0-cuda10.2-cudnn7-runtime

USER root
RUN apt-get update && apt-get install -y libsm6 libxrender1 libfontconfig1 libxext6 libglib2.0-0 gcc binutils less

ENV APP_DIR='/workers'

WORKDIR $APP_DIR
RUN git clone https://github.com/i008/pytorch-deepfashion.git model

COPY /requirements.txt /tmp/requirements.txt
RUN apt-get update -yqq && \
    apt-get -yqq install libsndfile1 --no-install-recommends && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --compile -r /tmp/requirements.txt && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/* /tmp/* /var/tmp/*

ADD utils app
ADD worker.py ./

EXPOSE 6379 5672