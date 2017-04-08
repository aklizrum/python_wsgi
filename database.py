import sqlite3
import os
import re


class Database:
    connector = None
    cursor = None
    database_filename = 'database.sqlite'
    backup_filename = 'backup.sql'

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        full_database_path = '{}/{}'.format(dir_path, self.database_filename)

        try:
            database_file = open(full_database_path, 'r')
            self.connector = sqlite3.connect(full_database_path)
            self.cursor = self.connector.cursor()
        except IOError:
            backup_file_path = '{}/{}'.format(dir_path, self.backup_filename)
            backup_file = open(backup_file_path, 'r')
            sql = backup_file.read()
            self.connector = sqlite3.connect(full_database_path)
            os.chmod(full_database_path, 0o755)
            self.cursor = self.connector.cursor()
            self.cursor.executescript(sql)

        self.cursor.row_factory = sqlite3.Row

    def get_regions(self):
        self.cursor.execute('select * from region')

        return [self.dict_from_row(x) for x in self.cursor]

    def get_more_posted_region(self, comments_minimal_count):
        sql = '''
            select region.id, region.name, count(comment.id) as comments_count 
            from comment
            left join user 
            on comment.user_id = user.id
            left join city
            on user.city = city.id
            left join region
            on city.region_id = region.id
            group by region.id 
            having count(*) >= {}
        '''.format(comments_minimal_count)

        self.cursor.execute(sql)

        return [self.dict_from_row(row) for row in self.cursor]

    def get_cities_by_region_id(self, region_id):
        self.cursor.execute('select * from city where region_id = {}'.format(region_id))

        return [self.dict_from_row(row) for row in self.cursor]

    def get_city_by_region_id(self, region_id):
        sql = '''
                select city.name, count(comment.id) as comments_count 
                from comment
                left join user 
                on comment.user_id = user.id
                left join city
                on user.city = city.id
                left join region
                on city.region_id = region.id
                where region.id = {}
                group by city.id
        '''.format(region_id)

        self.cursor.execute(sql)

        return [self.dict_from_row(row) for row in self.cursor]

    def save_user(self, post):
        user_post = post.copy()
        del user_post['comment']
        keys, values = self.unpack_post(user_post)

        sql = "insert into user ({}) values ({})".format(
            ', '.join(keys), (', '.join("'" + item + "'" for item in values)))

        self.cursor.execute(sql)
        self.connector.commit()

        return self.cursor.lastrowid

    def get_comments(self):
        self.cursor.execute('select * from comment')

        return [self.dict_from_row(row) for row in self.cursor]

    def delete_comment(self, comment_id):
        sql = 'delete from comment where id = {}'.format(comment_id)

        self.cursor.execute(sql)
        self.connector.commit()

    def save_comment(self, post):
        user_id = self.save_user(post)
        comment_text = ''

        if 'comment' in post:
            comment_text = self.escape_code(post['comment'][0])

        sql = "insert into comment (user_id, text) values ({}, '{}')".format(user_id, comment_text)

        self.cursor.execute(sql)
        self.connector.commit()

    def dict_from_row(self, row):
        return dict(zip(row.keys(), row))

    def unpack_post(self, post):
        keys = list(post)
        values = [post[key][0] for key in keys]

        return keys, values

    def escape_code(self, text):
        scripts = re.compile(r'<(script).*?</\1>(?s)')
        css = re.compile(r'<style.*?/style>')
        tags = re.compile(r'<.*?>')
        comment_text = scripts.sub('', text)
        comment_text = css.sub('', comment_text)
        comment_text = tags.sub('', comment_text)

        return comment_text
