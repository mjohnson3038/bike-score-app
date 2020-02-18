from bike_score_app import create_app
from flask import json


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_post_bike_score_returns_expected_json(client):
    response = client.post('/api/bike_score')
    assert json.loads(response.data) == {'bike_score': 79}

def test_get_bike_score_returns_405(client):
    response = client.get('/api/bike_score')
    assert response.status == '405 METHOD NOT ALLOWED'