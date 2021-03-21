from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from models import User

class RegisterForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('re_password')])
    re_password = PasswordField('re-password', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])


class LoginForm(FlaskForm):
    #로그인 폼 안에서만 사용
    class UserPassword(object):
        def __init__(self, message=None):
            self.message = message

        def __call__(self, form, field):
            userid = form['userid'].data
            password = field.data
            user = User.query.filter_by(userid=userid).first()#데이터속 id와 비교
            if user.password != password:
                raise ValueError('Wrong Password')
    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), UserPassword()])
