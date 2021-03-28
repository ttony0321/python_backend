import os
from flask import request
from flask import Flask, render_template, redirect, session
from api_v1 import api as api_v1
from models import db, User, Todo
from form import RegisterForm, LoginForm

app = Flask(__name__)
app.register_blueprint(api_v1, url_prefix='/api/v1')


basdir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basdir, 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'testscrf'

db.init_app(app)
db.app = app
db.create_all()


@app.route('/', methods=['GET'])
def home():     #로그인 안할경우 에러화면 뜸
    userid = session.get('userid', None)
    todos = []
    if userid:
        user = User.query.filter_by(userid=userid).first()
        todos = Todo.query.filter_by(user_id=user.id)
    return render_template('home.html', userid=userid, todos=todos)#templates 에다가 전달


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():#로그인이 됬으면 session 사용됬을꺼
        session['userid'] = form.data.get('userid')
        print('login susccss')
        return redirect('/')
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid', None)
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        user.userid = form.data.get('userid')
        user.password = form.data.get('password')

        db.session.add(user)
        db.session.commit()
        print('susccss')
        return redirect('/login')

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
