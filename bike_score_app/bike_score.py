from flask import Blueprint, request, jsonify, flash

bp = Blueprint('bike_score', __name__, url_prefix='/api')


def calculate_bike_lane_availability_score(bike_lane_availability):
    return bike_lane_availability


@bp.route('/bike_score', methods=('POST', ))
def bike_score():

    if request.method == 'POST':
        error = None

        bike_lane_availability = request.json.get('bike_lane_availability')

        if not bike_lane_availability:
            print('bad formatting, need a better way to handle this')

        if error is not None:
            print(error)

        content = {
            'bike_score': 79,
            'bike_lane_availability_score': bike_lane_availability,
        }

    return jsonify(
        {
            'data': content,
        }
    )
