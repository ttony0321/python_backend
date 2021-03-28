from models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    repassword = PasswordField('repassword', validators=[DataRequired()])


class LoginForm(FlaskForm):

    class UserPassword(object):
        def __init__(self, message=None):
            self.message = message

        def __call__(self, form, field):
            userid = form['userid'].data
            password = field.data

            user = User.query.filter_by(userid = userid).first()#같은 id 검색
            if user.password != password:#같은 id의 비번과 입력된 비번 같은지 확인
                raise ValueError('Wrong password')
    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), UserPassword()])