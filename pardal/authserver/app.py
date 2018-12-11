from datetime import datetime
from flask import Flask
import os
from pardal import get_logger
from peewee import DateTimeField, CharField
from playhouse.flask_utils import FlaskDB


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'super secret key'
app.config['DATABASE'] = f'sqlite:///pardal.db'

db_wrapper = FlaskDB(app)
logger = get_logger(__name__)

API_ADDRESS = f"{os.getenv('HOST', 'http://0.0.0.0')}:" \
              f"{os.getenv('PORT', '6001')}"


class AuthToken(db_wrapper.Model):
    created = DateTimeField(default=datetime.now)
    updated = DateTimeField(null=True)
    oauth_token = CharField()
    oauth_token_secret = CharField()
    username = CharField()

    def save(self, *args, **kwargs):
        if self.id:
            self.updated = datetime.now()
        return super(AuthToken, self).save(*args, **kwargs)

    def print(self):
        print(f'{self.username}\n'
              f'{self.oauth_token}\n'
              f'{self.oauth_token_secret}\n'
              f'{self.created}')


def initialize_db():
    if not db_wrapper.database.table_exists('AuthToken'):
        db_wrapper.database.create_tables([AuthToken], safe=True)
    logger.info('DB initialized')


@app.cli.command()
def initdb():
    initialize_db()
