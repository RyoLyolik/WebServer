from flask import *
from flask_wtf import *
from wtforms import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title='About', header='Home')


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')