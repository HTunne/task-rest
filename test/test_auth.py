import pytest
import jwt
import base64


def query_auth(client, user, password):
    return client.get(
        '/auth',
        headers = {
            'Authorization': 'Basic ' \
            + base64.b64encode(bytes(user + ":" + password, 'ascii')).decode('ascii')
        }
    )

def test_auth_no_password(client):
    """Test auth endpoint with no user or password"""
    rv = client.get('/auth')
    assert b'Could not verify' in rv.data

def test_auth_wrong_password(client):
    """Test auth endpoint with correct user wrong password"""
    user = "dev"
    password = "wrong_password"
    rv = query_auth(client, user, password)
    assert b'Could not verify' in rv.data

def test_auth_wrong_user(client):
    """Test auth endpoint with correct user wrong password"""
    user = "div"
    password = "password"
    rv = query_auth(client, user, password)
    assert b'Could not verify' in rv.data

def test_auth(client):
    """Test auth endpoint with correct user and password"""
    user = "dev"
    password = "password"
    rv = query_auth(client, user, password)
    json_data = rv.get_json()
    assert jwt.decode(json_data['token'], 'SECRET_KEY', algorithms="HS256")
