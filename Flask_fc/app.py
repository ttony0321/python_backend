import os
from flask import Flask, session
from flask import render_template
from models import db
from flask import request, redirect
from models import User
from flask_jwt import JWT
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm
from api_v1 import api as api_v1



app = Flask(__name__)
app.register_blueprint(api_v1, url_prefix='/api/v1')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #로그인 세션 아이디에 form 유저아이디 가져와서 넣기
        session['userid'] = form.data.get('userid')
        return redirect('/')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
#    if request.method == 'POST':
#        userid = request.form.get('userid')
#        username = request.form.get('username')
#        password = request.form.get('password')
#        re_password = request.form.get('re-password')
#        if (userid and username and password and re_password) and password == re_password:
        user = User()
        user.userid = form.data.get('userid')
        user.username = form.data.get('username')
        user.password = form.data.get('password')
            #추가하기
        db.session.add(user)
        db.session.commit()
        print('success')
        return redirect('/')
    return render_template('register.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    #값 꺼내기
    session.pop('userid', None)
    return redirect('/')

@app.route('/')
def hello_world():
    userid = session.get('userid', None)
    return render_template('hello.html', userid=userid)



basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basedir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'testscrf'

#csrf = CSRFProtect(app)
#csrf.init_app(app)
db.init_app(app)#설정 초기화
db.app = app
db.create_all()


def authenticate(username, password):
    user = User.query.filter(User.userid == username).first()
    if user.password == password:
        return user


def identity(payload):
    userid = payload['identity']
    return User.query.filter(User.id == userid).first()


jwt = JWT(app, authenticate, identity)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
