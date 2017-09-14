FROM python:3

RUN \
  apt-get update && apt-get install -y \
    lsb-release && \
  export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
  echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
  apt-get update && apt-get install -y \
    google-cloud-sdk \
    openssl && \
  pip install \
    google-cloud-storage \
    pyquery \
    elasticsearch && \
  apt-get clean && rm -rf /var/lib/apt/lists/* 

WORKDIR /opt/ptt-crawler
ENTRYPOINT /bin/bash
