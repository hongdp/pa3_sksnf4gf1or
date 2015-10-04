from utils import appendKey, mysql
from flask import *
import hashlib
import os
import time

login = Blueprint('login', __name__, template_folder='views')

@login.route(appendKey('/login'), methods=['GET', 'POST'])
def login():
    url = request.args.get('url')
    if request.method == 'POST':
        session['username'] = request.form['username']

        return redirect(url)
    return ''
