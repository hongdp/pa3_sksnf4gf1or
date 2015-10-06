from utils import *
from flask import *
import hashlib
import os
import time

useredit = Blueprint('useredit', __name__, template_folder='views')

@useredit.route(appendKey('/user/edit'), methods=['GET', 'POST'])
def edit():
    username = ''
    con = mysql.connection
    cur = con.cursor()
    msgs = {}
    #auth code
    if not sessionExists(session):
        return render_template('noLogin.html', login=False)
    elif sessionIsExpired(session):
        session.clear()
        return render_template('sessionExpire.html', login=False)
    else:
        username = session['username']
        cur.execute("SELECT * FROM User WHERE username='%s'"%(username))
        userinfo = cur.fetchall()
        if not userinfo:
            session.clear();
            return render_template('noLogin.html', login=False)
        else:
            options = {
                "login": True,
                "userinfo": userinfo[0]
            }

    return render_template("edit.html", **options)
