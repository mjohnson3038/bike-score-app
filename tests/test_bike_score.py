import pytest


from bike_score_app import create_app
from bike_score_app import bike_score as module

from flask import json

TEST_REQUEST_CONTENT = {
	"total_distance": 6.9,
	"points_of_elevation": [1, 3.2, 5.0, 9.9, 2.3],
	"bike_lane_availability": 40,
    "safety_incidents": 2,
}

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


@pytest.mark.parametrize(('points_of_elevation', 'expected'), (
    ([], 0),
    ([5], 0),
    ([5, 5], 0),
    ([0, 0], 0),
    ([-4, -4], 0),
    ([-4, -3], 1),
    ([-4, 10], 14),
    ([10, 0], -10),
    ([0, 100, 0], 0),
    ([1, 100, -1], -2),
    ([1, -100, -1], -2),
))
def test_net_elevation_gain_returns_expected_value(points_of_elevation, expected):
    actual = module.calculate_net_elevation_gain(points_of_elevation)
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
            'bike_lane_availability_score': 40,
            'net_elevation_gain': 1.3,
            'total_elevation_gain': 8.9,
            'safety_incidents': 2,
        }
    }

    assert json.loads(response.data) == expected_response
