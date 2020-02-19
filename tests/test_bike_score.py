import pytest


from bike_score_app import create_app
from bike_score_app import bike_score as module

from flask import json

TEST_REQUEST_CONTENT = {
   'bike_lane_availability': 80
}

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


@pytest.mark.parametrize(('start', 'end', 'expected'), (
    (5, 5, 0),
    (0, 0, 0),
    (-4, -4, 0),
    (-4, -3, 1),
    (-4, 10, 14),
    (10, 0, -10),
    (1, -1, -2),
))
def test_net_elevation_gain_returns_expected_value(start, end, expected):
    actual = module.calculate_net_elevation_gain(start, end)
    assert expected == actual


@pytest.mark.parametrize(('availability', 'expected'), (
    (100, 100),
    (0, 0),
    (57, 57),
    (33, 33),
))
def test_bike_lane_availability_score_returns_percentage_of_bike_lanes_available(availability, expected):
    actual = module.calculate_bike_lane_availability_score(availability)
    assert expected == actual


@pytest.mark.parametrize(('elevation_points', 'expected'), (
    ([], 0),
    ([2], 0),
    ([2, 2], 0),
    ([2, -3], 0),
    ([2, 4], 2),
    ([2, 4, 2], 2),
    ([2, -13, -12, -13, -6, -8, -1, 0, 2, 3, 4, 2], 20),
    ([2.0, 4.3, 2], 2.3),
))
def test_calculate_elevation_gain_returns_expected_elevation_gain(elevation_points, expected):
    actual = module.calculate_elevation_gain(elevation_points)
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
