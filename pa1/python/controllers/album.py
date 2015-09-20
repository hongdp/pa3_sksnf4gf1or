from utils import appendKey, mysql
from flask import *
import hashlib
import os
import time

album = Blueprint('album', __name__, template_folder='views')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'bmp', 'gif'])
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, '../static/img')
def allowed_file(filename):
    filename.lower()
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@album.route(appendKey('/album/edit'), methods=['GET', 'POST'])
def album_edit_route():

    albumid = request.args.get('id')
    con = mysql.connection
    cur = con.cursor()
    #add img to static/img
    if request.method == 'POST':
        #add img to static/img
        if request.form['op'] == 'add':
            file = request.files['file']

            if file and allowed_file(file.filename):
                format = file.filename.rsplit('.', 1)[1]
                date = time.strftime('%Y-%m-%d', time.gmtime())
                curtime = time.strftime('%Y-%m-%d-%H-%M-%S', time.gmtime())
                picid = hashlib.sha224(file.filename+curtime).hexdigest()
                picname = picid + '.' + format
                url = '/static/img/'+picname
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
    }
    return render_template("album.html", **options)

@album.route(appendKey('/album'), methods = ['GET'])
def album_route():

    albumid = request.args.get('id')
    cur = mysql.connection.cursor()
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
    }
    print options
    return render_template("album.html", **options)
