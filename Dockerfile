FROM python:3.10.4-slim-buster

WORKDIR /usr/src/microblog

COPY . .
RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r ./requirements.txt
RUN chmod +x boot.sh

RUN export FLASK_APP=microblog.py

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]

#RUN ["flask", "db", "upgrade"]
#RUN ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "microblog:app"]