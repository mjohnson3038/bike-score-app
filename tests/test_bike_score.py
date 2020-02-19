import pytest


from bike_score_app import create_app
from bike_score_app.bike_score import calculate_bike_lane_availability_score

from flask import json

TEST_REQUEST_CONTENT = {
   'bike_lane_availability': 80
}

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


@pytest.mark.parametrize(('availability', 'expected'), (
    (100, 100),
    (0, 0),
    (57, 57),
    (33, 33),
))
def test_bike_lane_availability_score_returns_percentage_of_bike_lanes_available(availability, expected):
    actual = calculate_bike_lane_availability_score(availability)
    assert expected == actual


def test_post_bike_score_returns_expected_json(client):
    response = client.post(
        '/api/bike_score',
         json=TEST_REQUEST_CONTENT
    )

    expected_response = {
        'data': {
            'bike_score': 79,
            'bike_lane_availability_score': 80,
        }
    }

    assert json.loads(response.data) == expected_response

# def test_get_bike_score_returns_405(client):
#     response = client.get('/api/bike_score')
#     assert response.status == '405 METHOD NOT ALLOWED'
