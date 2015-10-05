from flask import Flask, render_template
import controllers
from utils import mysql, configApp
import os
app = Flask(__name__, template_folder='views', static_url_path='/static')


app.register_blueprint(controllers.main)
app.register_blueprint(controllers.album)
app.register_blueprint(controllers.albums)
app.register_blueprint(controllers.pic)
app.register_blueprint(controllers.login)
app.register_blueprint(controllers.user)


app.secret_key = '\xe8/\x04Y\x13x>\x99\xfd\xfb4!\x11\x8b\xb2\xd3\x9b\xd6\xe7\x96Q\xf0\xfa8'

@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'), 404

configApp(app)
mysql.init_app(app)

# comment this out using a WSGI like gunicorn
# if you dont, gunicorn will ignore it anyway
if __name__ == '__main__':
    # listen on external IPs
    app.run(host='0.0.0.0', port=3000, debug=True)
