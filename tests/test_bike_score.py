import pytest


from bike_score_app import create_app
from bike_score_app import bike_score as module

from flask import json

TEST_REQUEST_CONTENT = {
	"total_distance": 1,
	"points_of_elevation": [1, 3.2, 5.0, 9.9, 2.3],
	"bike_lane_availability": 40,
    "safety_incidents": 1,
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


@pytest.mark.parametrize(('num_of_incidents', 'expected'), (
    (0, 100),
    (1, 50),
    (2, 33.3333),
    (3, 25),
    (4, 20),
))
def test_calculate_bike_safety_score(num_of_incidents, expected):
    actual = module.calculate_bike_safety_score(num_of_incidents)
    assert expected == actual


@pytest.mark.parametrize(('total_elevation_gain', 'total_distance', 'expected'), (
    (0, 1, 100),
    (201, 1, 0),
    (200, 1, 0),
    (100, 1, 50),
    (50, 2.5, 90),
    (100, 3, 83.3333),
))
def test_calculate_bike_grade_score(total_elevation_gain, total_distance, expected):
    actual = module.calculate_bike_grade_score(total_elevation_gain, total_distance)
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
            'bike_safety_score': 50,
            'bike_grade_score': 95.55,
        }
    }

    assert json.loads(response.data) == expected_response
