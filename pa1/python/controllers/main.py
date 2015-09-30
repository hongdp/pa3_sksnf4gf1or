from utils import appendKey, mysql, secretKey
from flask import *
# -*- coding: utf-8 -*-

main = Blueprint('main', __name__, template_folder='views')

@main.route(appendKey('/'))
def main_route():
	cur = mysql.connection.cursor()
	cur.execute("SELECT username FROM User")
	msgs = cur.fetchall()
	return render_template("index.html", usernames=msgs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return ''


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
