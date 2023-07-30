FROM python:alpine

WORKDIR /app/downloader

RUN apk add ffmpeg \
    && apk add g++

RUN pip3 install flask flask-sqlalchemy flask-login sqlalchemy-utils yt_dlp requests ffmpeg-python

COPY ./ ./

CMD [ "python","app.py" ]