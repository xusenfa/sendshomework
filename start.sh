#!/bin/sh
cd /sendshomework/flask
cp /tmp/dhparam.pem /sendshomework/nginx/nginxconf/dhparam.pem
python3 spider.py
python3 app.py &
service cron start
nginx -c /sendshomework/nginx/nginxconf/nginx.conf -g 'daemon off;'