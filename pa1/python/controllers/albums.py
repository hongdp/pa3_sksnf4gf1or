from utils import appendKey
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
	options = {
		"edit": False
	}
	return render_template("albums.html", **options)