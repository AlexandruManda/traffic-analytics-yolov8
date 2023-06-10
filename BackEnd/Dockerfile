FROM nvidia/cuda:11.6.0-base-ubuntu20.04
RUN apt update
RUN apt-get install -y python3 python3-pip 


WORKDIR /app

COPY requirements.txt .


RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu116

RUN apt-get update && apt-get install -y \
    libxkbcommon-x11-0 \
    libxcb-xinerama0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-render-util0 \
    libxcb-util1 \
    libxcb-xfixes0 \
    libxcb-xkb1 \
    build-essential \
    libxrender1 \
    libxtst6 \
    openssl \
    libssl-dev \
    xvfb

RUN pip install -r requirements.txt

RUN pip install uwsgi

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get install -y libglib2.0-0

COPY . .

EXPOSE 5000

CMD uwsgi --http :5000 --http-websockets --master --wsgi-file run.py --callable app

