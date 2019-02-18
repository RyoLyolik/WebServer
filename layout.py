from flask import *
from flask_wtf import *
from wtforms import *
from lorem import *
from wtforms.validators import DataRequired
from Controller import *
from data_base_control import *

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

dbase = DB()
users = Users(dbase.get_connection())
users.init_table()

app = Flask(__name__)
pages = Pages()
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
@app.route('/')
@app.route('/home')
def home():
    return pages.home()

@app.route('/about')
def about():
    return pages.about()

@app.route('/download')
def download():
    return pages.download()

@app.route('/levels')
def levels():
    return pages.levels()
# @app.route('/login')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return pages.login(form)
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email, password)
        exists = users.exists(email, password)
        if (exists[0]):
            print(exists)
            session['email'] = email
            session['user_id'] = exists[1][0]
            session['name'] = exists[1][1]
            session['levels'] = exists[1][2]
        return redirect("/index")

@app.route('/registration', methods=['GET','POST'])
def reg():
    if request.method == 'GET':
        return pages.registration(form)
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        if email is not None and password and not None and name is not None:
            try:
                users.insert(name,password,email)
            except sqlite3.IntegrityError:
                return '<h1>Такая почта уже используется</h1>'

        else:
            return '<h1>Заполните все поля</h1>'

        return redirect('/index')

@app.route('/logout')
def logout():
    session.pop('email',0)
    session.pop('user_id',0)
    return redirect('/login')

@app.route('/index')
def index():
    if session['email'] not in session:
        return redirect('/login')
    return render_template('home.html', email=session['email'])

@app.route('/profile')
def profile():
    return pages.profile()
if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')