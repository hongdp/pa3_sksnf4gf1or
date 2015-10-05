from utils import *
from flask import *
import hashlib
import os
import time

user = Blueprint('user', __name__, template_folder='views')

@user.route(appendKey('/user'), methods=['GET', 'POST'])
def reg():

    # redirect to user/edit
    # if request.method == 'GET':
    # 	if 'username' in session:
    # 		return redirect(url)

    if request.method == 'POST':
        error = None
        username = request.form['username']
        con = mysql.connection
        cur = con.cursor()
        cur.execute("SELECT * FROM User WHERE username='%s'"%(username))
        exist = cur.fetchall()
        if exist:
            error = 'username already exist'
            return render_template('user.html',error=error)

        if request.form['password'] != request.form['re-password']:
            error = 'password does not match'
            return render_template('user.html',error=error)

        hash_password = hashlib.sha224(request.form['password']).hexdigest()
        cur.execute("INSERT INTO User VALUES ('%s', '%s', '%s', '%s', '%s')" % (request.form['username'], \
        request.form['firstname'], request.form['lastname'],hash_password , request.form['email']) )
        session['username'] = request.form['username']
        renewSession(session)
        con.commit()
        return redirect(url_for('main.main_route'))


    return render_template('user.html')
