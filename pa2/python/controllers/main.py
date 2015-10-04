from utils import *
from flask import *
# -*- coding: utf-8 -*-

main = Blueprint('main', __name__, template_folder='views')

@main.route(appendKey('/'))
def main_route():
	cur = mysql.connection.cursor()
	cur.execute("SELECT username FROM User")
	msgs = cur.fetchall()
	if 'username' in session:
		hasLoginButton = False
		hasLogoutButton = True
	else:
		hasLogoutButton = False
		hasLoginButton = True
	return render_template("index.html", usernames=msgs, hasLoginButton=hasLoginButton, hasLogoutButton=hasLogoutButton)


#
# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     return redirect(url_for('index'))
