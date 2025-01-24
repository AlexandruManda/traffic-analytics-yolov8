FROM nvidia/cuda:11.6.0-base-ubuntu20.04
RUN apt update
RUN apt-get install -y python3 python3-pip 


WORKDIR /app

COPY requirements.txt .


RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu116


RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    cmake \
    gcc g++ \
    libavcodec-dev \
    libswscale-dev \
    libavformat-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer1.0-dev \
    libpng-dev \
    libopencv-dev \
    libjpeg-dev \
    libopenexr-dev \
    libtiff-dev \
    libwebp-dev \
    wget \
    qtbase5-dev \
    qtchooser \
    qt5-qmake \
    qtbase5-dev-tools \
    libtbb-dev \
    libgphoto2-dev \
    ffmpeg \
    usbutils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install -r requirements.txt

RUN pip install uwsgi

RUN apt-get install -y libglib2.0-0

COPY . .

EXPOSE 5000

CMD uwsgi --http :5000 --http-websockets --master --wsgi-file run.py --callable app

