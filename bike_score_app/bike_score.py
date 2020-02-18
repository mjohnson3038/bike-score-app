import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('bike_score', __name__)

@bp.route('/bike_score', methods=('GET', 'POST', ))
def bike_score():
    # return 'hello bike score get'
    
    if request.method == 'POST':
        error = None
        
        # DO OTHER STUFF
        
        if error is not None:
            flash(error)
    
    return render_template('bike_score.html')