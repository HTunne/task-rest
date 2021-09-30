import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ['FLASK_ENV'] = "development"

import pytest

from task_rest import create_app
import jwt
from datetime import datetime, timedelta


@pytest.fixture
def client(tmpdir):
    app = create_app()
    app.config['TESTING'] = True
    app.config['USER_CONF']['dev']['TASKDATA_LOCATION'] = tmpdir

    with app.test_client() as client:
        yield client

@pytest.fixture
def token():
    token = jwt.encode({
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() \
        + timedelta(minutes=6)
    }, 'SECRET_KEY', algorithm="HS256")
    return token
