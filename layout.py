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

@app.route('/levels')
def levels():
    return pages.levels()
# @app.route('/login')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)

if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')