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
        return render_template('home.html', title='Home', info=info, to_do=to_do, some=some)

    def download(self):
        return render_template('download.html', title='Download')
pages = Pages()

@app.route('/')
def ret():
    return redirect('/home')

@app.route('/home')
def home():
    return pages.home()

@app.route('/about')
def about():
    return pages.about()

@app.route('/download')
def download():
    return pages.download()


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')