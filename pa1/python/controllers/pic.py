from utils import appendKey
from flask import *

pic = Blueprint('pic', __name__, template_folder='views')

@pic.route(appendKey('/pic'))
def pic_route():
	return render_template("pic.html")