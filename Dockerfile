FROM alpine:3.7
EXPOSE 9000
VOLUME /usr/src/app/public
WORKDIR /usr/src/app
RUN apk add --no-cache uwsgi-python3 python3
COPY . .
RUN rm -rf public/*
CMD [ "uwsgi", "--socket", "0.0.0.0:9000", \
               "--uid", "uwsgi", \
               "--plugins", "python3", \
               "--protocol", "http", \
               "--wsgi", "main:application"]