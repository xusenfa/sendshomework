FROM nginx:latest
RUN apt update -y && apt -y install python3 python3-pip cron
RUN pip3 install bs4 flask gevent requests lxml
RUN openssl dhparam -out /tmp/dhparam.pem 2048
RUN echo '*/5 * * * * root sh -c "cd /sendshomework/flask && /usr/bin/python3 spider.py"' >> /etc/crontab
CMD ["/sendshomework/start.sh"]