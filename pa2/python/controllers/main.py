from utils import *
from flask import *
# -*- coding: utf-8 -*-

main = Blueprint('main', __name__, template_folder='views')

@main.route(appendKey('/'))
def main_route():
	con = mysql.connection
	cur = con.cursor()
	if sessionIsValid(session):
		cur.execute("SELECT albumid, title FROM Album WHERE access='public' OR username='%s' UNION SELECT albumid, title FROM AlbumAccess, Album WHERE AlbumAccess.albumid = Album.albumid AND AlbumAccess.username='%s'"%(session['username'], session['username']))
		hasLoginButton = False
		hasLogoutButton = True
		return render_template("index.html", usernames=session[username], hasLoginButton=hasLoginButton, hasLogoutButton=hasLogoutButton, albums=albums)
	elif sessionIsExpired(session):
		session.clear()
	cur.execute("SELECT albumid, title FROM Album WHERE access='public'")
	albums = cur.fetchall()
	hasLogoutButton = False
	hasLoginButton = True
	return render_template("index.html", hasLoginButton=hasLoginButton, hasLogoutButton=hasLogoutButton, albums=albums)

	


#
# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     return redirect(url_for('index'))
