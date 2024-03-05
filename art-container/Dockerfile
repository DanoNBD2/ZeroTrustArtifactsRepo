FROM tiangolo/uwsgi-nginx-flask:python3.11
RUN pip3 install art PyJWT requests cryptography
COPY uwsgi.ini /etc/uwsgi/uwsgi.ini
COPY ./uwsgi-streaming.conf /etc/nginx/conf.d/
COPY ./app /app