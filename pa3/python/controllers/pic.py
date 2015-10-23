from utils import *
from flask import *

pic = Blueprint('pic', __name__, template_folder='views')

@pic.route(appendKey('/pic'), methods=['GET', 'POST'])
def pic_route():
	owner = False
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
				elif access[0][1] == session['username']:
					owner = True
					renewSession(session)
				else:
					renewSession(session)
					cur.execute("SELECT username FROM AlbumAccess WHERE albumid=%s and username='%s'"%(access[0][0], session['username']))
					authUser = cur.fetchall()
					if not authUser:
						return render_template('noAccess.html', login=True), 403
			else:
				return render_template('noLogin.html', login=False), 403
		else:
			if sessionExists(session):
				if sessionIsExpired(session):
					# print 'session expired'
					session.clear();
				else:
					renewSession(session)
					if access[0][1] == session['username']:
						owner = True
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
			"login": login,
			"owner": owner
		}

		return render_template("pic.html", **options)

	else:
		pic_id = request.args.get('id')
		con = mysql.connection
		cur = con.cursor()
		cur.execute("SELECT url FROM Photo WHERE Photo.picid = '%s'" %(pic_id))
		msgs = cur.fetchall()
		cur.execute("SELECT username FROM Contain, Album WHERE Contain.albumid=Album.albumid AND Contain.picid = '%s'" %(pic_id))
		owner = cur.fetchall()
		if sessionExists(session):
			if sessionIsExpired(session):
				session.clear()
				return render_template('sessionExpire.html', login=False)
			elif owner[0][0] == session['username']:
				renewSession(session)
			else:
				return render_template('noAccess.html', login=True), 403

		if not msgs or not request.form['caption']:
			abort(404)
		cur.execute("UPDATE Contain SET caption = '%s' WHERE Contain.picid = '%s'" %(request.form['caption'], pic_id))
		con.commit()
		return redirect(url_for('pic.pic_route')+'?id=%s'%(pic_id))


@pic.route('/caption', methods=['GET'])
def pic_caption_get():
    '''
    Expects URL query parameter with picid.
    Returns JSON with the picture's current caption or error.
    {
        "caption": "current caption"
    }
    {
        "error": "error message",
        "status": 422
    }
    '''
    try:
        picid = get_picid(request)
    except InvalidPicIDError as err:
        response = json.jsonify(error='Could not retrieve caption. You did not provide a picture id.', status=404)
        response.status_code = 404
        return response


    query = "SELECT caption FROM Contain WHERE picid='%s';" % (picid)
    results = application.execute(query)
    caption = None
    if len(results) > 0:
        caption = results[0][0]
    else:
        response = json.jsonify(error='Could not retrieve caption. You did not provide a valid picture id.', status=422)
        response.status_code = 422
        return response
    return json.jsonify(caption=caption)

@pic.route('/caption', methods=['POST'])
def pic_caption_post():
    '''
    Expects JSON POST of the format:
    {
        "caption": "this is the new caption",
        "id": "picid"
    }
    Updates the caption and sends a response of the format
    {
        "id": "picid",
        "status": 201
    }
    Or if an error occurs:
    {
        "error": "error message",
        "status": 422
    }
    '''
    req_json = request.get_json()

    picid = req_json.get('id')
    caption = req_json.get('caption')
    if picid is None and caption is None:
        response.json.jsonify(error='Could not update caption. You did not provide a valid picture id or caption.', status=404)
        response.status_code = 404
        return response
    if picid is None:
        response = json.jsonify(error='Could not update caption. You did not provide a valid picture id.', status=404)
        response.status_code = 404
        return
    if caption is None:
        response = json.jsonify(error='Could not update caption. You did not provide a valid caption.', status=404)
        response.status_code = 404
        return response

    try:
        query = "UPDATE Contain SET caption='%s' WHERE picid='%s';" % (caption, picid)
        application.update(query)
    except InvalidPicIDError as e:
        response = json.jsonify(error='Could not update caption. The picture id was not valid.', status=422)
        response.status_code = 422
        return response

    response = json.jsonify(id=picid, status=201)
    response.status_code = 201
    return response
