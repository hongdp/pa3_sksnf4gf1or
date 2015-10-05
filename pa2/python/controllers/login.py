from utils import *
from flask import *
import hashlib
import os
import time

login = Blueprint('login', __name__, template_folder='views')

@login.route(appendKey('/user/login'), methods=['GET', 'POST'])
def login_func():
    url = request.args.get('url')
    if request.method == 'GET':
    	if 'username' in session:
    		return redirect(url)
    if request.method == 'POST':
        error = None
        username = request.form['username']
        hash_password = hashlib.sha224(request.form['password']).hexdigest()[0:20]
        con = mysql.connection
        cur = con.cursor()
        cur.execute("SELECT username, password FROM User WHERE username='%s'"%(username))
        userinfo = cur.fetchall()
        if not userinfo:
            error = 'Username does not exist'
            return render_template('login.html',error = error)

        if userinfo[0][1] != hash_password:
            error = 'password incorrent'
            return render_template('login.html',error = error)

        flash('You were successfully logged in')
        session['username'] = request.form['username']
        renewSession(session)
        return redirect(url)
    return render_template('login.html')

@login.route(appendKey('/logout'), methods=['GET'])
def logout_func():
    session.clear();
    return redirect(url_for('main.main_route'))
