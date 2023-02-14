FROM ubuntu:18.04

USER root

ENV DEBIAN_FRONTEND=noninteractive 
ENV TZ=Asia/Kolkata
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get install ffmpeg libsm6 libxext6  -y && \
    rm -rf /var/lib/apt/lists/*
RUN add-apt-repository ppa:deadsnakes/ppa && apt-get -y update && apt-get install -y \
    g++ \
    ca-certificates\
    curl\
    git \
    make \
    python3.10-dev \
    sudo \
    libdpkg-perl \
    --no-install-recommends
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

RUN mkdir /backend
WORKDIR /backend
COPY requirements.txt /backend/requirements.txt
RUN pip3 install setuptools==67.2.0
RUN pip3 install -r requirements.txt
RUN mkdir /Backend



COPY . /backend/Backend
ENV PYTHONPATH=/backend
ENV PYTHONUNBUFFERED=1
WORKDIR /backend



ENTRYPOINT ["python3.10","fast-api/main.py"]
