from flask import *
from flask_wtf import *
from wtforms import *
from lorem import *

app = Flask(__name__)
class Pages:
    def __init__(self):
        pass

    def about(self):
        return render_template('about.html', title='About', lorem=what)

    def home(self):
        return render_template('home.html', title='Home', info=info, to_do=to_do)
pages = Pages()
@app.route('/about')
def about():
    return pages.about()

@app.route('/home')
def home():
    return pages.home()

@app.route('/')
def ret():
    return redirect('/home')


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')