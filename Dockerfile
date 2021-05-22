FROM python

WORKDIR /app/downloader

RUN apt-get -y update 

RUN pip3 install flask flask-sqlalchemy flask-login sqlalchemy-utils youtube_dl requests
RUN set -x  add-apt-repository ppa:mc3man/trusty-media \
    && apt-get -y update \
    && apt-get -y dist-upgrade \
    && apt-get install -y ffmpeg

COPY ./ ./

CMD [ "python","app.py" ]