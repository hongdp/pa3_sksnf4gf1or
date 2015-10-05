from utils import appendKey, mysql
from flask import *
import hashlib
import os
import time

user = Blueprint('user', __name__, template_folder='views')

@user.route(appendKey('/user'), methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        if request.form['password'] == request.form['re-password']:
            con = mysql.connection
            cur = con.cursor()
            cur.execute("INSERT INTO User VALUES ('%s', '%s', '%s', '%s', '%s')" % (request.form['username'], \
            request.form['firstname'], request.form['lastname'], request.form['password'], request.form['email']) )
            session['username'] = request.form['username']
            con.commit()
            return redirect(url_for('main.main_route'))


    return render_template('user.html')
