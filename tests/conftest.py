from pardal.authserver.app import AuthToken
from pardal.authserver.run import app as server
from peewee import SqliteDatabase
import pytest


test_db = SqliteDatabase(':memory:')
MODELS = [AuthToken]


@pytest.fixture
def app():
    server.config['TESTING'] = True
    server.config['DATABASE'] = ':memory:'
    return server


@pytest.fixture(scope="session", autouse=True)
def db():
    with test_db.bind_ctx(MODELS):
        test_db.create_tables(MODELS, safe=True)

        yield test_db

        test_db.drop_tables(MODELS)
        test_db.close()
