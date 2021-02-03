FROM gcc as builder

WORKDIR /app/downloader

RUN apt-get -y update \
    && apt-get install -y cmake \
    && apt-get install -y liblog4c-dev \
    && wget https://yt-dl.org/downloads/latest/youtube-dl -O /usr/local/bin/youtube-dl \
    && chmod a+rx /usr/local/bin/youtube-dl \
    && apt-get install -y default-libmysqlclient-dev \
    && apt-get install -y default-mysql-client \
    && apt-get install -y libconfig-dev \
    && apt-get install -y ffmpeg

COPY ./ ./

RUN mkdir build \
    && cp support/log4crc build \
    && cp support/ffmpeg_sup.sh build \
    && cd build \
    && cmake .. \
    && make

CMD [ "build/Downloader" ]