from utils import appendKey, mysql, secretKey
from flask import *
# -*- coding: utf-8 -*-

main = Blueprint('main', __name__, template_folder='views')

@main.route(appendKey('/'))
def main_route():
	cur = mysql.connection.cursor()
	cur.execute("SELECT username FROM User")
	msgs = cur.fetchall()
	return render_template("index.html", usernames=msgs, secretKey=secretKey)
