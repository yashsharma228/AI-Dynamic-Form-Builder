import os
import tempfile

import pytest

from app import create_app
from extensions import db


@pytest.fixture()
def app():
    temp_dir = tempfile.TemporaryDirectory()
    db_path = os.path.join(temp_dir.name, "test.db")

    class TestConfig:
        TESTING = True
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        JSON_SORT_KEYS = False
        LOG_LEVEL = "INFO"

    app = create_app(TestConfig)

    with app.app_context():
        db.drop_all()
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    temp_dir.cleanup()


@pytest.fixture()
def client(app):
    return app.test_client()
