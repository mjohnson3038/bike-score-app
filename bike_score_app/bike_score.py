import json
from flask import Blueprint, current_app, request, jsonify, flash
from .constants import SAMPLE_GOOGLE_DIRECTIONS_RESPONSE_200

bp = Blueprint('bike_score', __name__, url_prefix='/api')


def get_google_route(origin, desitination):
    return SAMPLE_GOOGLE_RESPONSE_200


def calculate_net_elevation_gain(elevation_points):
    if len(elevation_points) < 2:
        return 0

    net_change = elevation_points[-1] - elevation_points[0]
    return round(net_change, 4)


def calculate_elevation_gain(elevation_points):
    '''
    elevation_points - array of elevation points

    Calculates elevation gain without subtracting any negative elevation.
    '''
    if len(elevation_points) < 2:
        return 0

    total_elevation_gain = 0
    current_elevation = elevation_points[0]

    for i in range(1, len(elevation_points)):
        elevation_change = elevation_points[i] - current_elevation

        if elevation_change > 0:
            total_elevation_gain += elevation_change

        current_elevation = elevation_points[i]

    return total_elevation_gain


def calculate_bike_lane_availability_score(bike_lane_availability):
    return bike_lane_availability


def calculate_bike_safety_score(safety_incidents):
    '''
    Initial safety incidents carry more weight to the score than subsequent ones.
    '''
    if safety_incidents == 0:
        return 100

    score = (100 / (1 + safety_incidents))
    return round(score, 4)


def calculate_bike_grade_score(total_elevation_gain, distance):
    '''
    total_elevation_gain - total elevation gained on the bike ride, in feet
    distance - distance of route, in miles

    My personal experience:

    50 ft/ mile - good challenge
    100 feet / mile - breathing hard
    over 200 feet / mile - I'm walking
    '''

    elevation_per_miles = total_elevation_gain / distance
    rounded_elevation_per_miles = round(elevation_per_miles, 4)
    if elevation_per_miles > 200:
        return 0

    return round(100 - (1/2) * elevation_per_miles, 4)


def calculate_bike_score(bike_lane_availability_score, bike_safety_score, bike_grade_score):
    '''
    The bike score is out of 100 and equal parts all subscores. This score is
    comprised of `bike_lane_availability_score`, `bike_safety_score`, and `bike_grade_score`.
    '''

    sum_of_scores = bike_lane_availability_score + bike_safety_score + bike_grade_score
    return round(sum_of_scores/3, 0)


get_value = lambda raw_value, clean_function: None if raw_value is None else clean_function(raw_value)


@bp.route('/bike_score', methods=('GET', ))
def bike_score():
    if request.method == 'GET':
        bike_lane_availability = get_value(request.args.get('bike_lane_availability'), int)
        points_of_elevation = get_value(request.args.get('points_of_elevation'), json.loads)
        safety_incidents = get_value(request.args.get('safety_incidents'), int)
        total_distance = get_value(request.args.get('total_distance'), float)

        if not bike_lane_availability:
            return "`bike_lane_availability` is a required field and must be included in the parameters.", 400
        if not points_of_elevation:
            return "`points_of_elevation` is a required field and must be included in the parameters.", 400
        if not safety_incidents:
            return "`safety_incidents` is a required field and must be included in the parameters.", 400
        if not total_distance:
            return "`total_distance` is a required field and must be included in the parameters.", 400

        total_elevation_gain = calculate_elevation_gain(points_of_elevation)
        bike_lane_availability_score = calculate_bike_lane_availability_score(bike_lane_availability)
        bike_safety_score = calculate_bike_safety_score(safety_incidents)
        bike_grade_score = calculate_bike_grade_score(total_elevation_gain, total_distance)
        bike_score = calculate_bike_score(bike_lane_availability_score, bike_safety_score, bike_grade_score)

        content = {
            'bike_score': bike_score,
            'bike_lane_availability_score': bike_lane_availability_score,
            'bike_safety_score': bike_safety_score,
            'bike_grade_score': bike_grade_score,
        }

        return {
            'data': content,
        }

    if __name__ == '__main__':
        print('hello world')
