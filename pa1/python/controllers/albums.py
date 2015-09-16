from utils import appendKey, mysql
from flask import *

albums = Blueprint('albums', __name__, template_folder='views')

@albums.route(appendKey('/albums/edit'))
def albums_edit_route():
	options = {
		"edit": True
	}
	return render_template("albums.html", **options)


@albums.route(appendKey('/albums'))
def albums_route():

	username = request.args.get('username')
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM Album WHERE username =\'" + username+"\'")
	msgs = cur.fetchall()
	options = {
		"edit": False
	}
	return render_template("albums.html", albums=msgs, **options)
