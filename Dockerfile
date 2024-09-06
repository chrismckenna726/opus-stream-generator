FROM python:3.10-slim

WORKDIR /code

RUN apt update --allow-unauthenticated --allow-insecure-repositories && apt install -y \
    libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev \
    gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 \
    gstreamer1.0-qt5 gstreamer1.0-pulseaudio  gstreamer1.0-rtsp

COPY main.py .

CMD ["python","-u","./main.py"]
