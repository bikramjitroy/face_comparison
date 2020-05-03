# This is a sample Dockerfile you can modify to deploy your own app based on face_recognition

FROM python:3.6-slim-stretch

RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*


RUN cd ~ && \
    pip3 install face_recognition && \
    pip3 install flask flask-uploads && \
    pip3 install werkzeug==0.15 && \
    mkdir /root/uploads && \
    cd /root/

COPY . /root/

RUN ls -lthr /root

RUN cd /root && \
    export FLASK_APP=app.py

CMD ["flask","run","--host=0.0.0.0"] 

EXPOSE 5000/tcp
