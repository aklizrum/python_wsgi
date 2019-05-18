import json
import os
import re
from html import escape
from urllib.parse import parse_qs
from database import Database


COMMENTS_MINIMAL_COUNT = 5
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
db = Database()


def index(environ, start_response):
    with open('{}/{}'.format(DIR_PATH, 'templates/index.html'), 'r') as f:
        body = f.read()
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    return [body.encode('utf-8')]


def not_found(environ, start_response):
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return [b'Not Found']


def comments(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size).decode('utf-8')

    post_data = parse_qs(request_body)

    if environ.get('REQUEST_METHOD') == 'POST':
        db.save_comment(post_data)

    template = open('{}/{}'.format(DIR_PATH, 'templates/comments.html'), 'r')
    body = template.read()

    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

    return [body.encode('utf-8')]


def delete_comment(environ, start_response):
    url_args = environ['url_args']
    comment_id = escape(url_args[0])
    db.delete_comment(comment_id)

    start_response(
        '302 FOUND',
        [('Location', 'http://{}/view'.format(environ.get('HTTP_HOST')))])

    return [b'Deleted']


def view(environ, start_response):
    template = open('{}/{}'.format(DIR_PATH, 'templates/view.html'), 'r')
    body = template.read()
    rows = ''
    for comment in db.get_comments():
        rows += '''
                <tr>
                    <td>{}</td>
                    <td><a href="/comment/delete/{}">Удалить</a></td>
                </tr>
        '''.format(comment['text'], comment['id'])

    body = body.replace('%rows%', rows)

    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

    return [body.encode('utf-8')]


def stat(environ, start_response):
    template = open('{}/{}'.format(DIR_PATH, 'templates/stat.html'), 'r')
    body = template.read()
    regions = db.get_more_posted_region(COMMENTS_MINIMAL_COUNT)

    rows = ''

    for region in regions:
        rows += '''
                <tr>
                    <td><a href="/stat/{}">{}</a></td>
                    <td>{}</td>
                </tr>
        '''.format(region['id'], region['name'], region['comments_count'])

    body = body.replace('%rows%', rows)

    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

    return [body.encode('utf-8')]


def stat_city(environ, start_response):
    url_args = environ['url_args']
    region_id = escape(url_args[0])

    template = open('{}/{}'.format(DIR_PATH, 'templates/stat_city.html'), 'r')
    body = template.read()
    cities = db.get_city_by_region_id(region_id)

    rows = ''

    for city in cities:
        rows += '''
                <tr>
                    <td>{}</td>
                    <td>{}</td>
                </tr>
        '''.format(city['name'], city['comments_count'])

    body = body.replace('%rows%', rows)

    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

    return [body.encode('utf-8')]


def scripts(environ, start_response):
    script_name = environ['filename']
    script = open('{}/{}'.format(DIR_PATH, script_name), 'r')
    body = script.read()

    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

    return [body.encode('utf-8')]


def get_regions(environ, start_response):
    body = json.dumps(db.get_regions())

    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    return [body.encode('utf-8')]


def get_cities(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size).decode('utf-8')
    post_data = parse_qs(request_body)

    region_id = post_data['region_id'][0]
    body = json.dumps(db.get_cities_by_region_id(region_id))

    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

    return [body.encode('utf-8')]


def wsgi_app(environ, start_response):
    path = environ.get('REQUEST_URI', '').lstrip('/')
    for regex, callback in urls:
        match = re.search(regex, path)
        if match:
            environ['url_args'] = match.groups()
            environ['filename'] = path
            return callback(environ, start_response)
    return not_found(environ, start_response)


urls = [
    (r'comments/?$', comments),
    (r'comment/delete/(.+)$', delete_comment),
    (r'view/?$', view),
    (r'stat/?$', stat),
    (r'stat/(.+)$', stat_city),
    (r'.*\.js$', scripts),
    (r'get_regions/?$', get_regions),
    (r'get_cities/?$', get_cities),
    (r'', index),
]

application = wsgi_app
