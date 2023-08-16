FROM python:3.10-slim
USER root

RUN apt-get update
RUN apt-get install curl -y wget
RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

COPY requirements.txt .

RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > ./google-cloud-sdk.tar.gz  \
        && mkdir -p /gcloud \
        && tar -C /gcloud -xvf ./google-cloud-sdk.tar.gz \
        && /gcloud/google-cloud-sdk/install.sh
ENV PATH $PATH:/gcloud/google-cloud-sdk/bin

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
