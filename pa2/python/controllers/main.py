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
		hasLoginButton = False
		hasLogoutButton = True
		print session['username']
		username = session['username']
		return render_template("index.html", username=username, hasLoginButton=hasLoginButton, hasLogoutButton=hasLogoutButton)
	elif sessionIsExpired(session):
		session.clear()

	hasLogoutButton = False
	hasLoginButton = True
	return render_template("index.html", username=username, hasLoginButton=hasLoginButton, hasLogoutButton=hasLogoutButton)




#
# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     return redirect(url_for('index'))
