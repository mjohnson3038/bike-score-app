from flask import Blueprint, request, jsonify, flash

bp = Blueprint('bike_score', __name__, url_prefix='/api')


def calculate_bike_lane_availability_score(bike_lane_availability):
    return bike_lane_availability


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


@bp.route('/bike_score', methods=('POST', ))
def bike_score():

    if request.method == 'POST':
        error = None

        bike_lane_availability = request.json.get('bike_lane_availability')
        points_of_elevation = request.json.get('points_of_elevation')
        safety_incidents = request.json.get('safety_incidents')

        if not bike_lane_availability:
            print('bad formatting, need a better way to handle this')
        if not points_of_elevation:
            print('bad formatting, need a better way to handle this')
        if not safety_incidents:
            print('bad formatting, need a better way to handle this')

        if error is not None:
            print(error)

        content = {
            'bike_score': 79,
            'bike_lane_availability_score': bike_lane_availability,
            'total_elevation_gain': calculate_elevation_gain(points_of_elevation), # feet
            'net_elevation_gain': calculate_net_elevation_gain(points_of_elevation), # feet
            'safety_incidents': safety_incidents,
        }

    return jsonify(
        {
            'data': content,
        }
    )
