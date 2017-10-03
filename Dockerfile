FROM python:3

ENV GOOGLE_APPLICATION_CREDENTIALS /opt/ptt-crawler/oauth.json
RUN \
  apt-get update && apt-get install -y \
    lsb-release && \
  export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
  echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
  apt-get update && apt-get install -y \
    locales \
    google-cloud-sdk \
    openssl && \
  pip install --no-cache-dir \
    urllib3 \
    google-cloud-storage \
    pyquery \
    elasticsearch && \
  apt-get clean && rm -rf /var/lib/apt/lists/* 

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

WORKDIR /opt/ptt-crawler
ENTRYPOINT python web_crawler/ptt.py
