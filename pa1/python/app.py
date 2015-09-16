from flask import Flask, render_template
import controllers
from utils import mysql

app = Flask(__name__, template_folder='views', static_url_path='/static')

app.register_blueprint(controllers.album)
app.register_blueprint(controllers.albums)
app.register_blueprint(controllers.pic)
app.register_blueprint(controllers.main)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'red123'
app.config['MYSQL_DB'] = 'group88'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)

# comment this out using a WSGI like gunicorn
# if you dont, gunicorn will ignore it anyway
if __name__ == '__main__':
    # listen on external IPs
    app.run(host='0.0.0.0', port=3000, debug=True)
