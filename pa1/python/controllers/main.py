from utils import appendKey
from flask import *

main = Blueprint('main', __name__, template_folder='views')

@main.route(appendKey('/'))
def main_route():
    return render_template("index.html")
