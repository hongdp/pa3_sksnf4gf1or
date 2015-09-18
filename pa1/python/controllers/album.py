from utils import appendKey, mysql
from flask import *

album = Blueprint('album', __name__, template_folder='views')

@album.route(appendKey('/album/edit'), methods = ['GET', 'POST'])
def album_edit_route():
	albumid = request.args.get('id')
	cur = mysql.connection.cursor()
	cur.execute("SELECT Photo.picid, url FROM Photo, Contain WHERE Photo.picid = Contain.picid AND Contain.albumid = '%s' ORDER BY sequencenum "%(albumid))
	photos = cur.fetchall()
	cur.execute("SELECT username, title FROM Album WHERE albumid = '%s'" %(albumid))
	albumInfo = cur.fetchall()
	options = {
		"edit": True,
		"photos": photos,
		"username": albumInfo[0][0],
		"albumname":albumInfo[0][1],
		"albumid": albumid,
	}
	return render_template("album.html", **options)

@album.route(appendKey('/album'), methods = ['GET'])
def album_route():

	albumid = request.args.get('id')
	cur = mysql.connection.cursor()
	cur.execute("SELECT Photo.picid, url FROM Photo, Contain WHERE Photo.picid = Contain.picid AND Contain.albumid = '%s' ORDER BY sequencenum "%(albumid))
	photos = cur.fetchall()
	cur.execute("SELECT username, title FROM Album WHERE albumid = '%s'" %(albumid))
	albumInfo = cur.fetchall()
	options = {
		"edit": False,
		"photos": photos,
		"username": albumInfo[0][0],
		"albumname":albumInfo[0][1],
		"albumid": albumid,
	}
	print options
	return render_template("album.html", **options)
