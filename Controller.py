from flask import *
from flask_wtf import *
from wtforms import *
from lorem import *

class Pages:
    def __init__(self):
        pass

    def about(self):
        return render_template('about.html', title='About', lorem=what)

    def home(self):
        return render_template('home.html', title='Home', info=info, to_do=to_do, some=some)

    def download(self):
        return render_template('download.html', title='Download')

    def levels(self):
        return render_template('levels.html', title = 'Levels')

    def login(self):
        return render_template('login.html', title='Login')

