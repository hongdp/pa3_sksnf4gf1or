from utils import appendKey, mysql
from flask import *
import hashlib
import os
import time

album = Blueprint('album', __name__, template_folder='views')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'bmp', 'gif'])
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, '../static/img')
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@album.route(appendKey('/album/edit'), methods=['GET', 'POST'])
def album_edit_route():

	albumid = request.args.get('id')
	con = mysql.connection
	cur = con.cursor()
	#add img to static/img
	if request.method == 'POST':
		#add img to static/img
		if request.form['op'] == 'add':
			file = request.files['file']

			if file and allowed_file(file.filename):
				format = file.filename.rsplit('.', 1)[1]
				date = time.strftime('%Y-%m-%d', time.gmtime())
				picid = hashlib.sha224(file.filename+date).hexdigest()
				picname = picid + '.' + format
				url = '/static/img/'+picname
				file.save(os.path.join(UPLOAD_FOLDER,picname))
				# sqlcode = "INSERT INTO Album (title, created, lastupdated, username) VALUES ('%s', '%s', '%s', '%s')" % (title, date, date, username)
				# cur.execute(sqlcode)

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
