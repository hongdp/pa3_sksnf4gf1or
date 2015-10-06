from utils import *
from flask import *
import hashlib
import os
import time
from flask_mail import Message

user = Blueprint('user', __name__, template_folder='views')
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@user.route(appendKey('/user'), methods=['GET', 'POST'])
def reg():

    # redirect to user/edit
    if request.method == 'GET':
        if 'username' in session:
     	      return redirect(url_for('useredit.edit'))

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

        msg = Message("Congratulation! Your just started journey to the Great Album Wall!", \
        recipients=[request.form['email']])
        mail.send(msg)

        cur.execute("INSERT INTO User VALUES ('%s', '%s', '%s', '%s', '%s')" % (request.form['username'], \
        request.form['firstname'], request.form['lastname'],hash_password , request.form['email']) )
        session['username'] = request.form['username']
        renewSession(session)
        con.commit()
        return redirect(url_for('main.main_route'))


    return render_template('user.html')

@user.route(appendKey('/user/delete'), methods=['POST'])
def deleteUser():
    # redirect to user/edit
    # if request.method == 'GET':
    #   if 'username' in session:
    #       return redirect(url)
    if not sessionExists(session):
        return render_template("noLogin.html")
    elif sessionIsExpired(session):
        session.clear()
        return render_template("sessionExpire.html")

    username = session['username']
    con = mysql.connection
    cur = con.cursor()
    cur.execute("SELECT * FROM User WHERE username='%s'"%(username))
    exist = cur.fetchall()
    if not exist:
        abort(404)
    cur.execute("SELECT Photo.picid, Photo.url FROM User, Album, Contain, Photo WHERE User.username = Album.username AND Album.albumid = Contain.albumid AND Contain.picid = Photo.picid AND User.username = '%s'"%(username))
    pics = cur.fetchall();
    cur.execute("DELETE FROM Photo WHERE Photo.picid IN (SELECT Contain.picid as picid FROM User, Album, Contain WHERE User.username = Album.username AND Album.albumid = Contain.albumid AND User.username = '%s')"%(username))
    con.commit()
    for pic in pics:
        url = '..'+pic[1]
        os.remove(os.path.join(APP_ROOT, url))
    cur.execute("DELETE FROM User WHERE username = '%s'"%(username))
    con.commit()
    session.clear()
    return redirect(url_for('main.main_route'))
