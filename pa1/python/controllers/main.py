
from flask import *

main = Blueprint('main', __name__, template_folder='views')

@main.route('/sksnf4gf1or/pa1')
def main_route():
    return render_template("index.html")
