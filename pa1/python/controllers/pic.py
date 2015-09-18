from utils import appendKey, mysql
from flask import *

pic = Blueprint('pic', __name__, template_folder='views')

@pic.route(appendKey('/pic'))
def pic_route():
	pic_id = request.args.get('id')
	cur = mysql.connection.cursor()
	cur.execute("SELECT url FROM Photo WHERE Photo.picid = '%s'" %(pic_id))
	msgs = cur.fetchall()
	cur.execute("SELECT albumid FROM Contain WHERE Contain.picid = '%s'" %(pic_id))
	msgs1 = cur.fetchall()
	options = {
		"url":msgs[0],
		"albumid":msgs1[0]
	}
	return render_template("pic.html", **options)