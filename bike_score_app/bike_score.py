from flask import Blueprint, request, jsonify

bp = Blueprint('bike_score', __name__, url_prefix='/api')


@bp.route('/bike_score', methods=('POST', ))
def bike_score():
    # return 'hello bike score get'
    print(request.json)
    
    if request.method == 'POST':
        error = None
        
        # DO OTHER STUFF
        
        if error is not None:
            flash(error)
    
    return jsonify(
        {'bike_score': 79}
    )