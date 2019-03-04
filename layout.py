from flask import *
from flask_wtf import *
from wtforms import *
from lorem import *
from wtforms.validators import DataRequired
from Controller import *
from data_base_control import *
import os


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


dbase = DB()
users = Users(dbase.get_connection())
users.init_table()

lvls = Levels(dbase.get_connection())
lvls.table_init()

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
    l = lvls.get_all(level_id=None)
    print(l)
    return pages.levels(lvls=l)


@app.route('/login', methods=['GET', 'POST'])
def login():
    print(session)
    if 'name' not in session:
        if request.method == 'GET':
            return pages.login(form, False)
        elif request.method == 'POST':
            print('POST')
            email = request.form['email']
            password = request.form['password']
            print(email, password)
            exists = users.exists(email, password)
            print(exists, 'exists')
            if (exists[0]):
                session['email'] = email
                session['user_id'] = exists[1][0]
                session['name'] = exists[1][1]
                session['levels'] = exists[1][3]
                session['password'] = exists[1][2]
                return redirect("/index")
            elif exists[0] is False:
                return pages.login(form, True)
    else:
        return redirect('/')


@app.route('/registration', methods=['GET', 'POST'])
def reg():
    if 'name' not in session:
        if request.method == 'GET':
            return pages.registration(form)
        elif request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            name = request.form['name']
            if email is not None and password and not None and name is not None:
                try:
                    users.insert(name, password, email)
                except sqlite3.IntegrityError:
                    return '<h1>Такая почта уже используется</h1>'

            else:
                return '<h1>Заполните все поля</h1>'

            return redirect('/index')

    else:
        return redirect('/')


@app.route('/logout')
def logout():
    session.pop('email', 0)
    session.pop('user_id', 0)
    session.pop('levels', 0)
    session.pop('name', 0)
    return redirect('/login')


@app.route('/index')
def index():
    if session['email'] not in session:
        return redirect('/login')
    return render_template('home.html', name=session['name'])


@app.route('/profile')
def profile():
    return pages.profile()


@app.route('/load', methods=['POST', 'GET'])
def load():
    if 'name' in session:
        if request.method == 'GET':
            return pages.load()

        elif request.method == 'POST':
            file = request.files['file']
            data = file.read()
            data = data.decode('utf-8')
            data = data.split('\n')
            data = ''.join(data)
            lvl_id = lvls.insert(session['user_id'])
            f = open('databases/levels/lvl_' + str(lvl_id) + '.txt', mode='w')
            f.writelines(data)
            f.close()
            return pages.load()

    else:
        return redirect('/')


@app.route('/current_lvl=<int:lvl_id>', methods=['POST', 'GET'])
def current_level(lvl_id):
    lvl_info = lvls.get_all(level_id=lvl_id)
    if len(lvl_info) == 0:
        return 'Такого уровня нет'
    else:
        return pages.current_level(lvl_info[0])


@app.route('/current_lvl=<int:lvl_id>/download', methods=['POST', 'GET'])
def download_level(lvl_id):
    filename = 'lvl_' + str(lvl_id) + '.txt'
    upload = 'databases/levels/'
    return send_file(upload + filename, as_attachment=True, attachment_filename=filename)


@app.route('/current_lvl=<int:lvl_id>/get', methods=['POST', 'GET'])
def get_level(lvl_id):
    if request.method == 'GET':
        filename = 'lvl_' + str(lvl_id) + '.txt'
        upload = 'databases/levels/'
        file = open(upload + filename, mode='r', encoding='utf-8')
        data = file.read()
        return data

@app.route('/get_list_of_levels')
def get_levels():
    l = lvls.get_all(level_id=None)
    levels_ids = [str(i[0]) for i in l]
    return '\n'.join(levels_ids)

if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
