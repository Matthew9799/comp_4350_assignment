FROM ubuntu:18.04

RUN apt-get update -y && apt-get install -y python3-pip python3.6

COPY .. /Backend

WORKDIR /Backend

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

ENTRYPOINT [ "gunicorn" ]
CMD ["-b :8080","app:app"]