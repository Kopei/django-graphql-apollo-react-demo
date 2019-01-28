FROM python:3.6.8

RUN sed -i "s/httpredir.debian.org/mirrors.163.com/" /etc/apt/sources.list

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
        g++ \
        gcc \
        gettext \
    	git \
        vim \
        build-essential \
        xorg \
        libssl-dev \
        libxrender-dev \
        wget \
        gdebi \
        libffi-dev\
        unzip \
        libaio1 \
        libaio-dev \
        ca-certificates \
    	&& apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com

RUN echo "Asia/Shanghai" > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata

EXPOSE 8080

ADD . .

#CMD ['which', 'python']
#CMD ['uwsgi', '/app/uwsgi.ini']