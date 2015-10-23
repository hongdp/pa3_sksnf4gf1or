from utils import *
from flask import *

pic = Blueprint('pic', __name__, template_folder='views')


@pic.route(append_key('/pic'), methods=['GET', 'POST'])
def pic_route():
    owner = False
    if request.method == 'GET':
        pic_id = request.args.get('id')
        cur = mysql.connection.cursor()
        cur.execute("SELECT url FROM Photo WHERE Photo.picid = '%s'" % (pic_id))
        msgs = cur.fetchall()
        if not msgs:
            abort(404)
        cur.execute("SELECT albumid FROM Contain WHERE Contain.picid = '%s'" % (pic_id))
        msgs1 = cur.fetchall()
        # Authentication Codes
        cur.execute("SELECT albumid, username, access FROM Album WHERE Album.albumid = '%s'" % (msgs1[0][0]))
        access = cur.fetchall()
        if access[0][2] == 'private':
            if session_exists(session):
                if session_is_expired(session):
                    session.clear()
                    return render_template('sessionExpire.html', login=False)
                elif access[0][1] == session['username']:
                    owner = True
                    renew_session(session)
                else:
                    renew_session(session)
                    cur.execute("SELECT username FROM AlbumAccess WHERE albumid=%s and username='%s'" % (
                        access[0][0], session['username']))
                    auth_user = cur.fetchall()
                    if not auth_user:
                        return render_template('noAccess.html', login=True), 403
            else:
                return render_template('noLogin.html', login=False), 403
        else:
            if session_exists(session):
                if session_is_expired(session):
                    # print 'session expired'
                    session.clear()
                else:
                    renew_session(session)
                    if access[0][1] == session['username']:
                        owner = True
        login = False
        if session_exists(session):
            login = True
            # Authentication Codes End

        cur.execute("SELECT sequencenum, caption FROM Contain WHERE Contain.picid = '%s'" % (pic_id))
        msgs2 = cur.fetchall()
        cur.execute(
            "SELECT picid, sequencenum FROM Contain WHERE Contain.albumid = %d AND Contain.sequencenum < %d ORDER BY sequencenum" % (
                msgs1[0][0], msgs2[0][0]))
        msgs3 = cur.fetchall()
        cur.execute(
            "SELECT picid, sequencenum FROM Contain WHERE Contain.albumid = %d AND Contain.sequencenum > %d ORDER BY sequencenum" % (
                msgs1[0][0], msgs2[0][0]))
        msgs4 = cur.fetchall()

        prev = ''
        nxt = ''

        if msgs3:
            prev = msgs3[-1][0]

        if msgs4:
            nxt = msgs4[0][0]

        options = {
            "url": msgs[0],
            "albumid": msgs1[0],
            "caption": msgs2[0][1],
            "prev": prev,
            "next": nxt,
            "login": login,
            "owner": owner,
            "id": pic_id
        }

        return render_template("pic.html", **options)

    else:
        pic_id = request.args.get('id')
        con = mysql.connection
        cur = con.cursor()
        cur.execute("SELECT url FROM Photo WHERE Photo.picid = '%s'" % (pic_id))
        msgs = cur.fetchall()
        cur.execute(
            "SELECT username FROM Contain, Album WHERE Contain.albumid=Album.albumid AND Contain.picid = '%s'" % (
                pic_id))
        owner = cur.fetchall()
        if session_exists(session):
            if session_is_expired(session):
                session.clear()
                return render_template('sessionExpire.html', login=False)
            elif owner[0][0] == session['username']:
                renew_session(session)
            else:
                return render_template('noAccess.html', login=True), 403

        if not msgs or not request.form['caption']:
            abort(404)
        cur.execute("UPDATE Contain SET caption = '%s' WHERE Contain.picid = '%s'" % (request.form['caption'], pic_id))
        con.commit()
        return redirect(url_for('pic.pic_route') + '?id=%s' % (pic_id))


@pic.route(append_key('/pic/caption'), methods=['GET'])
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
    picid = request.args.get('id')
    if picid is None:
        response = json.jsonify(error='Could not retrieve caption. You did not provide a picture id.', status=404)
        response.status_code = 404
        return response

    query = "SELECT caption FROM Contain WHERE picid='%s';" % (picid)
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()
    if len(results) > 0:
        caption = results[0][0]
        return json.jsonify(caption=caption)
    else:
        response = json.jsonify(error='Could not retrieve caption. You did not provide a valid picture id.', status=422)
        response.status_code = 422
        return response


@pic.route(append_key('/pic/caption'), methods=['POST'])
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
        response = json.jsonify(error='Could not update caption. You did not provide a valid picture id or caption.',
                                status=404)
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

    query = "SELECT caption FROM Contain WHERE picid='%s';" % picid
    con = mysql.connection
    cur = con.cursor()
    cur.execute(query)
    results = cur.fetchall()
    if len(results) == 0:
        response = json.jsonify(error='Could not update caption. The picture id was not valid.', status=422)
        response.status_code = 422
        return response

    query = "UPDATE Contain SET caption='%s' WHERE picid='%s';" % (caption, picid)
    cur.execute(query)
    con.commit()

    response = json.jsonify(id=picid, status=201)
    response.status_code = 201
    return response
