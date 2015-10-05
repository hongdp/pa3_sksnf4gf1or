from utils import *
from flask import *
import hashlib
import os
import time

album = Blueprint('album', __name__, template_folder='views')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'bmp', 'gif'])
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, '../static/pictures')
def allowed_file(filename):
    lowerFileName = filename.lower()
    print 
    return '.' in lowerFileName and lowerFileName.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@album.route(appendKey('/album/edit'), methods=['GET', 'POST'])
def album_edit_route():
    albumid = request.args.get('id')
    if not albumid:
        abort(404)
    con = mysql.connection
    cur = con.cursor()
    cur.execute("SELECT albumid, username FROM Album WHERE albumid=%s"%(albumid))
    album = cur.fetchall()
    if not album:
        abort(404)

# Authentication Codes
    if sessionExists(session):
        if sessionIsExpired(session):
            session.clear();
            return render_template('sessionExpire.html', login=False)
        else:
            if album[0][1] == session['username']:
                renewSession(session)
            else:
                return render_template('noAccess.html', login=True)
    else:
        return render_template('noLogin.html', login=False)
    if sessionExists(session):
        login = True
# Authentication Codes End

    #add picture to static/pictures
    if request.method == 'POST':
        #add picture to static/pictures
        if request.form['op'] == 'add':
            file = request.files['file']

            if file and allowed_file(file.filename):
                format = file.filename.rsplit('.', 1)[1]
                date = time.strftime('%Y-%m-%d', time.gmtime())
                curtime = time.strftime('%Y-%m-%d-%H-%M-%S', time.gmtime())
                picid = hashlib.sha224(file.filename+curtime).hexdigest()
                picname = picid + '.' + format
                url = '/static/pictures/'+picname
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                file.save(os.path.join(UPLOAD_FOLDER,picname))


                seqnum = 1
                sqlphoto = "INSERT INTO Photo (picid, url, format, date) VALUES ('%s', '%s', '%s', '%s')" % (picid, url, format, date)
                cur.execute(sqlphoto)
                con.commit()

                cur.execute("SELECT MAX(sequencenum) FROM Contain WHERE Contain.albumid = %s" %(albumid))
                maxseq = cur.fetchall()[0][0]
                if maxseq:
                    seqnum = maxseq+1

                sqlcontain = "INSERT INTO Contain (albumid, picid, caption, sequencenum) VALUES(%s, '%s', '', %d )" %(albumid, picid, seqnum)
                cur.execute(sqlcontain)
                con.commit()

        if request.form['op'] == 'delete':
            picid = request.form['photoid']
            sqlcontain = "DELETE FROM Contain WHERE Contain.picid = '%s'" %(picid)
            cur.execute(sqlcontain)
            con.commit()

            sqlphoto = "SELECT url FROM Photo WHERE Photo.picid = '%s'" %(picid)
            cur.execute(sqlphoto)
            msgsurl = cur.fetchall()
            url = msgsurl[0][0]

            sqlphoto = "DELETE FROM Photo WHERE Photo.picid = '%s'" %(picid)
            cur.execute(sqlphoto)
            con.commit()

            url = ".." + url
            os.remove(os.path.join(APP_ROOT, url))

    cur.execute("SELECT Photo.picid, url FROM Photo, Contain WHERE Photo.picid = Contain.picid AND Contain.albumid = '%s' ORDER BY sequencenum "%(albumid))
    photos = cur.fetchall()
    cur.execute("SELECT username, title FROM Album WHERE albumid = '%s'" %(albumid))
    albumInfo = cur.fetchall()
    options = {
        "edit": True,
        "photos": photos,
        "username": albumInfo[0][0],
        "albumname":albumInfo[0][1],
        "albumid": albumid,
        "login": login
    }
    return render_template("album.html", **options)

@album.route(appendKey('/album'), methods = ['GET'])
def album_route():

    albumid = request.args.get('id')
    if not albumid:
        abort(404)
    cur = mysql.connection.cursor()
    cur.execute("SELECT albumid, username, access FROM Album WHERE albumid=%s"%(albumid))
    album = cur.fetchall()
    if not album:
        abort(404)
        
# Authentication Codes
    if album[0][2] == 'private':
        if sessionExists(session):
            if sessionIsExpired(session):
                session.clear();
                return render_template('sessionExpire.html', login=False)
            else:
                if album[0][1] == session['username']:
                    renewSession(session)
                else:
                    cur.execute("SELECT username FROM AlbumAccess WHERE albumid=%s and username='%s'"%(albumid, session['username']))
                    authUser = cur.fetchall()
                    if authUser:
                        renewSession(session)
                    else:
                        return render_template('noAccess.html', login=True)
        else:
            return render_template('noLogin.html', login=False)
    else:
        if sessionExists(session):
            if sessionIsExpired(session):
                print 'session expired'
                session.clear();
            else:
                renewSession(session)
    login = False
    if sessionExists(session):
        login = True
# Authentication Codes End

    cur.execute("SELECT Photo.picid, url FROM Photo, Contain WHERE Photo.picid = Contain.picid AND Contain.albumid = '%s' ORDER BY sequencenum "%(albumid))
    photos = cur.fetchall()
    cur.execute("SELECT username, title FROM Album WHERE albumid = '%s'" %(albumid))
    albumInfo = cur.fetchall()
    options = {
        "edit": False,
        "photos": photos,
        "username": albumInfo[0][0],
        "albumname":albumInfo[0][1],
        "albumid": albumid,
        "login": login
    }
    print options
    return render_template("album.html", **options)
