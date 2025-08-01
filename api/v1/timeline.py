from flask import Blueprint, render_template
from api.data import events

timeline_bp = Blueprint('timeline', __name__, url_prefix='/timeline')

@timeline_bp.route('/')
def timeline():
    return render_template('timeline.html', events=events) 