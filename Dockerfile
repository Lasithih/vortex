FROM python

WORKDIR /app/downloader

RUN apt-get -y update 

RUN pip3 install flask flask-sqlalchemy flask-login sqlalchemy-utils
RUN pip3 install youtube_dl
RUN pip3 install requests


COPY ./ ./

CMD [ "python","app.py" ]