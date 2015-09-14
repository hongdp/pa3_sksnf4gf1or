from utils import appendKey
from flask import *

main = Blueprint('main', __name__, template_folder='views')

@main.route(appendKey('/pa1'))
def main_route():
    return render_template("index.html")
