from utils import *
from flask import *
# -*- coding: utf-8 -*-

main = Blueprint('main', __name__, template_folder='views')

@main.route(appendKey('/'))
def main_route():
	con = mysql.connection
	cur = con.cursor()
	username = ''
	if sessionIsValid(session):
		renewSession(session)
		cur.execute("SELECT albumid, title, username FROM (SELECT albumid, title, \
		username FROM Album WHERE access='public' OR username='%s' UNION SELECT \
		Album.albumid as albumid, title, Album.username FROM AlbumAccess, Album \
		WHERE AlbumAccess.albumid = Album.albumid AND AlbumAccess.username='%s') \
		as t1 ORDER BY username"%(session['username'], session['username']))
		albums = cur.fetchall()
		print session['username']
		return render_template("index.html", username=session['username'], login=True, albums=albums)
	elif sessionIsExpired(session):
		session.clear()
	cur.execute("SELECT albumid, title FROM Album WHERE access='public' ORDER BY username")
	albums = cur.fetchall()
	return render_template("index.html", login=False, albums=albums)


#
# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     return redirect(url_for('index'))
