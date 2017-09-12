FROM python:3

RUN \
  apt-get update && apt-get install -y \
    openssl && \
  pip install \
    beautifulsoup4 \
    elasticsearch 

WORKDIR /opt/ptt-crawler
ENTRYPOINT /bin/bash
