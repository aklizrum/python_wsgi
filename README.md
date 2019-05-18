# Python WSGI

Simple wsgi python application without external dependency

## Run:

- wsgi
```
pip install uwsgi
uwsgi --http :9000 --wsgi-file main.py
```
- docker 
```
docker run -p 9000:9000 aklizrum/python_wsgi
```
- docker-compose
```
docker-compose up
```