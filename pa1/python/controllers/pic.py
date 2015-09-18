from utils import appendKey, mysql
from flask import *

pic = Blueprint('pic', __name__, template_folder='views')

@pic.route(appendKey('/pic'))
def pic_route():
	pic_id = request.args.get('id')
	cur = mysql.connection.cursor()
	cur.execute("SELECT url FROM Photo WHERE Photo.picid = '%s'" %(pic_id))
	msgs = cur.fetchall()
	cur.execute("SELECT albumid FROM Contain WHERE Contain.picid = '%s'" %(pic_id))
	msgs1 = cur.fetchall()

	cur.execute("SELECT sequencenum FROM Contain WHERE Contain.picid = '%s'" %(pic_id))
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
		"prev": prev,
		"next": nxt
	}

 	return render_template("pic.html", **options)
