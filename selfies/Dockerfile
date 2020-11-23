FROM nginx
WORKDIR '/root'

RUN apt-get update
RUN apt-get install python3 python3-pip -y

COPY app_nginx.conf /etc/nginx/conf.d/
COPY application .
COPY selfies.service /etc/systemd/system/multi-user.target.wants/selfies.service

RUN service selfies start
RUN service selfies enable
RUN pip3 install -r requirements.txt
RUN service nginx restart
