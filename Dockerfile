FROM python:3.9-bullseye

RUN apt-get update

WORKDIR /root

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait 
RUN chmod +x /wait 

CMD /wait && python webserver/webserver.py