import pytest
import jwt
import base64


def test_auth_no_password(client):
    """Test auth endpoint with no password"""
    rv = client.get('/auth')
    assert b'Could not verify' in rv.data
 
def test_auth_wrong_password(client):
    """Test auth endpoint with wrong password"""
    password = "wrong_password"
    rv = client.get(
        '/auth',
        headers = {
            'Authorization': 'Basic ' \
            + base64.b64encode(bytes(":" + password, 'ascii')).decode('ascii')
        }
    )
    assert b'Could not verify' in rv.data
 
def test_auth(client):
    """Test auth endpoint with correct password"""
    password = "password"
    rv = client.get(
        '/auth',
        headers = {
            'Authorization': 'Basic ' \
            + base64.b64encode(bytes(":" + password, 'ascii')).decode('ascii')
        }
    )

    json_data = rv.get_json()
    assert jwt.decode(json_data['token'], 'SECRET_KEY', algorithms="HS256")
