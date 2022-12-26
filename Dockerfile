FROM python:3.10.4-slim-buster

WORKDIR /usr/src/microblog

COPY app app
COPY requirements.txt requirements.txt
COPY migrations migrations
COPY .env microblog.py config.py boot.sh ./
RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r ./requirements.txt
RUN chmod +x boot.sh

RUN export FLASK_APP=microblog.py

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]