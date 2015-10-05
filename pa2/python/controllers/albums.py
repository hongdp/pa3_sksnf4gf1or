from utils import *
from flask import *
import time, os

albums = Blueprint('albums', __name__, template_folder='views')
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@albums.route(appendKey('/albums/edit'), methods=['GET', 'POST'])
def albums_edit_route():
    username = request.args.get('username')
    if not username:
        abort(404)
    con = mysql.connection
    cur = con.cursor()
    cur.execute("SELECT * FROM User WHERE username='%s'"%(username))
    user = cur.fetchall()
    if not user:
        abort(404)
    if request.method == 'POST':
        if request.form['op'] == 'delete':
            albumid = request.form['albumid']
            sql_get_picids = "SELECT picid FROM Contain WHERE Contain.albumid = %s" %(albumid)
            cur.execute(sql_get_picids)
            picids = cur.fetchall()
            cur.execute("DELETE FROM Contain WHERE Contain.albumid = %s" %(albumid))
            for picid_row in picids:
                picid = picid_row[0]
                sql_pic_from_contain = "DELETE FROM Contain WHERE Contain.picid = '%s'" %(picid)
                cur.execute(sql_pic_from_contain)
                con.commit()

                sql_url_from_photo = "SELECT url FROM Photo WHERE Photo.picid = '%s'" %(picid)
                cur.execute(sql_url_from_photo)
                msgsurl = cur.fetchall()
                url = msgsurl[0][0]

                sql_delete_photo = "DELETE FROM Photo WHERE Photo.picid = '%s'" %(picid)
                cur.execute(sql_delete_photo)
                con.commit()

                url = ".." + url
                os.remove(os.path.join(APP_ROOT, url))
            cur.execute("DELETE FROM Album WHERE albumid = '%s'"%(albumid))

        if request.form['op'] == 'add':
            title = request.form['title']
            date = time.strftime('%Y-%m-%d', time.gmtime())
            sqlcode = "INSERT INTO Album (title, created, lastupdated, username) VALUES ('%s', '%s', '%s', '%s')" % (title, date, date, username)
            cur.execute(sqlcode)
            cur.execute("SELECT LAST_INSERT_ID()")
            id = cur.fetchall()
            con.commit()
    cur.execute("SELECT * FROM Album WHERE username ='%s'"%(username))
    msgs = cur.fetchall()
    con.commit()
    options = {
        "edit": True
    }
    return render_template("albums.html", albums=msgs, username = username, **options)


@albums.route(appendKey('/albums'), methods=['GET'])
def albums_route():
    username = ''
    con = mysql.connection
    cur = con.cursor()
    msgs = {}
    if sessionIsValid(session):
        username = session['username']

        cur.execute("SELECT * FROM Album WHERE username='%s'"%(username))
        msgs = cur.fetchall()
        options = {
            "edit": False
        }
        return render_template("albums.html", username = username, albums=msgs, **options)
    elif sessionIsExpired(session):
		session.clear()

    cur.execute("SELECT * FROM Album WHERE access ='public'")
    msgs = cur.fetchall()
    options = {
        "edit": False
    }
    return render_template("albums.html", username = username, albums=msgs, **options)
