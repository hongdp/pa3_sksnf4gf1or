def getUserInfoFromSession(session, mysql):
	if 'username' in session:
		ur = mysql.connection.cursor()
		cur.execute("SELECT * FROM User WHERE User.username = '%s'" %(session['username']))
		msgs = cur.fetchall()
		if msgs:
			return msgs;
	return None;

def checkAccessibilityOfSession(session, mysql, albumid):
	if 'username' in session:
		ur = mysql.connection.cursor()
		cur.execute("SELECT * FROM AlbumAccess WHERE username = '%s' AND albumid = '%s'" %(session['username'], albumid))
		msgs = cur.fetchall()
		if msgs:
			return True;
	return False;
