FROM python

WORKDIR /app/downloader

RUN set -x  add-apt-repository ppa:mc3man/trusty-media \
    && apt-get -y update \
    && apt-get -y dist-upgrade \
    && apt-get install -y ffmpeg

RUN pip3 install flask flask-sqlalchemy flask-login sqlalchemy-utils youtube_dl requests ffmpeg-python

COPY ./ ./

CMD [ "python","app.py" ]