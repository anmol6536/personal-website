from flask import Blueprint, render_template
from api.data import projects, publications

work_bp = Blueprint('work', __name__, url_prefix='/work')

@work_bp.route('/')
def work_page():
    return render_template('work.html', projects=projects, publications=publications) 