from utils import *
from flask import *

pic = Blueprint('pic', __name__, template_folder='views')

@pic.route(appendKey('/pic'), methods=['GET', 'POST'])
def pic_route():
	if request.method == 'GET':
		pic_id = request.args.get('id')
		cur = mysql.connection.cursor()
		cur.execute("SELECT url FROM Photo WHERE Photo.picid = '%s'" %(pic_id))
		msgs = cur.fetchall()
		if not msgs:
			abort(404)
		cur.execute("SELECT albumid FROM Contain WHERE Contain.picid = '%s'" %(pic_id))
		msgs1 = cur.fetchall()
	# Authentication Codes
		cur.execute("SELECT albumid, username, access FROM Album WHERE Album.albumid = '%s'"%(msgs1[0][0]))
		access = cur.fetchall()
		if access[0][2] == 'private':
			if sessionExists(session):
				if sessionIsExpired(session):
					session.clear();
					return render_template('sessionExpire.html', login=False)
				else:
					if access[0][1] == session['username']:
						renewSession(session)
					else:
						cur.execute("SELECT username FROM AlbumAccess WHERE albumid=%s and username='%s'"%(access[0][0], session['username']))
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
					# print 'session expired'
					session.clear();
				else:
					renewSession(session)
		login = False
		if sessionExists(session):
			login = True
	# Authentication Codes End

		cur.execute("SELECT sequencenum, caption FROM Contain WHERE Contain.picid = '%s'" %(pic_id))
		msgs2 = cur.fetchall()
		cur.execute("SELECT picid, sequencenum FROM Contain WHERE Contain.albumid = %d AND Contain.sequencenum < %d ORDER BY sequencenum" %(msgs1[0][0], msgs2[0][0]))
		msgs3 = cur.fetchall()
		cur.execute("SELECT picid, sequencenum FROM Contain WHERE Contain.albumid = %d AND Contain.sequencenum > %d ORDER BY sequencenum" %(msgs1[0][0], msgs2[0][0]))
		msgs4 = cur.fetchall()

		prev = ''
		nxt = ''

		if msgs3:
			prev = msgs3[-1][0]

		if msgs4:
			nxt = msgs4[0][0]




		options = {
			"url":msgs[0],
			"albumid":msgs1[0],
			"caption": msgs2[0][1],
			"prev": prev,
			"next": nxt,
			"login": login
		}

		return render_template("pic.html", **options)

	else:
		pic_id = request.args.get('id')
		con = mysql.connection
		cur = con.cursor()
		cur.execute("SELECT url FROM Photo WHERE Photo.picid = '%s'" %(pic_id))
		msgs = cur.fetchall()
		if not msgs or not request.form['caption']:
			abort(404)
		cur.execute("UPDATE Contain SET caption = '%s' WHERE Contain.picid = '%s'" %(request.form['caption'], pic_id))
		con.commit()
		return redirect(url_for('pic.pic_route')+'?id=%s'%(pic_id))
