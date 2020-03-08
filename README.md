# Python WSGI

Simple wsgi python application without external dependency

## Run:

- wsgi
```
pip install uwsgi
uwsgi --http :9000 --ini uwsgi.ini
```
- docker-compose
```
docker-compose up
```