from utils import appendKey, mysql
from flask import *

album = Blueprint('album', __name__, template_folder='views')

@album.route(appendKey('/album/edit'))
def album_edit_route():
	options = {
		"edit": True
	}
	return render_template("album.html", **options)

@album.route(appendKey('/album'), methods = ['GET'])
def album_route():

	albumid = request.args.get('id')
	cur = mysql.connection.cursor()
	cur.execute("SELECT picid, url FROM Photo, Contain WHERE Photo.picid = Contain.picid AND Contain.albumid = '%s' ORDER BY sequencenum "%(albumid))
	msgs = cur.fetchall()
	cur.execute("SELECT title FROM Album WHERE albumid = '%s'" %(albumid))
	msgs1 = cur.fetchall()
	options = {
		"edit": False,
		"photos": msgs,
		"albumname":msgs1[0]
	}
	return render_template("album.html", **options)
