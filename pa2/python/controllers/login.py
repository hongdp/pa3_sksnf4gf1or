from utils import appendKey, mysql
from flask import *
import hashlib
import os
import time

login = Blueprint('login', __name__, template_folder='views')

@login.route(appendKey('/login'), methods=['GET', 'POST'])
def login_func():
    url = request.args.get('url')
    if request.method == 'GET':
    	if 'username' in session:
    		return redirect(url)		
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url)
    return render_template('login.html')

@login.route(appendKey('/logout'), methods=['GET'])
def logout_func():
    session.clear();
    return redirect(url_for('main.main_route'))