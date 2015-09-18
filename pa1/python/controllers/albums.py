from utils import appendKey, mysql
from flask import *
import time

albums = Blueprint('albums', __name__, template_folder='views')

@albums.route(appendKey('/albums/edit'), methods=['GET', 'POST'])
def albums_edit_route():
	username = request.args.get('username')
	con = mysql.connection
	cur = con.cursor()
	if request.method == 'POST':
		if request.form['op'] == 'delete':
			cur.execute("DELETE FROM Album WHERE albumid = '%s'"%(request.form['albumid']))	
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
	username = request.args.get('username')
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM Album WHERE username ='%s'"%(username))
	msgs = cur.fetchall()
	options = {
		"edit": False
	}
	return render_template("albums.html", username = username, albums=msgs, **options)
